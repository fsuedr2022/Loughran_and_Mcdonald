import os
import os_tools
import linguistic_tools
import cik_filter
import lm_litigous
import lm_neg_wordlist
import lm_positive
import lm_uncertain
import harvard_wordlist
import json
import cleaning_tools
from tqdm import tqdm

from headerParse import runEdgarHeaderSearch
#construct header search
headerSearch = runEdgarHeaderSearch()

DIRPATH = os.path.join('/media','abc-123','M2','DOWNLOADS')
OUTPATH = os.path.join('/media','abc-123','M2')

filelist = os_tools.get_file_list(DIRPATH)
int_list = cleaning_tools.convertStrListtoIntList(cik_filter.cik_list)

#construct master variables
#TODO: Is there a better way to do this?
total_obs = 0
d_master_word_count = {}
d_master_word_pct = {}
d_lm_neg_master_count = linguistic_tools.countAllWordsInWordList(lm_neg_wordlist.lm_negative, {})
d_lm_neg_master_pct = linguistic_tools.countAllWordsInWordList(lm_neg_wordlist.lm_negative, {})
d_lm_pos_master_count = linguistic_tools.countAllWordsInWordList(lm_positive.lm_positive, {})
d_lm_pos_master_pct = linguistic_tools.countAllWordsInWordList(lm_positive.lm_positive, {})
d_lm_uncertain_master_count = linguistic_tools.countAllWordsInWordList(lm_uncertain.lm_uncertain, {})
d_lm_uncertain_master_pct = linguistic_tools.countAllWordsInWordList(lm_uncertain.lm_uncertain, {})
d_lm_litigous_master_count = linguistic_tools.countAllWordsInWordList(lm_litigous.lm_litigous, {})
d_lm_litigous_master_pct = linguistic_tools.countAllWordsInWordList(lm_litigous.lm_litigous, {})
d_lm_harvard_master_count = linguistic_tools.countAllWordsInWordList(harvard_wordlist.harvard_neg, {})
d_lm_harvard_master_pct = linguistic_tools.countAllWordsInWordList(harvard_wordlist.harvard_neg, {})

def updateMasterCountDictionaries(d_master, d_file):
    for key, value in d_file.items():
        d_master[key] += value


for file in tqdm(filelist):
    with open(file, 'r', errors='ignore') as f:
        text = f.readlines(10000)
        header_dict = headerSearch.searchEdgarHeader(textSnippet=text)
        #use first cik in edgar file
        cik_header = cleaning_tools.splitEDGARHeader(header_dict, 'CENTRAL INDEX KEY')
        header_dict['CENTRAL INDEX KEY'] = cik_header[0]

        if int(header_dict.get('CENTRAL INDEX KEY', -99)) in int_list:
            total_obs += 1
            f.seek(0)
            full_text = f.read()
            cleaned_text = linguistic_tools.parse_document(full_text, purge_tables=True)

        else:
            continue

l_master_data_files = [d_master_word_pct, d_master_word_count, d_lm_harvard_master_count, d_lm_harvard_master_pct, d_lm_litigous_master_count,
                       d_lm_litigous_master_pct, d_lm_neg_master_count, d_lm_neg_master_pct, d_lm_pos_master_count, d_lm_pos_master_pct,
                       d_lm_uncertain_master_count, d_lm_uncertain_master_pct]

output_filenames = ['master_pct.json', 'master_count.json', 'harvard_count.json', 'harvard_pct.json', 'litigous_count.json',
                    'litigous_pct.json', 'neg_count.json', 'neg_pct.json', 'pos_count.json', 'pos_pct.json', 'uncert_count.json',
                    'uncert_pct.json']

l_output_files = os_tools.constructOutputFilenames(OUTPATH, output_filenames)

os_tools.multipleSaveToJson(l_master_data_files, l_output_files)

print(total_obs)
print('done')