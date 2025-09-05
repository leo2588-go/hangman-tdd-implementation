"""
Word Dictionary Module for Hangman Game
Author: CDU Software Engineering Student
Course: PRT582 - Software Unit Testing

Dictionary management system for the hangman game.
Handles word storage, validation and random selection.
"""

import random


class WordDictionary:
    """
    Manages words and phrases for different game difficulties.
    Keeps basic words separate from intermediate phrases.
    """
    def __init__(self):
        """Set up word lists for both game modes."""
        # Basic level words - mostly programming related
        self.basic_words = [
            "python", "java", "coding", "debug", "loops", "array",
            "string", "method", "class", "object", "variable", "function",
            "compiler", "syntax", "boolean", "integer", "database", "server",
            "client", "network", "protocol", "framework", "library", "module"
        ]
        # Intermediate phrases - technical concepts
        self.phrases = [
            "object oriented programming", "test driven development",
            "software engineering", "agile methodology", "version control",
            "continuous integration", "design patterns", "data structures",
            "machine learning", "artificial intelligence", "web development",
            "mobile applications", "cloud computing", "cyber security"
        ]
    def get_random_word(self):
        """Pick a random word for basic level."""
        if not self.basic_words:
            return "PYTHON"  # fallback
        return random.choice(self.basic_words).upper()
    def get_random_phrase(self):
        """Pick a random phrase for intermediate level."""
        if not self.phrases:
            return "UNIT TESTING"  # fallback
        return random.choice(self.phrases).upper()

    def is_valid_word(self, word):
        """Check if word/phrase exists in our dictionary."""
        if not word:
            return False
        word_clean = word.lower().strip()
        return (word_clean in self.basic_words or word_clean in self.phrases)
    def word_count(self):
        """How many basic words we have."""
        return len(self.basic_words)
    def phrase_count(self):
        """How many phrases we have."""
        return len(self.phrases)
