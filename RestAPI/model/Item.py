class Item:
    def __init__(self, word, url, cat):
        self.word = word
        self.url = url
        self.cat = cat

    def __hash__(self):
        return hash((self.word, self.url, self.cat))

    def __eq__(self, other):
        return (self.word, self.url) == (other.word, other.url)

    def to_json(self):
        return {'word': self.word, 'url': self.url, 'cat': self.cat}
