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
import multiprocessing as mp
from concurrent import futures

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
d_lm_neg_master_count = linguistic_tools.constructWordlistFrequency(lm_neg_wordlist.lm_negative, {'':''})
d_lm_neg_master_pct = linguistic_tools.constructWordlistFrequency(lm_neg_wordlist.lm_negative, {'':''})
d_lm_pos_master_count = linguistic_tools.constructWordlistFrequency(lm_positive.lm_positive, {'':''})
d_lm_pos_master_pct = linguistic_tools.constructWordlistFrequency(lm_positive.lm_positive, {'':''})
d_lm_uncertain_master_count = linguistic_tools.constructWordlistFrequency(lm_uncertain.lm_uncertain, {'':''})
d_lm_uncertain_master_pct = linguistic_tools.constructWordlistFrequency(lm_uncertain.lm_uncertain, {'':''})
d_lm_litigous_master_count = linguistic_tools.constructWordlistFrequency(lm_litigous.lm_litigous, {'':''})
d_lm_litigous_master_pct = linguistic_tools.constructWordlistFrequency(lm_litigous.lm_litigous, {'':''})
d_lm_harvard_master_count = linguistic_tools.constructWordlistFrequency(harvard_wordlist.harvard_neg, {'':''})
d_lm_harvard_master_pct = linguistic_tools.constructWordlistFrequency(harvard_wordlist.harvard_neg, {'':''})

def updateMasterCountDictionaries(d_master, d_file):
    for key, value in d_file.items():
        d_master[key] += value


#for file in tqdm(filelist):
def mainthread(file):
    with open(file, 'r', errors='ignore') as f:
        text = f.readlines(10000)
        header_dict = headerSearch.searchEdgarHeader(textSnippet=text)
        #use first cik in edgar file
        cik_header = cleaning_tools.splitEDGARHeader(header_dict, 'CENTRAL INDEX KEY')
        header_dict['CENTRAL INDEX KEY'] = cik_header[0]

        if int(header_dict.get('CENTRAL INDEX KEY', -99)) in int_list:
            #total_obs += 1
            f.seek(0)
            full_text = f.read()
            cleaned_text = linguistic_tools.parse_document(full_text, purge_tables=True)
            cleaned_text = cleaned_text.upper()
            f_words = linguistic_tools.wordFrequency(cleaned_text)
            return (f_words, header_dict)
            #print('out')
        else:
            return False


def mp_handler():
    cpu = mp.cpu_count() - 1
    total_obs = 0
    with futures.ProcessPoolExecutor(max_workers=cpu) as executor:

        running = {executor.submit(mainthread, file): file for file in
               tqdm(filelist)}

        for f_words in futures.as_completed(running):
            f_words = f_words._result
            if f_words:
                header_dict = f_words[1]
                f_words = f_words[0]

                f_neg = linguistic_tools.constructWordlistFrequency(lm_neg_wordlist.lm_negative, f_words)
                f_pos = linguistic_tools.constructWordlistFrequency(lm_positive.lm_positive, f_words)
                f_litigous = linguistic_tools.constructWordlistFrequency(lm_litigous.lm_litigous, f_words)
                f_uncertain = linguistic_tools.constructWordlistFrequency(lm_uncertain.lm_uncertain, f_words)
                f_harvard = linguistic_tools.constructWordlistFrequency(harvard_wordlist.harvard_neg, f_words)

                output_filenames = ['master_count_{}.json'.format(header_dict['ACCESSION NUMBER']),
                                    'harvard_count_{}.json'.format(header_dict['ACCESSION NUMBER']),
                                    'litigous_count_{}.json'.format(header_dict['ACCESSION NUMBER']),
                                    'neg_count_{}.json'.format(header_dict['ACCESSION NUMBER']),
                                    'pos_count_{}.json'.format(header_dict['ACCESSION NUMBER']),
                                    'uncert_count_{}.json'.format(header_dict['ACCESSION NUMBER']),]

                l_data_files = [f_words, f_harvard, f_litigous, f_neg, f_pos, f_uncertain]

                f_l_output_files = os_tools.constructOutputFilenames(os.path.join(OUTPATH, 'LM_DOCS'), output_filenames)

                os_tools.multipleSaveToJson(f_l_output_files, l_data_files)

                linguistic_tools.updateDictionary(d_lm_uncertain_master_count, f_uncertain)
                linguistic_tools.updateDictionary(d_lm_pos_master_count, f_pos)
                linguistic_tools.updateDictionary(d_lm_neg_master_count, f_neg)
                linguistic_tools.updateDictionary(d_lm_litigous_master_count, f_litigous)
                linguistic_tools.updateDictionary(d_master_word_count, f_words)
                linguistic_tools.updateDictionary(d_lm_harvard_master_count, f_harvard)
                total_obs += 1
                print(total_obs)

if __name__ == '__main__':
    mp_handler()

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