# Enhanced Flashcard Learning Tool - "Ankara"

<p align="center">
  <img src="./ankara.png" width="400px" alt="Enhanced Flashcard Learning Tool Logo">
</p>

<p align="center">
  <strong>An intelligent, data-driven vocabulary learning application with spaced repetition and comprehensive analytics</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square" alt="Platform Support">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">

</p>

---

## 🚀 Overview

`Ankara` is a next-generation vocabulary learning application that tries to combine proven educational techniques with modern data analytics. Unlike traditional flashcard applications, this tool features **three-sided cards** (word, meaning, example) and collects comprehensive learning data for AI research applications ( and this feature is completely for fun and experimental).

### 🎯 Key Innovation

While most flashcard tools limit you to two-sided cards, our application provides a unique **three-stage learning approach**:
1. **Word** → See the vocabulary term
2. **Example** → Context before definition (optional intermediate step)
3. **Meaning** → Final definition reveal

This progression mimics natural language acquisition and allows learners to build context before seeing direct translations, at least for me this approach helped and I like to think its better approach.

## ✨ Features

### 🧠 **Advanced Learning System**
- **Spaced Repetition Algorithm**: Intelligently schedules reviews based on your performance
- **Three-Sided Flashcards**: Word → Example → Meaning progression
- **Vim-Inspired Keybindings**: Efficient navigation for power users, plus helps you learning touch typing
- **Multi-Language Support**: Automatic language detection for pronunciation

### 📊 **Data Analytics & AI Integration**
- **Comprehensive Learning Metrics**: Track study time, accuracy, and progress patterns
- **Machine Learning Ready**: Generates datasets suitable for memory research
- **Performance Analytics**: Session statistics and long-term progress tracking
- **Export Capabilities**: Data ready for neural network training

### 🛡️ **Robust Data Management**
- **Automatic Backups**: Scheduled backups with configurable retention
- **CSV-Based Storage**: Lightweight, portable, and version-controllable
- **Data Recovery**: Built-in backup restoration system
- **Performance Optimized**: Handles large vocabularies efficiently

### 🎨 **User Experience**
- **Intuitive Interface**: Clean, distraction-free design
- **Real-Time Pronunciation**: Text-to-speech with automatic language detection
- **Progress Visualization**: Session stats and accuracy tracking
- **Responsive Controls**: Both keyboard and mouse support

## 🛠️ Installation

### Prerequisites

```bash
Python 3.8+
```

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Andebugulin/ankara.git
   cd ankara
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python ankara.py
   ```

### Dependencies

- `pygame` - GUI framework
- `pandas` - Data manipulation
- `gtts` - Text-to-speech functionality
- `pathlib` - Modern path handling
- `langdetect` - Language detection

## 📖 Usage Guide

### Initial Setup

1. **Prepare your vocabulary data** in CSV format:
   ```csv
   word,meaning,example
   serendipity,pleasant surprise,Finding that book was pure serendipity
   ephemeral,lasting very briefly,The ephemeral beauty of cherry blossoms
   ```

2. **Place the CSV file** in the application directory in flashcard_data/words.csv

3. **Launch the application** and follow the on-screen instructions

### Keyboard Controls

#### Navigation
- `N` - Next card
- `P` - Previous card  
- `0` - Skip 10 cards forward
- `<` - Switch language for pronunciation manually
- `>` - Switch language for pronunciation manually

#### Card Views
- `F` - Show word
- `D` - Show meaning
- `S` - Show example
- `A` - Play pronunciation (auto-detects language)

#### Evaluation (Spaced Repetition)
- `H` - Don't remember (1) 
- `J` - Hard (2)
- `K` - Normal (3)
- `L` - Nice (4)
- `I` - Very impressive (5)

#### System
- `ESC` - Save and exit

### Optimal Hand Positioning

For maximum efficiency, position your hands like this:

**Left Hand**: `A` `S` `D` `F` (ring → index fingers)  
**Right Hand**: `H` `J` `K` `L` (index → pinky fingers)

This Vim-inspired layout minimizes hand movement and maximizes learning speed.

## 📁 Project Structure

```
ankara.py                  # Main application script
requirements.txt          # Python dependencies
flashcard_data/
├── words.csv              # Main vocabulary database
├── config.json           # Application settings
└── backups/              # Automatic backup storage
    ├── words_backup_20241201_120000.csv
    └── words_backup_20241130_120000.csv
```

## 📊 Data Collection & AI Applications

### Learning Analytics

The application collects comprehensive learning metrics:

```python
# Per-word analytics
- study_sessions: int      # Times studied
- total_study_time: float  # Cumulative study time
- correct_answers: int     # Successful recalls
- total_answers: int       # Total attempts
- accuracy_rate: float     # Success percentage
- class_progression: list  # Spaced repetition history
```

### AI Research Applications

This data structure enables research into:
- **Memory retention patterns**
- **Optimal review scheduling**
- **Individual learning differences**
- **Vocabulary acquisition modeling**


## ⚙️ Configuration

### Backup Settings

Edit `flashcard_data/config.json`:

```json
{
  "auto_backup": true,
  "backup_interval_days": 7,
  "max_backups": 10,
  "last_backup": "20250912_143722",
  "pronunciation_language": "en"
}
```

### Performance Tuning

For large vocabularies (10,000+ words):
- Increase chunk size in data loading
- Adjust backup frequency
- Consider SSD storage for better I/O performance

## 🔬 Research Applications

This tool is designed for academic research in:
- **Cognitive Science**: Memory and learning pattern analysis
- **Educational Technology**: Adaptive learning algorithm development  
- **Natural Language Processing**: Vocabulary acquisition modeling
- **Human-Computer Interaction**: Interface optimization studies

### Data Sharing Protocol

For research collaboration:
1. Export anonymized learning data
2. Follow ethical guidelines for educational data
3. Contribute to open learning research initiatives

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add unit tests for new features
- Update documentation for API changes
- Ensure cross-platform compatibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by proven spaced repetition research
- Built for the open-source learning community
- Designed with accessibility and efficiency in mind

---

<p align="center">
  <strong>Made with ❤️ for learners and researchers worldwide</strong>
</p>
