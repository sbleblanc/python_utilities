from lxml import etree
from os import walk, path
from python_utilities.utils.utils_fn import print_progress_bar


def extract_original_text(file):
    doc = etree.parse(file)
    sentences = []

    #All text is in 'p' tags
    for p in doc.iterfind('.//p'):
        s = []
        if p.text:
            s.append(p.text)
        #Errors are in <NS> nodes
        for ns in p:
            #Some NS tags are nested, we grab the deepest
            nested_ns = ns.findall('.//NS')
            if len(nested_ns) > 0:
                correction_node = nested_ns[-1]
            else:
                correction_node = ns
            # if the correction is a replacement or a deletion, the first child is a <i> node with the erronuous text
            if len(correction_node) == 0:
                if correction_node.text:
                    s.append(correction_node.text)
            else:
                if correction_node[0].tag == 'i':
                    if correction_node[0].text:
                        s.append(correction_node[0].text)
                    else:
                        print('nested : {}'.format(file))
            #Need to append the tail (if present) since <NS> tags are inline
            if ns.tail:
                s.append(ns.tail)
        sentences.append(''.join(s))
    return '\n'.join(sentences)


def extract_original_text_to_file(output_fn, dataset_folder, recursive=True):
    files = []
    for dpath, _, fnames in walk(dataset_folder):
        files.extend([path.join(dpath, fn) for fn in fnames])
        if not recursive:
            break
    with open(output_fn, 'w') as out_file:
        for i, f in enumerate(files):
            print_progress_bar(i + 1, len(files), f)
            out_file.write(extract_original_text(f))


