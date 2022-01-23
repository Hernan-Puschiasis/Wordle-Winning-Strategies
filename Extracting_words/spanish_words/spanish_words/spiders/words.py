import scrapy


def word_processing(word):
    word = word.lower()
    letters = ""
    for letter in word:
        if letter == "á":
            letters += 'a'
        elif letter == "é":
            letters += 'e'
        elif letter == "í":
            letters += 'i'
        elif letter == 'ó':
            letters += 'o'
        elif letter == 'ú':
            letters += 'u'
        elif letter == 'ü':
            letters += 'u'
        else:
            letters += letter
    return letters


class Words(scrapy.Spider):
    name = 'words'
    link = 'https://www.palabrascon.com/palabras-con.php?i={}&f=&ms=&mns=&m=&mn=&fs=0&fs2=0&fnl=5&fnl2=5&fa=0&ju=0&d=0&tv=4&Submit=Buscar'
    letters = ['A', "á", 'B', 'C', 'D', 'E', 'é', 'F', 'G', 'H', 'I', 'í', 'J', 'K', 'L', 'M',
               'N', 'Ñ', 'O', 'ó', 'P', 'Q', 'R', 'S', 'T', 'U', 'ú', 'V', 'W', 'X', 'Y', 'Z']
    start_urls = [link.format('a')]
    actual_letter = 0
    words = []
    f = open('words.txt', 'w')

    def parse(self, response):
        all_words = response.css('.omega div a::text').extract()
        for word in all_words:
            new_word = word_processing(word)
            self.f.write(new_word + "\n")
        self.actual_letter += 1
        try:
            yield scrapy.Request(self.link.format(self.letters[self.actual_letter].lower()))
        except IndexError:
            pass
            self.f.close()
