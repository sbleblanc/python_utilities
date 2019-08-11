import re
import heapq
import os
import os.path as osp
from python_utilities.utils.utils_fn import print_progress_bar


def replace_by_unk(input_fn, output_fn, stats_fn, top_k, keep_punc=True, keep_number=False, replace_token='<UNK>', number_token='<NUM>', unk_thresh=0.5, split=1):
    punc_re = re.compile(r"[\'\"\.\,\?\!\-\”\’\“…]+")
    valid_word_re = re.compile(r"[\w\-]+")
    number_re = re.compile(r"\d+[\d\,\.]*")
    wdic = {}
    bod_count = 0
    with open(input_fn, 'r') as in_file:
        for line in in_file:
            for w in line.strip().split(' '):
                if w == '<BOD>':
                    bod_count += 1
                    continue
                if not keep_number:
                    if number_re.search(w) and len(number_re.search(w).group(0)) == len(w):
                        continue
                if keep_punc:
                    if punc_re.search(w) and len(w) == len(punc_re.search(w).group(0)):
                        continue
                if valid_word_re.search(w) and len(valid_word_re.search(w).group(0)) == len(w):
                    if w in wdic:
                        wdic[w] += 1
                    else:
                        wdic[w] = 1
    split_after = bod_count // split
    if split_after == 0:
        split_after = bod_count
    heap_buffer = []
    for w, c in wdic.items():
        heapq.heappush(heap_buffer, (-c, w))
    word_filter = set()
    with open(stats_fn, 'w') as out_file:
        for _ in range(min(top_k, len(wdic))):
            c, w = heapq.heappop(heap_buffer)
            out_file.write('{}: {}\n'.format(w, c))
            word_filter.add(w)
    word_filter.add('<BOD>')
    if keep_punc:
        for p in ["'", '"', '.', ',', '?', '!', '-', '”', '’', '“', '…']:
            word_filter.add(p)
    out_file = None
    line_counter = 0
    bod_count = -1
    file_count = 0
    create_new_file = False
    with open(input_fn, 'r') as in_file:
        for line in in_file:
            if line.strip() == '<BOD>':
                bod_count += 1
                if file_count < split and bod_count % split_after == 0:
                    create_new_file = True
            if create_new_file:
                if out_file:
                    out_file.close()
                out_file = open(osp.join(osp.dirname(output_fn), '{}_{}'.format(file_count + 1, osp.basename(output_fn))), 'w')
                file_count += 1
                create_new_file = False
            final_sentence = []
            for w in line.strip().split(' '):
                if w not in word_filter:
                    if not keep_number and number_re.search(w) and len(number_re.search(w).group(0)) == len(w):
                        final_sentence.append(number_token)
                    else:
                        final_sentence.append(replace_token)
                else:
                    final_sentence.append(w)
            if final_sentence.count(replace_token)/len(final_sentence) <= unk_thresh:
                out_file.write(' '.join(final_sentence) + '\n')
                line_counter += 1
    return len(wdic), len(word_filter), line_counter


def extract_punctuation(input_fn):
    candidates = set()
    punc_re = re.compile(r'[^\w\s]')
    with open(input_fn) as in_file:
        for line in in_file:
            for p in punc_re.findall(line):
                candidates.add(p)
    return candidates


def set_from_textfile(filename):
    sentence_set = set()
    with open(filename, 'r') as in_file:
        for line in in_file:
            sentence_set.add(line.strip())
    return sentence_set


def detect_dup_docs(root_folder, threshold=0.9):
    text_files = []
    for f in os.listdir(root_folder):
        if f.endswith('.txt'):
            text_files.append(osp.join(root_folder, f))

    duplicate_pairs = []
    to_remove = set()
    for i in range(len(text_files) - 1):
        print_progress_bar(i, len(text_files) - 2, 'Comparing {}'.format(osp.basename(text_files[i])))
        if text_files[i] in to_remove:
            continue
        sentence_set_1 = set_from_textfile(text_files[i])
        for j in range(i + 1, len(text_files)):
            if text_files[j] in to_remove:
                continue
            sentence_set_2 = set_from_textfile(text_files[j])
            if len(sentence_set_1) < len(sentence_set_2):
                remove_candidate = text_files[i]
                compare_file = text_files[j]
                compare_length = len(sentence_set_1)
            else:
                remove_candidate = text_files[j]
                compare_file = text_files[i]
                compare_length = len(sentence_set_2)
            if compare_length == 0:
                to_remove.add(remove_candidate)
                duplicate_pairs.append((remove_candidate, 'EMPTY'))
                continue
            duplicate_sentences = sentence_set_1.intersection(sentence_set_2)
            if len(duplicate_sentences) / compare_length > threshold:
                to_remove.add(remove_candidate)
                duplicate_pairs.append((remove_candidate, compare_file))
                break

    return duplicate_pairs


def adjust_corpus_to_characters(input_fn, output_fn, max_len=256, space_token='<S>'):
    line_counter = 0
    with open(input_fn, 'r') as in_file:
        with open(output_fn, 'w') as out_file:
            for line in in_file:
                if len(line.strip()) <= max_len:
                    final_str = []
                    for w in line.strip().split():
                        final_str.extend(list(w))
                        final_str.append(space_token)
                    out_file.write('{}\n'.format(' '.join(final_str[:-1])))
                    line_counter += 1
    return line_counter


def get_corpus_stats(corpus_fn):
    words_total = 0
    sentences_total = 0
    unique_words = set()
    with open(corpus_fn, 'r') as in_file:
        for line in in_file:
            stripped_line = line.strip()
            if stripped_line == '<BOD>':
                continue
            sentences_total += 1
            words = stripped_line.split(' ')
            words_total += len(words)
            unique_words.update(words)
    return words_total, len(unique_words), sentences_total
