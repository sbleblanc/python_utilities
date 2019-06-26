from lxml import etree
from os import walk, path


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
            #if the correction is a replacement or a deletion, the first child is a <i> node with the erronuous text
            if ns[0].tag == 'i':
                if ns[0].text:
                    s.append(ns[0].text)
                else:
                    print('nested?')
            #Need to append the tail since <NS> tags are inline
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
        for f in files:
            out_file.write(extract_original_text(f))


