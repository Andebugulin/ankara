# Vocabulary Learning Tool

<p align="center">
  <img src="./ankara.png" alt="Vocabulary Learning Tool (Ankara) Logo">
</p>

Welcome to the **Vocabulary Learning Tool**, an interactive and engaging way to enhance your vocabulary. This application utilizes principles of spaced repetition and randomization to help users effectively learn and retain new words.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Key Bindings](#key-bindings)
- [Optimized Hand Placement](#optimized-hand-placement)
- [How It Works](#how-it-works)
- [Setup Instructions](#setup-instructions)
- [How to Use](#how-to-use)
- [Data Format](#data-format)
- [Data Analysis and Neural Networks](#data-analysis-and-neural-networks)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Learning vocabulary is crucial for language acquisition, but it can often be tedious and ineffective without the right methods. This tool leverages spaced repetition and randomization to optimize the learning process. By randomizing the presentation of words, we prevent the brain from merely memorizing their sequences or positions, thus ensuring better retention and understanding.

## Features

- **Spaced Repetition**: Prioritizes words based on how well you remember them.
- **Randomization**: Prevents memorization of word sequences, ensuring better retention.
- **Interactive Learning**: Provides examples and pronunciation for each word.
- **User-Friendly Interface**: Easy-to-use graphical interface with visual feedback.
- **Vim-like Key Bindings**: Efficient and ergonomic key bindings for seamless interaction.

## Key Bindings

The application supports Vim-like key bindings for an intuitive and efficient learning experience:

- `n` - Next word
- `p` - Previous word
- `h` - Mark word as "don't remember"
- `j` - Mark word as "hard"
- `k` - Mark word as "normal"
- `l` - Mark word as "nice"
- `i` - Mark word as "very impressive"
- `0` - Skip 10 words forward
- `f` - Show word
- `d` - Show meaning
- `s` - Show example
- `a` - Play pronunciation

## Optimized Hand Placement

For the best user experience, we recommend positioning your hands as follows:

- **Right Hand**: Place your index finger on `h`, middle finger on `j`, ring finger on `k`, and pinky on `l`. This positioning allows easy access to the evaluation keys.
- **Left Hand**: Place your index finger on `f`, middle finger on `d`, ring finger on `s`, and pinky on `a`. This positioning allows easy access to the word interaction keys.

This hand placement mimics the efficient navigation of Vim, allowing for quick and comfortable interaction with the application.

## How It Works

The human brain tends to remember information better when it is presented in a non-linear, unpredictable manner. This tool randomizes the order of words to prevent users from simply memorizing their positions or sequences. Instead, it encourages true understanding and retention by presenting words in varied contexts.

### Spaced Repetition

Spaced repetition is a learning technique that involves increasing intervals of time between subsequent reviews of previously learned material. This tool tracks your progress with each word and adjusts the frequency of review based on how well you remember it.

### Randomization

Randomizing the order of words disrupts the potential for pattern recognition or memorizing positions, which can hinder true learning. This method ensures that your brain engages with the content meaningfully each time.

## Setup Instructions

### Prerequisites

- Python 3.x
- Required Python libraries: `pygame`, `pandas`, `gtts`

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/vocabulary-learning-tool.git
   cd vocabulary-learning-tool
   ```

2. **Create and Activate a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare Your Vocabulary Data**

   - Place your vocabulary data in an `xlsx` or `csv` file named `capture.xlsx` or `capture.csv` in the root directory.

## How to Use

1. **Run the Application**

   ```bash
   python main.py
   ```

2. **Follow the On-Screen Instructions**

   - Use the provided key bindings to navigate and interact with the vocabulary words.
   - Evaluate each word based on your familiarity to adjust its review frequency.

3. **Close the Application**

   - Press `ESC` to exit the application. Your progress will be automatically saved.

## Data Format

To ensure your vocabulary data is properly loaded, please refer to the example Excel file [example](/capture.xlsx) provided in the repository. The data should be structured with the following columns:

### Essential Columns

- **word**: The vocabulary word to learn.
- **meaning**: The definition or meaning of the word.
- **example**: A sentence or phrase using the word in context.

### Feedback Columns

- **date**: The date the word was added.
- **classes**: The spaced repetition class of the word (used for tracking review intervals).
- **last_changes_of_class**: The date when the class was last changed.
- **date_becoming**: The date the word reached the highest class.
- **recalling**: A counter for recalling the word after it has reached the highest class.

These additional columns help the tool manage the spaced repetition algorithm more effectively.

## Data Analysis and Neural Networks

The collected data can also be used for data analysis purposes and to train neural networks. The feedback columns are designed with this in mind. By analyzing user interactions and progress, we can provide more thorough feedback and potentially enhance the learning algorithm. This opens up opportunities for future improvements and personalized learning experiences.

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests with your improvements.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/your-feature`)
3. Commit your Changes (`git commit -m 'Add your feature'`)
4. Push to the Branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Thank you for using the **Vocabulary Learning Tool**. We hope it helps you achieve your language learning goals effectively! If you have any questions or feedback, feel free to open an issue or contact us directly. Happy learning!
