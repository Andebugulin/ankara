import datetime
import pygame
import pandas as pd
import random
from gtts import gTTS
import time
import os

language = 'en-us'
white = '#FBFBF8'

green = (0, 255, 0)
blue = (0, 0, 128)
black = (25, 25, 25)

Days_full_of_relax_if_class_is_5 = 3

pygame.init()
X, Y = 1700, 900
screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption('You can bear it, I believe in you')

# File paths
excel_file = 'capture.xlsx'
csv_file = 'capture.csv'
button_list = []

class Button:
    def __init__(self, color, x, y, text='', font_size=50):
        self.color = color
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size
        self.width = 0
        self.height = 0

    def draw(self, display_drawing):
        font = pygame.font.SysFont('Helvetica', self.font_size)
        text = font.render(self.text, True, (0, 0, 0))
        self.width, self.height = text.get_size()
        display_drawing.blit(text, (self.x + 10, self.y - self.height // 2))
        pygame.draw.rect(display_drawing, black, (self.x, self.y - self.height // 2, self.width + 20, self.height + 20), 4)

    def where_clicked(self, pos):
        if (pos[0] > self.x) and (pos[0] < self.x + self.width + 20):
            if (pos[1] > self.y - self.height // 2) and (pos[1] < self.y + self.height // 2):
                return True
        return False

class Word:
    all_words_in_file = []
    screen = screen
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
    def read_file():
        if os.path.exists(excel_file):
            data = pd.read_excel(excel_file, index_col=0, parse_dates=True)
        elif os.path.exists(csv_file):
            data = pd.read_csv(csv_file, index_col=0, parse_dates=True)
        else:
            raise FileNotFoundError("No input file found.")

        data['last_changes_of_class'] = data['last_changes_of_class'].fillna(
            (datetime.date.today() - datetime.timedelta(days=1)))
        data['classes'] = data['classes'].fillna(0)
        data['date'] = data['date'].fillna(datetime.date.today())
        data['date_becoming'] = data['date_becoming'].fillna(datetime.date(2222, 2, 2))
        data['recalling'] = data['recalling'].fillna(0)
        Word.save_file(data)  # Save to both Excel and CSV
        # initialization of objects
        for index, date_word_meaning_ex in data.iterrows():
            word_meaning_ex = [i.strip() for i in date_word_meaning_ex.tolist()[1:-4]]
            date = date_word_meaning_ex.tolist()[0]
            _class = date_word_meaning_ex.tolist()[-4]
            last_changes_of_class = date_word_meaning_ex.tolist()[-3]
            date_becoming = date_word_meaning_ex[-2]
            recalling = date_word_meaning_ex[-1]
            object0 = Word(word_meaning_ex[0], word_meaning_ex[1], word_meaning_ex[2], date, _class,
                           last_changes_of_class, date_becoming, recalling)
            Word.all_words_in_file.append(object0)
            if _class < 5:
                Word.deck_without_reverse_cards.append(object0)
                Word.deck_without_shuffle.append(object0)
                Word.deck_without_shuffle.append(
                    Word(word_meaning_ex[1], word_meaning_ex[0], word_meaning_ex[2], date, _class,
                         last_changes_of_class, date_becoming, recalling))
            elif recalling == 0:
                if random.uniform(0, 1) < 0.5:
                    object0 = Word(word_meaning_ex[1], word_meaning_ex[0], word_meaning_ex[2], date, _class,
                                   last_changes_of_class, date_becoming, recalling)
                Word.deck_without_shuffle.append(object0)
                Word.deck_without_reverse_cards.append(object0)
        for word_not_shown in Word.all_words_in_file:
            for word_shown in Word.deck_without_reverse_cards:
                if word_not_shown.word == word_shown.word:
                    break
            else:
                if word_not_shown.class_changes != datetime.date.today():
                    word_not_shown.class_changes = datetime.date.today()
                    word_not_shown.recalling -= 1
        time.sleep(0.001)

    @staticmethod
    def save_file(data=None):
        if data is None:
            classes = []
            classes_changes = []
            data_becoming = []
            recalling = []
            for element in Word.all_words_in_file:
                classes.append(element.class0)
                classes_changes.append(element.class_changes)
                data_becoming.append(element.when_becoming_5)
                recalling.append(element.recalling)
            data = pd.read_excel(excel_file, parse_dates=True, index_col=0)
            data['classes'] = classes
            data['last_changes_of_class'] = classes_changes
            data['date_becoming'] = data_becoming
            data['recalling'] = recalling
        data.to_excel(excel_file)
        data.to_csv(csv_file)

    @staticmethod
    def rendering(message: str, text: str, position, font_size=70):
        if len(button_list) > 1:
            button_list.pop(0)
        font = pygame.font.SysFont('Helvetica', font_size)
        x, y = position

        def render_paragraph(paragraph, x, y):
            words = paragraph.split(' ')
            space = font.size(' ')[0]
            for word in words:
                word_surface = font.render(word, True, black)
                word_wid, word_hei = word_surface.get_size()
                if x + word_wid >= X:
                    x = position[0]
                    y += word_hei
                Word.screen.blit(word_surface, (x, y))
                x += word_wid + space
            return position[0], y + word_hei + 5  # Reset x to the original position, reduced space between lines

        lines = message.split('\n')
        for line in lines:
            x, y = render_paragraph(line, x, y)

        y += 20  # Increased space between text and pronunciation button

        lines = text.split('\n')
        for line in lines:
            x, y = render_paragraph(line, x, y)

        button_pronunciation = Button(white, 10, y + 30, text='pronunciation', font_size=font_size // 2)
        button_list.insert(0, button_pronunciation)

    def __init__(self, word: str, meaning: str, example: str, date: datetime, _class=0,
                 last_changes_of_class=(datetime.date.today() - datetime.timedelta(days=1)),
                 when_becoming_5=(datetime.date(2222, 2, 2)), recalling=0):
        self.__word = word
        self.__meaning = meaning
        self.__example = example
        self.__class = _class
        self.__date = date
        self.__last_changes_of_class = last_changes_of_class
        self.when_becoming_5 = when_becoming_5
        self.recalling = recalling
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
        if self.__last_changes_of_class != datetime.date.today():
            if self.permission_for_changing_class:
                if value > 3:
                    if self.__class != 5:
                        if self.__class + 1 == 5:
                            self.when_becoming_5 = datetime.date.today()
                        self.__class += 1
                elif value < 3:
                    if self.__class != 0:
                        self.__class -= 1
                    Word.deck.append(Word.deck[index_current_word])
                else:
                    pass
                self.permission_for_changing_class = False
            self.__last_changes_of_class = datetime.date.today()
            if self.__class == 5 and self.recalling == 0:
                self.recalling = random.randrange(3, 6)
            elif self.recalling != 0:
                self.recalling -= 1

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
    Word.read_file()
except PermissionError:
    print('PermissionError, it seems that you forgot to close the excel or csv file and we cannot access it.')
    print('Just close the file.')
screen.fill(white)
Word.rendering('hello',
               '''for start press almost random key :^)\n
                  Instructions:\n
                  Tool for learning words\n
                   ---------------------------------------------------------------------------------\n
                  use short_keys:\n
                  keys: Ff(word) - Dd(meaning) - Ss(example) - Space(for the next word) -\n
                  n - (for the next word) -\n
                  p - (for the previous word)\n
                  --------------------------------------------------------------------------\n
                  evaluation:\n
                              h do not remember -\n
                              j hard -\n
                              k normal -\n
                              l nice -\n
                              i very impressive\n
                  --------------------------------------------------------------------------\n
                  additional functions:\n
                  a - Play pronunciation of the word\n
                  0 - Skip 10 words forward\n
               ''',
               (20, 20), font_size=15)
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

N = 30
again_button = Button(white, 0 * X // 10 + 430, Y - N, text='again', font_size=30)
hard_button = Button(white, X // 10 + 400, Y - N, text='hard', font_size=30)
normal_button = Button(white, 2 * X // 10 + 430, Y - N, text='normal', font_size=30)
nice_button = Button(white, 3 * X // 10 + 497, Y - N, text='nice', font_size=30)
impressive_button = Button(white, 4 * X // 10 + 440, Y - N, text='impressive', font_size=30)
back_card_button = Button(white, 10, Y - N, text='previous card', font_size=30)
next_card_button = Button(white, 1500, Y - N, text='next card', font_size=30)
word_button = Button(white, 600, Y - 4 * N, text='word', font_size=30)
meaning_button = Button(white, 753, Y - 4 * N, text='meaning', font_size=30)
example_button = Button(white, 972, Y - 4 * N, text='example', font_size=30)
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
                        Word.save_file()
                    except PermissionError:
                        print(
                            'PermissionError, it seems that you forgot to close the excel or csv file and we cannot access it.')
                        print('Just close the file.')
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position_ = pygame.mouse.get_pos()
                    for button in button_list:
                        if button.where_clicked(position_):
                            if button.text == 'again':
                                Word.deck[index_current_word].class0 = 1
                                index_current_word += 1
                            elif button.text == 'hard':
                                Word.deck[index_current_word].class0 = 2
                                index_current_word += 1
                            elif button.text == 'normal':
                                Word.deck[index_current_word].class0 = 3
                                index_current_word += 1
                            elif button.text == 'nice':
                                Word.deck[index_current_word].class0 = 4
                                index_current_word += 1
                            elif button.text == 'impressive':
                                Word.deck[index_current_word].class0 = 5
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
                    if event.key == pygame.K_n:
                        index_current_word += 1
                    elif event.key == pygame.K_p:
                        index_current_word -= 1
                    elif event.key == pygame.K_h:
                        Word.deck[index_current_word].class0 = 1
                        index_current_word += 1
                    elif event.key == pygame.K_j:
                        Word.deck[index_current_word].class0 = 2
                        index_current_word += 1
                    elif event.key == pygame.K_k:
                        Word.deck[index_current_word].class0 = 3
                        index_current_word += 1
                    elif event.key == pygame.K_l:
                        Word.deck[index_current_word].class0 = 4
                        index_current_word += 1
                    elif event.key == pygame.K_i:
                        Word.deck[index_current_word].class0 = 5
                        index_current_word += 1
                    elif event.key == pygame.K_0:
                        if index_current_word + 10 <= max_index_current_word:
                            index_current_word += 10
                        else:
                            screen.fill(white)
                            Word('Warning: you cannot move further with key 0, you reached the end of the list', '', '',
                                 datetime.date.today(), 0).show()
                            pygame.display.update()
                            pygame.time.wait(1500)
                    elif event.key == pygame.K_f:
                        Word.deck[index_current_word].switch(word=True)
                    elif event.key == pygame.K_d:
                        Word.deck[index_current_word].switch(meaning=True)
                    elif event.key == pygame.K_s:
                        Word.deck[index_current_word].switch(example=True)
                    elif event.key == pygame.K_a:
                        Word.pronunciation(Word.deck[index_current_word])
                    draw = True
                if draw:
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
            Word.save_file()
        except PermissionError:
            print('PermissionError, it seems that you forgot to close the excel or csv file and we cannot access it.')
            print('Just close the file.')
        pygame.quit()
        quit()
except ValueError:
    print('You did not end lesson, values were not saved.')
pygame.quit()
quit()
