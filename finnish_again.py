import datetime
import math

import pygame
import pandas as pd
import random
from gtts import gTTS
import time
import os
import json

language = 'fi'
white = '#FBFBF8'

green = (0, 255, 0)
blue = (0, 0, 128)
black = (25, 25, 25)

Days_full_of_relax_if_class_is_5 = 3

pygame.init()
X, Y = 1700, 900
screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption('You can bear it, i believe in you')

# xls file with the data (excel)
file = 'finnish_capture.xlsx'

button_list = []


# creating buttons: again, hard, normal, nice, impressive, back, next
class Button:
    def __init__(self, color, x, y, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.text = text

    def draw(self, display_drawing):
        # Call this method to draw the button on the screen
        font = pygame.font.SysFont('Helvetica', 50)
        text = font.render(self.text, True, (0, 0, 0))
        self.width, self.height = text.get_size()
        display_drawing.blit(text,
                             (self.x + 10,
                              self.y - 50))

        pygame.draw.rect(display_drawing, black, (self.x, self.y - self.height, self.width + 20, self.height + 20), 4)

    def where_clicked(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if (pos[0] > self.x) and (pos[0] < self.x + self.width + 20):
            if (pos[1] > self.y - self.height) and (pos[1] < self.y + 20 + self.height):
                return True
        return False


# creating class word with words meanings and examples.
class Word:
    all_words_in_file = []
    screen = screen
    font = pygame.font.SysFont('Helvetica', 70)
    deck_without_shuffle = []
    deck = []
    deck_without_reverse_cards = []

    @staticmethod
    def pronunciation(object_):
        try:
            my_obj = gTTS(text=object_.current, lang=language, slow=False)
            my_obj.save("welcome.mp3")
            time.sleep(0.1)
            pygame.mixer.init()
            pygame.mixer.music.load('welcome.mp3')
            pygame.mixer.music.play()
            clock = pygame.time.Clock()
            while pygame.mixer.music.get_busy():
                pygame.event.poll()
                clock.tick(10)
            pygame.mixer.quit()
            os.remove('welcome.mp3')
        except:
            print("Probably you do not have internet connection for pronouncing API")
            print("Something bad happened, even I do not know what to do.")

    @staticmethod
    def shuffle():
        random.shuffle(Word.deck_without_shuffle)
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
        # create a Pandas Excel writer using 'openpyxl' engine

        data = pd.read_excel(file, index_col=0, parse_dates=True, sheet_name='Sheet1')
        data2 = pd.read_excel(file, sheet_name='Sheet2', index_col=0)
        # read the first sheet from the Excel file
        writer = pd.ExcelWriter(file)
        # modify the dataframe
        # data = pd.read_excel(file, index_col=0, parse_dates=True, sheet_name='Sheet')

        data['last_changes_of_class'] = data['last_changes_of_class'].fillna(
            (datetime.date.today() - datetime.timedelta(days=1)))
        data['classes'] = data['classes'].fillna(0)
        data['date'] = data['date'].fillna(datetime.date.today())
        data['date_becoming'] = data['date_becoming'].fillna(datetime.date(2222, 2, 2))
        data['recalling'] = data['recalling'].fillna(0)
        data['length_of_the_word'] = data['words'].apply(lambda x: len(x.strip()))
        data['how_many_times_did_I_recalle_word'] = data['how_many_times_did_I_recalle_word'].fillna(0)

        data.to_excel(writer, sheet_name='Sheet1', index=True)

        data2.loc[len(data2.index)] = [datetime.date.today(), datetime.datetime.now(),
                                       datetime.datetime.now(), datetime.datetime.now(),
                                       len(Word.deck_without_reverse_cards), len(Word.all_words_in_file)]
        data2.to_excel(writer, sheet_name='Sheet2', index=True)

        writer.save()
        # data.to_excel(file, sheet_name='Sheet')
        index1 = 0
        # initialization of objects
        for index, date_word_meaning_ex in data.iterrows():
            # classes and date have altering type.

            shown = False
            word_meaning_ex = [i.strip() for i in date_word_meaning_ex.tolist()[1:4]]
            date = date_word_meaning_ex.tolist()[0]
            _class = date_word_meaning_ex.tolist()[4]
            last_changes_of_class = date_word_meaning_ex.tolist()[5]
            date_becoming = date_word_meaning_ex[6]
            recalling = date_word_meaning_ex[7]
            how_many_times_did_I_recalle_word = date_word_meaning_ex[8]

            object0 = Word(word_meaning_ex[0], word_meaning_ex[1], word_meaning_ex[2], date, _class,
                           last_changes_of_class, date_becoming, recalling, index1,
                           how_many_times_did_I_recalle_word)
            Word.all_words_in_file.append(object0)
            if _class < 5:
                Word.deck_without_reverse_cards.append(object0)

                # for reverse cards ( cards where questionare may ask about cards' meaning as well )

                Word.deck_without_shuffle.append(object0)
                Word.deck_without_shuffle.append(
                    Word(word_meaning_ex[1], word_meaning_ex[0], word_meaning_ex[2], date, _class,
                         last_changes_of_class, date_becoming, recalling, index1
                         ,
                         how_many_times_did_I_recalle_word
                         ))
                shown = True
            elif recalling == 0:
                if random.uniform(0, 1) < 0.5:
                    object0 = Word(word_meaning_ex[1], word_meaning_ex[0], word_meaning_ex[2], date, _class,
                                   last_changes_of_class, date_becoming, recalling, index1,
                                   how_many_times_did_I_recalle_word)

                Word.deck_without_shuffle.append(object0)
                Word.deck_without_reverse_cards.append(object0)
                shown = True

            if object0.class_changes != datetime.date.today():
                if not shown:
                    if object0.recalling >= 0:
                        object0.recalling -= 1
                        object0.class_changes = datetime.date.today()
                    if object0.recalling < 0:
                        object0.recalling = random.randrange(3,
                                                             6)
                        object0.class_changes = datetime.date.today()
            index1 += 1

    @staticmethod
    def save_changes():
        classes = []
        classes_changes = []
        data_becoming = []
        recalling = []
        list_how_many_times_did_I_recalle_word = []
        time_for_each_word = []

        for element in Word.all_words_in_file:
            classes.append(element.class0)
            classes_changes.append(element.class_changes)
            data_becoming.append(element.when_becoming_5)
            recalling.append(element.recalling)
            list_how_many_times_did_I_recalle_word.append(element.how_many_times_did_I_recalle_word)
            result = {}
            result['time'] = element.time_for_recalling
            result['result'] = element.result
            result = json.dumps(result)
            time_for_each_word.append(result)

        data = pd.read_excel(file, sheet_name='Sheet1', index_col=0, parse_dates=True)
        data2 = pd.read_excel(file, sheet_name='Sheet2', index_col=0)
        writer = pd.ExcelWriter(file)
        # read the first sheet from the Excel file

        data['classes'] = classes
        data['last_changes_of_class'] = classes_changes
        data['date_becoming'] = data_becoming
        data['recalling'] = recalling
        data['how_many_times_did_I_recalle_word'] = list_how_many_times_did_I_recalle_word
        data[datetime.datetime.now()] = time_for_each_word

        data.to_excel(writer, sheet_name='Sheet1', index=True)

        last_row = data2.iloc[-1]
        # change the values in the last row
        last_row['end_time'] = datetime.datetime.now()
        starts = last_row['time_of_start']
        last_row['duration'] = int((datetime.datetime.now() - starts).total_seconds() / 60)
        last_row['amount_of_recalling_words'] = len(Word.deck_without_reverse_cards)
        last_row['amount_of_words_currently'] = len(Word.all_words_in_file)
        data2.iloc[-1] = last_row
        data2.to_excel(writer, sheet_name='Sheet2', index=True)

        writer.save()

    @staticmethod
    def rendering(massage: str, text: str, position):
        if len(button_list) > 1:
            button_list.pop(0)
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
        button_pronunciation = Button(white, 10, y + 160, text='pronunciation')
        button_list.insert(0, button_pronunciation)

    def __init__(self, word: str, meaning: str, example: str, date: datetime, _class=0,
                 last_changes_of_class=(datetime.date.today() - datetime.timedelta(days=1)),
                 when_becoming_5=(datetime.date(2222, 2, 2)), recalling=0, index1=-1,
                 how_many_times_did_I_recalle_word=0):
        self.__word = word
        self.__meaning = meaning
        self.__example = example
        self.__class = _class
        self.__date = date
        self.__last_changes_of_class = last_changes_of_class
        self.when_becoming_5 = when_becoming_5
        self.recalling = recalling
        self.index1 = index1
        self.how_many_times_did_I_recalle_word = how_many_times_did_I_recalle_word
        self.time_for_recalling = 0
        # result can be forgotten, remembered, average, not_recalled
        self.result = 'average'

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
        boolean = True
        # there is a problem with version or something.
        self.how_many_times_did_I_recalle_word += 1
        Word.all_words_in_file[self.index1].time_for_recalling += math.ceil(
            (datetime.datetime.now() - timee).total_seconds())
        if self.__last_changes_of_class != datetime.date.today():
            boolean = False
            if self.permission_for_changing_class:
                if value > 3:
                    if self.__class != 5:
                        if self.__class + 1 == 5:
                            self.when_becoming_5 = datetime.date.today()
                        self.__class += 1
                        self.result = 'remembered'
                elif value < 3:
                    if self.__class != 0:
                        self.__class -= 1
                        self.result = 'forgotten'
                    if value == 1:
                        Word.deck.append(Word.deck[index_current_word])
                else:
                    self.result = 'average'
                self.permission_for_changing_class = False
            self.__last_changes_of_class = datetime.date.today()
            if self.recalling != 0:
                self.recalling -= 1
            elif self.__class == 5 and self.recalling == 0:
                self.recalling = random.randrange(3, 6)
        if boolean:
            if value > 3:
                self.result = 'remembered'
            elif value < 3:
                self.result = 'forgotten'
                if self.__class >= 1:
                    self.__class -= 1

    @property
    def class_changes(self):
        return self.__last_changes_of_class

    @class_changes.getter
    def class_changes(self):
        return self.__last_changes_of_class

    @class_changes.setter
    def class_changes(self, value: int):
        self.__last_changes_of_class = value

    @property
    def current(self):
        if self.word_showing:
            return self.__word
        if self.meaning_showing:
            return self.__meaning
        if self.example_showing:
            return self.__example


try:
    Word.reading_from_file()
except PermissionError:
    print('PermissionError, it seems that you forgot to close the excel file and we cannot approach it.')
    print('just close the file.')
screen.fill(white)
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

# all the buttons
N = 30
again_button = Button(white, 0 * X // 10 + 430, Y - N, text='again')
hard_button = Button(white, X // 10 + 400, Y - N, text='hard')
normal_button = Button(white, 2 * X // 10 + 430, Y - N, text='normal')
nice_button = Button(white, 3 * X // 10 + 497, Y - N, text='nice')
impressive_button = Button(white, 4 * X // 10 + 440, Y - N, text='impressive')
back_card_button = Button(white, 10, Y - N, text='previous card')
next_card_button = Button(white, 1500, Y - N, text='next card')
word_button = Button(white, 600, Y - 4 * N, text='word')
meaning_button = Button(white, 753, Y - 4 * N, text='meaning')
example_button = Button(white, 972, Y - 4 * N, text='example')
button_list.append(again_button)
button_list.append(hard_button)
button_list.append(normal_button)
button_list.append(nice_button)
button_list.append(impressive_button)
button_list.append(back_card_button)
button_list.append(next_card_button)
button_list.append(word_button)
button_list.append(meaning_button)
button_list.append(example_button)
timee = datetime.datetime.now()
try:
    start = False
    index_current_word = 0
    max_index_current_word = len(Word.deck) - 1
    draw = True
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    try:
                        Word.save_changes()

                    except PermissionError:
                        print(
                            'PermissionError, it seems that you forgot to close the excel file and we cannot approach'
                            ' it.')
                        print('just close the file.')
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position_ = pygame.mouse.get_pos()
                    for button in button_list:
                        if button.where_clicked(position_):
                            if button.text == 'again':
                                Word.all_words_in_file[Word.deck[index_current_word].index1].class0 = 1
                                index_current_word += 1
                            elif button.text == 'hard':
                                Word.all_words_in_file[Word.deck[index_current_word].index1].class0 = 2
                                index_current_word += 1
                            elif button.text == 'normal':
                                Word.all_words_in_file[Word.deck[index_current_word].index1].class0 = 3
                                index_current_word += 1
                            elif button.text == 'nice':
                                Word.all_words_in_file[Word.deck[index_current_word].index1].class0 = 4
                                index_current_word += 1
                            elif button.text == 'impressive':
                                Word.all_words_in_file[Word.deck[index_current_word].index1].class0 = 4
                                index_current_word += 1
                            elif button.text == 'previous card':
                                index_current_word -= 1
                            elif button.text == 'next card':
                                index_current_word += 1
                            elif button.text == 'word':
                                Word.deck[index_current_word].switch(word=True)
                            elif button.text == 'meaning':
                                Word.deck[index_current_word].switch(meaning=True)
                            elif button.text == 'example':
                                Word.deck[index_current_word].switch(example=True)
                            elif button.text == 'pronunciation':
                                Word.pronunciation(Word.deck[index_current_word])
                            break
                    draw = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_f:
                        Word.deck[index_current_word].switch(word=True)
                    elif event.key == pygame.K_d:
                        Word.deck[index_current_word].switch(meaning=True)
                    elif event.key == pygame.K_s:
                        Word.deck[index_current_word].switch(example=True)
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RIGHT:
                        index_current_word += 1
                    elif event.key == pygame.K_c or event.key == pygame.K_x:
                        Word.pronunciation(Word.deck[index_current_word])
                    elif event.key == pygame.K_LEFT:
                        index_current_word -= 1
                    # 1 - do not remember
                    # 2 - hard
                    # 3 - normal
                    # 4 - nice
                    # 5 - very impressive
                    elif event.key == pygame.K_1:
                        Word.all_words_in_file[Word.deck[index_current_word].index1].class0 = 1
                        index_current_word += 1
                    elif event.key == pygame.K_2:
                        Word.all_words_in_file[Word.deck[index_current_word].index1].class0 = 2
                        index_current_word += 1
                    elif event.key == pygame.K_3:
                        Word.all_words_in_file[Word.deck[index_current_word].index1].class0 = 3
                        index_current_word += 1
                    elif event.key == pygame.K_4:
                        Word.all_words_in_file[Word.deck[index_current_word].index1].class0 = 4
                        index_current_word += 1
                    elif event.key == pygame.K_5:
                        Word.all_words_in_file[Word.deck[index_current_word].index1].class0 = 5
                        index_current_word += 1
                    elif event.key == pygame.K_0:
                        if index_current_word + 10 <= max_index_current_word:
                            index_current_word += 10
                        else:
                            screen.fill(white)
                            Word('warning: you can not move further with key 0, you reached the end of the list', '',
                                 '',
                                 datetime.date.today(), 0).show()
                            pygame.display.update()
                            pygame.time.wait(1500)
                    draw = True
                if draw:
                    timee = datetime.datetime.now()
                    screen.fill(white)
                    Word.deck[index_current_word].show()
                    for button in button_list:
                        button.draw(screen)

                    count = 0
                    id = 0
                    for index, button in enumerate(button_list):
                        if button.text == 'pronunciation':
                            count += 1
                            id = index
                    if count == 2:
                        button_list.pop(id)
                    pygame.display.update()
                    draw = False
    except IndexError:
        try:
            Word.save_changes()
        except PermissionError:
            print('PermissionError, it seems that you forgot to close the excel file and we cannot approach it.')
            print('just close the file.')
        pygame.quit()
        quit()
except ValueError:
    print('you did not end lesson, values were not saved.')
pygame.quit()
quit()
