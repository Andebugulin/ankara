import datetime
import pygame
import pandas as pd
import random


white = '#FBFBF8'

green = (0, 255, 0)
blue = (0, 0, 128)
black = (25, 25, 25)

Days_full_of_relax_if_class_is_5 = 3

pygame.init()
X, Y = 1700, 900
display_surface = pygame.display.set_mode((X, Y))
pygame.display.set_caption('You can bear it, i believe in you')

pygame.display.set_mode((X, Y))

# xls file with the data (excel)
file = 'capture.xlsx'


class Word:
    screen = display_surface
    font = pygame.font.SysFont('Helvetica', 70)
    deck_without_shuffle = []
    deck = []
    deck_without_reverse_cards = []

    @staticmethod
    def shuffle():
        data = Word.deck_without_shuffle
        normalized_data = []
        counter_for_10 = set()
        small_list_with_words = []
        for i in data:
            counter_for_10.add(i.example)
            small_list_with_words.append(i)
            if len(counter_for_10) == 10:
                normalized_data.append(random.sample(small_list_with_words, len(small_list_with_words)))
                counter_for_10 = set()
                small_list_with_words = list()
        if len(counter_for_10) != 0:
            normalized_data.append(random.sample(small_list_with_words, len(small_list_with_words)))

        for i in normalized_data:
            for j in i:
                Word.deck.append(j)

    @staticmethod
    def reading_from_file():
        data = pd.read_excel(file, index_col=0, parse_dates=True)

        data['classes'] = data['classes'].fillna(0)
        data['date'] = data['date'].fillna(datetime.date.today())
        data.to_excel(file)
        # initialization of objects
        for index, date_word_meaning_ex in data.iterrows():
            # classes and date have altering type.
            word_meaning_ex = [i.strip() for i in date_word_meaning_ex.tolist()[1:-1]]
            date = date_word_meaning_ex.tolist()[0]
            _class = date_word_meaning_ex.tolist()[-1]
            object0 = Word(word_meaning_ex[0], word_meaning_ex[1], word_meaning_ex[2], date, _class)
            if _class < 5:
                Word.deck_without_reverse_cards.append(object0)

                # for reverse cards ( cards where questionare may ask about cards' meaning as well )

                Word.deck_without_shuffle.append(object0)
                Word.deck_without_shuffle.append(
                    Word(word_meaning_ex[1], word_meaning_ex[0], word_meaning_ex[2], date, _class))
            else:
                if (datetime.date.today().day - date.day) % Days_full_of_relax_if_class_is_5 == 0:
                    Word.deck_without_shuffle.append(object0)
                    Word.deck_without_reverse_cards.append(object0)

    @staticmethod
    def save_changes():
        classes = [i.class0 for i in Word.deck_without_reverse_cards]
        data = pd.read_excel(file, parse_dates=True, index_col=0)
        data['classes'] = classes
        data.to_excel(file)

    @staticmethod
    def rendering(massage: str, text: str, position):
        sentence = massage.split()
        space = Word.font.size(' ')[0]
        x, y = position
        for element in sentence:
            word_surface = Word.font.render(element, True, black)
            word_wid, word_hei = word_surface.get_size()
            if x + word_wid >= X:
                x = position[0]
                y += 80
            Word.screen.blit(word_surface, (x, y))
            x += word_wid + space

        x = position[0]
        y += 80
        sentence = text.split()
        for text in sentence:
            word_surface = Word.font.render(text, True, black)
            word_wid, word_hei = word_surface.get_size()
            if x + word_wid >= X:
                x = position[0]
                y += 80
            Word.screen.blit(word_surface, (x, y))
            x += word_wid + space

    def __init__(self, word: str, meaning: str, example: str, date: datetime, _class=0):
        self.__word = word
        self.__meaning = meaning
        self.__example = example
        self.__class = _class
        self.__date = date

        self.word_showing = True
        self.meaning_showing = False
        self.example_showing = False
        self.permission_for_changing_class = True

    def switch(self, word=False, meaning=False, example=False):
        self.word_showing = word
        self.meaning_showing = meaning
        self.example_showing = example

    def show_word(self):
        if self.word:
            pass

    def show_meaning(self):
        if self.meaning:
            pass

    def show_example(self):
        if self.example:
            pass

    def show(self):
        if self.word_showing:
            self.show_word()
        elif self.meaning_showing:
            self.show_meaning()
        else:
            self.show_example()

    @property
    def word(self):
        return self.__word

    @word.getter
    def word(self):
        Word.rendering('word:', self.__word, (20, 20))
        return self.__word

    @property
    def meaning(self):
        return self.__meaning

    @meaning.getter
    def meaning(self):
        Word.rendering('meaning:', self.__meaning, (20, 20))
        return self.__meaning

    @property
    def example(self):
        return self.__example

    @example.getter
    def example(self):
        Word.rendering('example:', self.__example, (20, 20))
        return self.__example

    @property
    def class0(self):
        return self.__class

    @class0.getter
    def class0(self):
        return self.__class

    @class0.setter
    def class0(self, value: int):
        if self.permission_for_changing_class:
            if value > 3:
                if self.__class != 5:
                    self.__class += 1
            else:
                if self.__class != 0:
                    self.__class -= 1
                Word.deck.append(Word.deck[index_current_word])
            self.permission_for_changing_class = False


Word.reading_from_file()
display_surface.fill(white)
Word.rendering('hello',
               '''for start press almost random key :^)-----------------------------------------------------------------
               -
               -
               -       
               
                  Instructions: 
                  Tool for learning words
                   ---------------------------------------------------------------------------------                                             
                  use short_keys:                             
                  keys: Ff(word)- Dd(face)- Ss(example)- Space(for the next word) -
                  Arrow to the right side(for the next word) -
                  Arrow to the left side(for the previous word)
                  --------------------------------------------------------------------------       
                  evaluation: 1 do not remember-
                              2 hard -
                              3 normal  -
                              4 nice-
                              5 very impressive''',
               (20, 20))
pygame.display.update()

start = False
while not start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            start = True
Word.shuffle()
index_current_word = 0
while True:
    display_surface.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Word.save_changes()
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                Word.deck[index_current_word].switch(word=True)
            elif event.key == pygame.K_d:
                Word.deck[index_current_word].switch(meaning=True)
            elif event.key == pygame.K_s:
                Word.deck[index_current_word].switch(example=True)
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RIGHT:
                index_current_word += 1
            elif event.key == pygame.K_LEFT:
                index_current_word -= 1
            # 1 - do not remember
            # 2 - hard
            # 3 - normal
            # 4 - nice
            # 5 - very impressive
            elif event.key == pygame.K_1:
                Word.deck[index_current_word].class0 = 1
                index_current_word += 1
            elif event.key == pygame.K_2:
                Word.deck[index_current_word].class0 = 2
                index_current_word += 1
            elif event.key == pygame.K_3:
                Word.deck[index_current_word].class0 = 3
                index_current_word += 1
            elif event.key == pygame.K_4:
                Word.deck[index_current_word].class0 = 4
                index_current_word += 1
            elif event.key == pygame.K_5:
                Word.deck[index_current_word].class0 = 5
                index_current_word += 1
    Word.deck[index_current_word].show()
    pygame.display.update()
