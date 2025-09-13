import datetime
import pygame
import pandas as pd
import random
from gtts import gTTS
import time
import os
import json
from pathlib import Path
import shutil
from typing import List, Dict, Optional
from langdetect import detect

# Constants
LANGUAGE = 'en'  # Default language
SUPPORTED_LANGUAGES = {
    'en': 'en',
    'es': 'es', 
    'fr': 'fr',
    'de': 'de',
    'it': 'it',
    'pt': 'pt',
    'ru': 'ru',
    'ja': 'ja',
    'ko': 'ko',
    'zh': 'zh'
}

# Language detection to gTTS mapping
LANG_DETECT_TO_GTTS = {
    'en': 'en',
    'ru': 'ru',
    'es': 'es',
    'fr': 'fr',
    'de': 'de',
    'it': 'it',
    'pt': 'pt',
    'ja': 'ja',
    'ko': 'ko',
    'zh-cn': 'zh',
    'zh': 'zh'
}

WHITE = '#FBFBF8'
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
BLACK = (25, 25, 25)
DAYS_FULL_OF_RELAX_IF_CLASS_IS_5 = 3

# File paths
DATA_DIR = Path("flashcard_data")
DATA_DIR.mkdir(exist_ok=True)
CSV_FILE = DATA_DIR / 'words.csv'
BACKUP_DIR = DATA_DIR / 'backups'
BACKUP_DIR.mkdir(exist_ok=True)
CONFIG_FILE = DATA_DIR / 'config.json'

class DataManager:
    """Handles all file operations and data management"""
    
    def __init__(self):
        self.config = self.load_config()
        
    def load_config(self) -> Dict:
        """Load configuration settings"""
        default_config = {
            "auto_backup": True,
            "backup_interval_days": 7,
            "max_backups": 10,
            "last_backup": None
        }
        
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except:
                pass
        
        self.save_config(default_config)
        return default_config
    
    def save_config(self, config: Dict):
        """Save configuration settings"""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2, default=str)
    
    def create_backup(self):
        """Create a backup of the current data"""
        if not CSV_FILE.exists():
            return
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = BACKUP_DIR / f"words_backup_{timestamp}.csv"
        
        try:
            shutil.copy2(CSV_FILE, backup_file)
            print(f"Backup created: {backup_file}")
            
            # Clean old backups
            self.cleanup_old_backups()
            
            # Update config
            self.config['last_backup'] = timestamp
            self.save_config(self.config)
            
        except Exception as e:
            print(f"Backup failed: {e}")
    
    def cleanup_old_backups(self):
        """Remove old backup files"""
        backups = sorted(BACKUP_DIR.glob("words_backup_*.csv"))
        max_backups = self.config.get('max_backups', 10)
        
        if len(backups) > max_backups:
            for backup in backups[:-max_backups]:
                backup.unlink()
    
    def should_create_backup(self) -> bool:
        """Check if backup should be created"""
        if not self.config['auto_backup']:
            return False
            
        last_backup = self.config.get('last_backup')
        if not last_backup:
            return True
            
        try:
            last_date = datetime.datetime.strptime(last_backup, "%Y%m%d_%H%M%S")
            days_since = (datetime.datetime.now() - last_date).days
            return days_since >= self.config.get('backup_interval_days', 7)
        except:
            return True
        
    def get_pronunciation_language(self) -> str:
        """Get current pronunciation language"""
        return self.config.get('pronunciation_language', 'en')
    
    def detect_language(self, text: str) -> str:
        """Detect language based on character sets"""
        try:
            clean_text = text.strip()
            if len(clean_text) < 1:
                return self.get_pronunciation_language()
            
            # Count characters by script
            cyrillic_count = 0
            latin_count = 0
            cjk_count = 0
            
            for char in clean_text:
                if '\u0400' <= char <= '\u04FF':  # Cyrillic
                    cyrillic_count += 1
                elif '\u4E00' <= char <= '\u9FFF' or '\u3400' <= char <= '\u4DBF':  # Chinese
                    cjk_count += 1
                elif '\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF':  # Japanese
                    cjk_count += 1
                elif char.isalpha():  # Latin and other alphabetic
                    latin_count += 1
            
            # Determine language based on character dominance
            total_chars = cyrillic_count + latin_count + cjk_count
            if total_chars == 0:
                return self.get_pronunciation_language()
            
            if cyrillic_count / total_chars > 0.3:
                return 'ru'
            elif cjk_count / total_chars > 0.3:
                return 'zh'  
            else:
                return 'en'  # Default to English for Latin script
                
        except Exception as e:
            print(f"Language detection error: {e}")
            return self.get_pronunciation_language()

    def set_pronunciation_language(self, lang_code: str):
        """Set pronunciation language"""
        if lang_code in SUPPORTED_LANGUAGES:
            self.config['pronunciation_language'] = lang_code
            self.save_config(self.config)
            return True
        return False

    def list_supported_languages(self) -> Dict[str, str]:
        """Return supported languages with names"""
        lang_names = {
            'en': 'English',
            'es': 'Spanish', 
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese'
        }
        return {code: lang_names.get(code, code.upper()) for code in SUPPORTED_LANGUAGES}

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
        text = font.render(self.text, True, BLACK)
        self.width, self.height = text.get_size()
        display_drawing.blit(text, (self.x + 10, self.y - self.height // 2))
        pygame.draw.rect(display_drawing, BLACK, 
                        (self.x, self.y - self.height // 2, self.width + 20, self.height + 20), 4)

    def where_clicked(self, pos):
        return (self.x < pos[0] < self.x + self.width + 20 and 
                self.y - self.height // 2 < pos[1] < self.y + self.height // 2)

class Word:
    """Represents a single flashcard with enhanced data collection"""
    
    def __init__(self, word: str, meaning: str, example: str, date: datetime.date = None,
                 class_level: int = 0, last_changes_of_class: datetime.date = None,
                 when_becoming_5: datetime.date = None, recalling: int = 0,
                 study_sessions: int = 0, total_study_time: float = 0.0,
                 correct_answers: int = 0, total_answers: int = 0):
        
        self.word = word
        self.meaning = meaning
        self.example = example
        self.date = date or datetime.date.today()
        self.class_level = class_level
        self.last_changes_of_class = last_changes_of_class or (datetime.date.today() - datetime.timedelta(days=1))
        self.when_becoming_5 = when_becoming_5 or datetime.date(2222, 2, 2)
        self.recalling = recalling
        
        # Enhanced data collection fields
        self.study_sessions = study_sessions
        self.total_study_time = total_study_time
        self.correct_answers = correct_answers
        self.total_answers = total_answers
        self.session_start_time = None
        
        # Display state
        self.word_showing = True
        self.meaning_showing = False
        self.example_showing = False
        self.permission_for_changing_class = True
    
    def start_session(self):
        """Start timing a study session"""
        self.session_start_time = time.time()
    
    def end_session(self, correct: bool = None):
        """End timing a study session and record data"""
        if self.session_start_time:
            session_time = time.time() - self.session_start_time
            self.total_study_time += session_time
            self.study_sessions += 1
            
            if correct is not None:
                self.total_answers += 1
                if correct:
                    self.correct_answers += 1
            
            self.session_start_time = None
    
    def get_accuracy(self) -> float:
        """Calculate accuracy percentage"""
        if self.total_answers == 0:
            return 0.0
        return (self.correct_answers / self.total_answers) * 100
    
    def get_average_study_time(self) -> float:
        """Calculate average study time per session"""
        if self.study_sessions == 0:
            return 0.0
        return self.total_study_time / self.study_sessions
    
    def switch(self, word=False, meaning=False, example=False):
        """Switch display mode"""
        self.word_showing = word
        self.meaning_showing = meaning
        self.example_showing = example

    def get_current_text(self) -> str:
        """Get currently displayed text"""
        if self.word_showing:
            return self.word
        elif self.meaning_showing:
            return self.meaning
        else:
            return self.example
    
    def get_current_label(self) -> str:
        """Get label for currently displayed content"""
        if self.word_showing:
            return "word:"
        elif self.meaning_showing:
            return "meaning:"
        else:
            return "example:"
    
    def update_class(self, rating: int):
        """Update class level based on rating (1-5)"""
        if self.last_changes_of_class != datetime.date.today():
            if self.permission_for_changing_class:
                if rating > 3:
                    if self.class_level < 5:
                        if self.class_level + 1 == 5:
                            self.when_becoming_5 = datetime.date.today()
                        self.class_level += 1
                elif rating < 3:
                    if self.class_level > 0:
                        self.class_level -= 1
                
                self.permission_for_changing_class = False
                self.end_session(correct=(rating >= 3))
            
            self.last_changes_of_class = datetime.date.today()
            
            if self.class_level == 5 and self.recalling == 0:
                self.recalling = random.randrange(3, 6)
            elif self.recalling > 0:
                self.recalling -= 1
    
    def to_dict(self) -> Dict:
        """Convert word to dictionary for CSV storage"""
        return {
            'word': self.word,
            'meaning': self.meaning,
            'example': self.example,
            'date': self.date,
            'class_level': self.class_level,
            'last_changes_of_class': self.last_changes_of_class,
            'when_becoming_5': self.when_becoming_5,
            'recalling': self.recalling,
            'study_sessions': self.study_sessions,
            'total_study_time': self.total_study_time,
            'correct_answers': self.correct_answers,
            'total_answers': self.total_answers
        }

class WordManager:
    """Manages collection of words and file operations"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.all_words: List[Word] = []
        self.deck: List[Word] = []
        self.deck_without_reverse: List[Word] = []
        
        # Check if backup is needed
        if self.data_manager.should_create_backup():
            self.data_manager.create_backup()
    
    def load_words(self):
        """Load words from CSV file with improved performance"""
        if not CSV_FILE.exists():
            print(f"No data file found at {CSV_FILE}")
            return
        
        try:
            # Use chunking for large files
            chunk_size = 1000
            chunks = []
            

            date_columns = []
            if 'date' in pd.read_csv(CSV_FILE, nrows=1).columns:
                date_columns.append('date')
            if 'last_changes_of_class' in pd.read_csv(CSV_FILE, nrows=1).columns:
                date_columns.append('last_changes_of_class')
            if 'when_becoming_5' in pd.read_csv(CSV_FILE, nrows=1).columns:
                date_columns.append('when_becoming_5')

            for chunk in pd.read_csv(CSV_FILE, chunksize=chunk_size, parse_dates=date_columns):                
                chunks.append(chunk)
            
            if not chunks:
                return
                
            data = pd.concat(chunks, ignore_index=True)
            
            # Check required columns
            required_columns = ['word', 'meaning', 'example']
            for col in required_columns:
                if col not in data.columns:
                    raise ValueError(f"Required column '{col}' not found in CSV")

            # Add missing optional columns
            optional_defaults = {
                'class_level': 0,
                'recalling': 0,
                'study_sessions': 0,
                'total_study_time': 0.0,
                'correct_answers': 0,
                'total_answers': 0,
                'date': datetime.date.today(),
                'last_changes_of_class': datetime.date.today() - datetime.timedelta(days=1),
                'when_becoming_5': datetime.date(2222, 2, 2)
            }

            for col, default_val in optional_defaults.items():
                if col not in data.columns:
                    data[col] = default_val
                else:
                    data[col] = data[col].fillna(default_val)
            
            # Create word objects
            self.all_words = []
            for _, row in data.iterrows():
                word = Word(
                    word=row['word'],
                    meaning=row['meaning'],
                    example=row['example'],
                    date=row['date'].date() if hasattr(row['date'], 'date') else row['date'],
                    class_level=int(row['class_level']),
                    last_changes_of_class=row['last_changes_of_class'].date() if hasattr(row['last_changes_of_class'], 'date') else row['last_changes_of_class'],
                    when_becoming_5=row['when_becoming_5'].date() if hasattr(row['when_becoming_5'], 'date') else row['when_becoming_5'],
                    recalling=int(row['recalling']),
                    study_sessions=int(row.get('study_sessions', 0)),
                    total_study_time=float(row.get('total_study_time', 0.0)),
                    correct_answers=int(row.get('correct_answers', 0)),
                    total_answers=int(row.get('total_answers', 0))
                )
                self.all_words.append(word)
            
            print(f"Loaded {len(self.all_words)} words")
            
        except Exception as e:
            print(f"Error loading words: {e}")
    
    def save_words(self):
        """Save words to CSV file with improved performance"""
        if not self.all_words:
            return
        
        try:
            # Convert to DataFrame efficiently
            data_list = [word.to_dict() for word in self.all_words]
            data = pd.DataFrame(data_list)
            
            # Save to CSV only (no Excel)
            data.to_csv(CSV_FILE, index=False)
            print(f"Saved {len(self.all_words)} words to {CSV_FILE}")
            
        except Exception as e:
            print(f"Error saving words: {e}")
    
    def create_deck(self):
        """Create study deck with optimized shuffling"""
        DAILY_LIMITS = {
            0: 20,  # Max 20 new cards (class 0) per day
            1: 30,  # Max 30 class 1 cards per day
            2: 40,  # Max 40 class 2 cards per day
            3: 50,  # Max 50 class 3 cards per day
            4: 60   # Max 60 class 4 cards per day
        }

        self.deck = []
        self.deck_without_reverse = []
        
        # Group words efficiently
        words_by_class = {}
        for word in self.all_words:
            class_level = word.class_level
            if class_level not in words_by_class:
                words_by_class[class_level] = []
            words_by_class[class_level].append(word)
        
        # Process each class level
        for class_level, words in words_by_class.items():
            if class_level < 5:
                # Apply daily limits
                limit = DAILY_LIMITS.get(class_level, len(words))
                limited_words = words[:limit] if len(words) > limit else words
                
                # Add forward and reverse cards for limited words
                for word in limited_words:
                    self.deck_without_reverse.append(word)
                    self.deck.append(word)
                    
                    # Create reverse card
                    reverse_word = Word(
                        word=word.meaning,
                        meaning=word.word,
                        example=word.example,
                        date=word.date,
                        class_level=word.class_level,
                        last_changes_of_class=word.last_changes_of_class,
                        when_becoming_5=word.when_becoming_5,
                        recalling=word.recalling
                    )
                    self.deck.append(reverse_word)
            else:
                # For class 5, add only if recalling > 0 or randomly
                for word in words:
                    if word.recalling == 0:
                        if random.random() < 0.5:  # 50% chance
                            self.deck.append(word)
                            self.deck_without_reverse.append(word)
                    else:
                        self.deck.append(word)
                        self.deck_without_reverse.append(word)
        
        # Shuffle deck in groups of 10 for better distribution
        self.shuffle_deck()
        
        # Update recalling for words not in deck
        self.update_missing_words()
    
    def shuffle_deck(self):
        """Shuffle deck in groups for better word distribution"""
        if not self.deck:
            return
            
        # Group by 10s and shuffle within groups
        shuffled_deck = []
        group_size = 10
        
        for i in range(0, len(self.deck), group_size):
            group = self.deck[i:i + group_size]
            random.shuffle(group)
            shuffled_deck.extend(group)
        
        self.deck = shuffled_deck
    
    def update_missing_words(self):
        """Update recalling for words not in current deck"""
        deck_words = {word.word for word in self.deck_without_reverse}
        
        for word in self.all_words:
            if word.word not in deck_words:
                if word.last_changes_of_class != datetime.date.today():
                    word.last_changes_of_class = datetime.date.today()
                    word.recalling = max(0, word.recalling - 1)



class FlashcardApp:
    """Main application class"""
    
    def __init__(self):
        pygame.init()
        self.X, self.Y = 1700, 900
        self.screen = pygame.display.set_mode((self.X, self.Y))
        pygame.display.set_caption('Enhanced Flashcard Learning Tool')
        
        self.word_manager = WordManager()
        self.buttons = []
        self.current_word_index = 0
        self.max_index = 0
        
        # Statistics
        self.session_stats = {
            'cards_studied': 0,
            'correct_answers': 0,
            'start_time': time.time()
        }

        self.review_queue = []  # Cards to review again
    
    def setup_buttons(self):
        """Create UI buttons"""
        N = 30
        self.buttons = [
            Button(WHITE, 0 * self.X // 10 + 430, self.Y - N, 'again', 30),
            Button(WHITE, self.X // 10 + 400, self.Y - N, 'hard', 30),
            Button(WHITE, 2 * self.X // 10 + 430, self.Y - N, 'normal', 30),
            Button(WHITE, 3 * self.X // 10 + 497, self.Y - N, 'nice', 30),
            Button(WHITE, 4 * self.X // 10 + 440, self.Y - N, 'impressive', 30),
            Button(WHITE, 10, self.Y - N, 'previous card', 30),
            Button(WHITE, 1500, self.Y - N, 'next card', 30),
            Button(WHITE, 600, self.Y - 4 * N, 'word', 30),
            Button(WHITE, 753, self.Y - 4 * N, 'meaning', 30),
            Button(WHITE, 972, self.Y - 4 * N, 'example', 30),
        ]
    
    def cycle_language(self, direction: int):
        """Cycle through supported languages"""
        languages = list(SUPPORTED_LANGUAGES.keys())
        current_lang = self.word_manager.data_manager.get_pronunciation_language()
        
        try:
            current_index = languages.index(current_lang)
            new_index = (current_index + direction) % len(languages)
            new_lang = languages[new_index]
            
            if self.word_manager.data_manager.set_pronunciation_language(new_lang):
                lang_names = self.word_manager.data_manager.list_supported_languages()
                print(f"Language changed to: {lang_names[new_lang]} ({new_lang})")
        except ValueError:
            # Fallback to English if current language not found
            self.word_manager.data_manager.set_pronunciation_language('en')
    
    def render_text(self, label: str, text: str, position, font_size=70):
        """Render text with word wrapping"""
        font = pygame.font.SysFont('Helvetica', font_size)
        x, y = position
        
        def render_paragraph(paragraph, x, y):
            words = paragraph.split(' ')
            space = font.size(' ')[0]
            for word in words:
                word_surface = font.render(word, True, BLACK)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= self.X:
                    x = position[0]
                    y += word_height
                self.screen.blit(word_surface, (x, y))
                x += word_width + space
            return position[0], y + word_height + 5
        
        # Render label
        lines = label.split('\n')
        for line in lines:
            x, y = render_paragraph(line, x, y)
        
        y += 20
        
        # Render text
        lines = text.split('\n')
        for line in lines:
            x, y = render_paragraph(line, x, y)
        
        # Add pronunciation button
        pronunciation_btn = Button(WHITE, 10, y + 30, 'pronunciation', font_size // 2)
        
        # Remove old pronunciation button and add new one
        self.buttons = [btn for btn in self.buttons if btn.text != 'pronunciation']
        self.buttons.append(pronunciation_btn)
    
    def play_pronunciation(self, word: Word):
        """Play pronunciation of current word with auto language detection"""
        try:
            text = word.get_current_text()
            
            # Auto-detect language
            detected_lang = self.word_manager.data_manager.detect_language(text)
            
            # Show detected language (optional - remove if too verbose)
            lang_names = self.word_manager.data_manager.list_supported_languages()
            detected_name = lang_names.get(detected_lang, detected_lang)
            print(f"Detected language: {detected_name} ({detected_lang})")
            
            tts = gTTS(text=text, lang=detected_lang, slow=False)
            tts.save("temp_audio.mp3")
            
            pygame.mixer.init()
            pygame.mixer.music.load('temp_audio.mp3')
            pygame.mixer.music.play()
            
            clock = pygame.time.Clock()
            while pygame.mixer.music.get_busy():
                pygame.event.poll()
                clock.tick(10)
            
            pygame.mixer.quit()
            os.remove('temp_audio.mp3')
            
        except Exception as e:
            print(f"Pronunciation failed: {e}")
    
    def show_instructions(self):
        """Display initial instructions"""
        self.screen.fill(WHITE)
        instructions = '''Enhanced Flashcard Learning Tool
        
Instructions:
• Learning tool with 3-sided flashcards (word, meaning, example)
• Data collection for AI research on memory patterns

Keyboard Shortcuts:
F - Show word    |    D - Show meaning    |    S - Show example
A - Pronunciation    |    N - Next card    |    P - Previous card
0 - Skip 10 cards forward
< - Previous language    |    > - Next language

Evaluation (affects learning algorithm):
H - Don't remember (1)    |    J - Hard (2)    |    K - Normal (3)
L - Nice (4)    |    I - Very impressive (5)

Features:
• Automatic backups    • Performance optimized for large datasets
• Enhanced data collection    • CSV-only storage

Press any key to start...'''
        
        self.render_text('', instructions, (20, 20), font_size=15)
        pygame.display.update()
    
    def run(self):
        """Main application loop"""
        try:
            self.word_manager.load_words()
            
            if not self.word_manager.all_words:
                print("No words found. Please add words to the CSV file first.")
                return
            
            self.setup_buttons()
            self.show_instructions()
            
            # Wait for start
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        waiting = False
            
            # Create study deck
            self.word_manager.create_deck()
            self.max_index = len(self.word_manager.deck) - 1
            
            if self.max_index < 0:
                print("No cards available for study.")
                return
            
            # Start first word session
            self.word_manager.deck[0].start_session()
            
            # Main game loop
            clock = pygame.time.Clock()
            running = True
            
            while running and self.current_word_index < self.max_index:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    
                    elif event.type == pygame.KEYDOWN:
                        running = self.handle_keyboard(event.key)
                    
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        running = self.handle_mouse_click(pygame.mouse.get_pos())
                
                self.draw_screen()
                pygame.display.update()
                clock.tick(60)  # Limit to 60 FPS
            
        except Exception as e:
            print(f"Application error: {e}")
        
        finally:
            self.cleanup()
    
    def handle_keyboard(self, key) -> bool:
        """Handle keyboard input"""
        if key == pygame.K_ESCAPE:
            return False
        
        current_word = self.word_manager.deck[self.current_word_index]
        
        # Navigation
        if key == pygame.K_n:
            self.next_card()
        elif key == pygame.K_p:
            self.previous_card()
        elif key == pygame.K_0:
            self.skip_forward(10)
        
        # Display modes
        elif key == pygame.K_f:
            current_word.switch(word=True)
        elif key == pygame.K_d:
            current_word.switch(meaning=True)
        elif key == pygame.K_s:
            current_word.switch(example=True)
        elif key == pygame.K_a:
            self.play_pronunciation(current_word)
        
        # Ratings
        elif key == pygame.K_h:
            self.rate_card(1)
        elif key == pygame.K_j:
            self.rate_card(2)
        elif key == pygame.K_k:
            self.rate_card(3)
        elif key == pygame.K_l:
            self.rate_card(4)
        elif key == pygame.K_i:
            self.rate_card(5)
        
        # Language cycling
        elif key == pygame.K_COMMA:  # '<' key - previous language
            self.cycle_language(-1)
        elif key == pygame.K_PERIOD:  # '>' key - next language  
            self.cycle_language(1)
        
        return True
    
    def handle_mouse_click(self, pos) -> bool:
        """Handle mouse clicks on buttons"""
        for button in self.buttons:
            if button.where_clicked(pos):
                if button.text in ['again', 'hard', 'normal', 'nice', 'impressive']:
                    rating_map = {'again': 1, 'hard': 2, 'normal': 3, 'nice': 4, 'impressive': 5}
                    self.rate_card(rating_map[button.text])
                elif button.text == 'previous card':
                    self.previous_card()
                elif button.text == 'next card':
                    self.next_card()
                elif button.text == 'word':
                    self.word_manager.deck[self.current_word_index].switch(word=True)
                elif button.text == 'meaning':
                    self.word_manager.deck[self.current_word_index].switch(meaning=True)
                elif button.text == 'example':
                    self.word_manager.deck[self.current_word_index].switch(example=True)
                elif button.text == 'pronunciation':
                    self.play_pronunciation(self.word_manager.deck[self.current_word_index])
                break
        return True
    
    def rate_card(self, rating: int):
        """Rate current card and move to next"""
        current_word = self.word_manager.deck[self.current_word_index]
        current_word.update_class(rating)
        
        # Add to review queue if rating < 3 (again/hard)
        if rating < 3:
            # Add back to deck after 5-10 cards
            review_position = min(self.current_word_index + random.randint(5, 10), len(self.word_manager.deck))
            self.review_queue.append((review_position, current_word))
        
        # Update session stats
        self.session_stats['cards_studied'] += 1
        if rating >= 3:
            self.session_stats['correct_answers'] += 1
        
        # Process review queue
        self.process_review_queue()
        
        self.next_card()

    def process_review_queue(self):
        """Insert review cards back into deck at appropriate positions"""
        for position, word in self.review_queue:
            if position <= self.current_word_index + 1:
                self.word_manager.deck.insert(self.current_word_index + 1, word)
                self.max_index += 1
        
        # Clear processed reviews
        self.review_queue = [item for item in self.review_queue if item[0] > self.current_word_index + 1]
    
    def next_card(self):
        """Move to next card"""
        if self.current_word_index < self.max_index:
            self.current_word_index += 1
            self.word_manager.deck[self.current_word_index].start_session()
        else:
            # End of deck reached
            return False
        return True
    
    def previous_card(self):
        """Move to previous card"""
        if self.current_word_index > 0:
            self.current_word_index -= 1
    
    def skip_forward(self, count: int):
        """Skip forward by count cards"""
        if self.current_word_index + count <= self.max_index:
            self.current_word_index += count
            self.word_manager.deck[self.current_word_index].start_session()
        else:
            # Show warning
            self.screen.fill(WHITE)
            self.render_text('Warning:', 'Cannot skip further - reached end of deck', (20, 20))
            pygame.display.update()
            pygame.time.wait(1500)
    
    def draw_screen(self):
        """Draw the current screen"""
        self.screen.fill(WHITE)
        
        if self.current_word_index <= self.max_index:
            current_word = self.word_manager.deck[self.current_word_index]
            label = current_word.get_current_label()
            text = current_word.get_current_text()
            
            # Show progress and stats
            progress = f"Card {self.current_word_index + 1}/{self.max_index + 1}"
            accuracy = self.session_stats['correct_answers'] / max(1, self.session_stats['cards_studied']) * 100
            stats = f"Session: {self.session_stats['cards_studied']} cards | Accuracy: {accuracy:.1f}%"
            
            self.render_text(f"{progress} | {stats}\n\n{label}", text, (20, 20))
            
            # Draw buttons
            for button in self.buttons:
                button.draw(self.screen)
    
    def cleanup(self):
        """Clean up and save data"""
        print("Saving data...")
        self.word_manager.save_words()
        
        # Show session summary
        total_time = time.time() - self.session_stats['start_time']
        accuracy = self.session_stats['correct_answers'] / max(1, self.session_stats['cards_studied']) * 100
        
        print(f"\nSession Summary:")
        print(f"Cards studied: {self.session_stats['cards_studied']}")
        print(f"Accuracy: {accuracy:.1f}%")
        print(f"Total time: {total_time:.1f} seconds")
        
        pygame.quit()

if __name__ == "__main__":
    app = FlashcardApp()
    app.run()