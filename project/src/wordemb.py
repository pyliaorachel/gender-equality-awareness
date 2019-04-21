import gensim.downloader as api


class WordEmb:
    def __init__(self, source='word2vec-google-news-300'):
        self.source = source
        self.wv = None
        self.vocab = None
        self.gender_scores = {}
        self.sent_scores = {}

    def init(self, preload_scores=False):
        self.load_word2vec()
        if preload_scores:
            self.load_gender_scores()
            self.load_sent_scores()

    def load_word2vec(self):
        self.wv = api.load(self.source)
        self.vocab = list(self.wv.vocab.keys())

    def load_gender_scores(self):
        self.gender_scores = {}
        for word in self.vocab:
            self.gender_scores[word] = self.gender_score(word)

    def load_sent_scores(self):
        self.sent_scores = {}
        for word in self.vocab:
            self.sent_scores[word] = self.sent_score(word)

    def wordlist_distance(self, word, wordlist):
        if word not in self.vocab:
            return 0
        dist = 0
        for word2 in wordlist:
            dist += self.wv.distance(word, word2)
        dist /= len(wordlist)
        return dist

    def extreme_scores(self, word, ext1_words, ext2_words):
        if word not in self.vocab:
            return 0
        score1 = self.wordlist_distance(word, ext1_words)
        score2 = self.wordlist_distance(word, ext2_words)
        return score1 - score2

    def gender_score(self, word):
        if word not in self.gender_scores:
            male_words = ['male', 'men', 'man', 'boy']
            female_words = ['female', 'women', 'woman', 'girl']
            self.gender_scores[word] = self.extreme_scores(word, male_words, female_words)
        return self.gender_scores[word]

    def sent_score(self, word):
        if word not in self.sent_scores:
            neg_words = ['negative', 'bad', 'poor']
            pos_words = ['positive', 'good', 'excellent']
            self.sent_scores[word] = self.extreme_scores(word, neg_words, pos_words)
        return self.sent_scores[word]