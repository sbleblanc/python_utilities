from lxml import etree

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
                s.append(ns[0].text)
            #Need to append the tail since <NS> tags are inline
            s.append(ns.tail)
        sentences.append(''.join(s))
    return '\n'.join(sentences)
