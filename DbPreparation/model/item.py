class Item:
    def __init__(self, word, url):
        self.word = word
        self.url = url

    def get_word(self):
        return self.word

    def get_url(self):
        return self.url

    def __hash__(self):
        return hash((self.word, self.url))

    def __eq__(self, other):
        return (self.word, self.url) == (other.word, other.url)

    def to_json(self):
        return {'word': self.word, 'url': self.url}
