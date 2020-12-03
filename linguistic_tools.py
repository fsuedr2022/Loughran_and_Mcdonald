from collections import defaultdict
from bs4 import BeautifulSoup
import lxml


def updateDictionary(d_master, d_file):
    '''
    Updates master dictionary with counts
    :param d_master: master dictionary
    :param d_file: observation dictionary
    :return: updated master dictionary
    '''
    for key, value in d_file.items():
        try:
            d_master[key] += value
        except KeyError:
            d_master[key] = value
    return d_master

def countWords(document):
    '''
    Returns count of words in a document
    :param document: String
    :return: Integer with total count of words
    '''
    return len(document.split())

def wordFrequency(words):
    '''
    Counts word frequency
    :param words: String
    :return: default dict that counts instances of words in a single document
    '''
    assert type(words) is str
    word_count = defaultdict(int)
    l_words = words.split()
    for word in l_words:
        word_count[word] += 1
    return word_count

def documentFrequency(l_tf_dict):
    '''
    Creates document frequency dictionary
    :param l_tf_dict: List of default dictionaries
    :return: default dictionary that counts the frequency of words in a population of documents
    '''
    assert type(l_tf_dict) is list
    idf_dict = defaultdict(int)
    for tf_dict in l_tf_dict:
        for key, value in tf_dict.items():
            idf_dict[key] += value
    return idf_dict

def constructWordlistCount(l_wordlist, d_word):
    '''
    :param l_wordlist: wordlist to count words in document
    :param d_word: Count of words in dictionary format
    :return: integer that counts the total words in the document listed in the wordlist
    '''
    assert type(l_wordlist) is list
    word_count = 0
    for word in l_wordlist:
        word_count += d_word.get(word, 0)
    return word_count


def constructWordlistFrequency(l_wordlist, d_word):
    '''
    constructs the frequency of words in a wordlist for a document
    :param l_wordlist: wordlist to construct
    :param d_word: frequency of words in a single document
    :return: dictionary of words with frequencies as values and words as keys
    '''
    assert type(l_wordlist) is list
    d_return_word = defaultdict(int)
    for word in l_wordlist:
        d_return_word[word] = d_word.get(word, 0)
    return d_return_word

def constructTfIdf(d_doc_wordcount, d_pop_wordcount, l_wordlist = None):
    '''
    constructs the TFIDF value for each word in a document
    :param d_doc_wordcount:
    :param d_pop_wordcount:
    :param l_wordlist:
    :return: TfIDF score for word
    '''

def cumulativePercentWords(word_dictionary):
    '''
    Returns the cumulative percent of each word in dictionary form
    :param word_dictionary: dictionary of words
    :return: dictionary of cumulative percentage of words in document or wordlist
    '''
    i_cumulative_word_count = 0
    for key in word_dictionary.keys():
        i_cumulative_word_count += word_dictionary.get(key, 0)
    d_cumulative_word_count = {}
    for key in word_dictionary.keys():
        d_cumulative_word_count[key] = word_dictionary.get(key, 0)/i_cumulative_word_count
    return d_cumulative_word_count

def parse_document(document, purge_tables=False):
    '''
    Returns raw text from html document
    :param document: html document -- type string
    :param purge_tables: boolean value to destroy tables if they are not needed
    :return: text of html document without html code
    '''
    assert type(document) is str
    soup = BeautifulSoup(document, 'lxml')
    if purge_tables:
        for table in soup.find_all("table"):
            table.decompose()
    return soup.get_text()


