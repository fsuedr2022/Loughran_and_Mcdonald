import unittest
import linguistic_tools
import cleaning_tools

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_convertStrListtoIntList(self):
        cik_list = [
            '1750',
            '313368',
            '910627',
            '702511',
            '61478',
            '4911',
            '2668',
            '319126',
            '2880',
            '730469',
        ]
        int_list = cleaning_tools.convertStrListtoIntList(cik_list)
        for item in int_list:
            self.assertTrue(type(item) is int)

    def test_wordcount(self):
        self.assertEqual(6, linguistic_tools.countWords('a a a a a a'))

    def test_wordFrequency(self):
        word_frequency = linguistic_tools.wordFrequency('The the The the The quick Quick quick Quick quick')
        word_frequency_lc = linguistic_tools.wordFrequency('The the The the The quick Quick quick Quick quick'.lower())
        word_frequency_uc = linguistic_tools.wordFrequency('The the The the The quick Quick quick Quick quick'.upper())
        self.assertEqual(3, word_frequency.get('The'))
        self.assertEqual(5, word_frequency_lc.get('the'))
        self.assertEqual(5, word_frequency_uc.get('THE'))

    def test_tfIDF(self):
        dict_list = []
        dict_list.append(linguistic_tools.wordFrequency('The the The the The quick Quick quick Quick quick'))
        dict_list.append(linguistic_tools.wordFrequency('The the The the The quick Quick quick Quick quick'.lower()))
        dict_list.append(linguistic_tools.wordFrequency('The the The the The quick Quick quick Quick quick'.upper()))
        doc_freq = linguistic_tools.documentFrequency(dict_list)
        self.assertEqual(7, doc_freq['the'])
        self.assertEqual(5, doc_freq['QUICK'])
        self.assertEqual(2, doc_freq['Quick'])

    def test_cumWordCount(self):
        word_frequency = linguistic_tools.wordFrequency('The the The the The quick Quick quick Quick quick')
        d_word_freq = linguistic_tools.cumulativePercentWords(word_frequency)
        total_percent = 0
        for value in d_word_freq.values():
            total_percent += value
        self.assertEqual(1, total_percent)

    def test_countWordsinWordlist(self):
        word_frequency = linguistic_tools.wordFrequency('The the The the The quick Quick quick Quick quick')
        wordlist = ['the']
        wordcount = linguistic_tools.countAllWordsInWordList(wordlist, word_frequency)
        self.assertEqual(2, wordcount)

    def test_countConstructedWordlist(self):
        word_frequency = linguistic_tools.wordFrequency('The the The the The quick Quick quick Quick quick')
        wordlist = ['the']
        wordcount = linguistic_tools.constructWordListFrequency(wordlist, word_frequency)
        self.assertEqual(2, wordcount.get('the', 0))
        self.assertEqual(0, wordcount.get('The', 0))

if __name__ == '__main__':
    unittest.main()
