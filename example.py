import python_utilities.data.preprocess as pp

# dup_pairs = pp.detect_dup_docs('/home/samuel/Documents/Corpus/BookCorpus/BC Processed')
# with open('temp/dup_results.txt', 'w') as out_file:
#     for r, c in dup_pairs:
#         out_file.write('{}: {}\n'.format(r, c))

_, _, lc = pp.replace_by_unk('temp/BookCorpus_historical_partial_bod.txt', 'temp/bc_historical_partial_bod_unk_num.txt', 'temp/stats_bc_historical_partial.txt', 10000, unk_thresh=0.99)
# _, _, lc = pp.replace_by_unk('temp/bc_historical_combined.txt', 'temp/bc_historical_combined_unk_num.txt', 'temp/bc_historical_combined_stats.txt', 10000, unk_thresh=0.99)
print(lc)
# lc = pp.adjust_corpus_to_characters('temp/BookCorpus_unique.txt', 'temp/BookCorpus_unique_char_256.txt')
# print('{} lines'.format(lc))
