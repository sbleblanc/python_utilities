
def replace_by_unk(input_fn, output_fn, min_freq, replace_token='<UNK>'):
    wdic = {}
    with open(input_fn, 'r') as in_file:
        for line in in_file:
            for w in line.strip().split(' '):
                if w in wdic:
                    wdic[w] += 1
                else:
                    wdic[w] = 1
    word_filter = set([w for w, c in wdic.items() if c < min_freq])
    with open(input_fn, 'r') as in_file:
        with open(output_fn, 'w') as out_file:
            for line in in_file:
                final_sentence = []
                for w in line.split(' '):
                    if w in word_filter:
                        final_sentence.append(replace_token)
                    else:
                        final_sentence.append(w)
                out_file.write(' '.join(final_sentence))
    return len(wdic), len(word_filter)
