from collections import defaultdict

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
        for key, value in tf_dict:
            idf_dict[key] += 1
    return idf_dict

def countAllWordsInWordList(l_wordlist, d_word):
    '''
    :param l_wordlist: Loughran and McDonald wordlist
    :param d_word: Count of words in dictionary format
    :return: integer that counts the total words in the document listed in the wordlist
    '''
    assert type(l_wordlist) is list
    assert type(d_word) is dict
    word_count = 0
    for word in l_wordlist:
        word_count += d_word.get(word, 0)
    return word_count

def constructWordListFrequency(l_wordlist, d_word):
    '''
    constructs the frequency of words in a wordlist for a document
    :param l_wordlist: wordlist to construct
    :param d_word: frequency of words in a single document
    :return: dictionary of words with frequencies as values and words as keys
    '''
    assert type(l_wordlist) is list
    assert type(d_word) is dict
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


