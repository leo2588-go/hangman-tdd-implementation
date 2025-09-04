"""
Core Game Logic for Hangman
Author: CDU Software Engineering Student

Main game mechanics and state management.
This took a while to get right with all the edge cases.
"""

from enum import Enum
from word_dictionary import WordDictionary
from timer import GameTimer


class GameLevel(Enum):
    """Game difficulty levels."""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"


class GameState(Enum):
    """Possible game states."""
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"
    QUIT = "quit"


class HangmanGame:
    """Main game logic and state management."""
    
    def __init__(self, level=GameLevel.BASIC):
        """Set up a new game."""
        self.dictionary = WordDictionary()
        self.level = level
        self.answer = ""
        self.guessed_letters = set()
        self.wrong_guesses = set()
        self.lives = 6
        self.state = GameState.PLAYING
        self.timer = GameTimer(self._on_timeout)
        
        self._start_new_round()
    
    def _start_new_round(self):
        """Initialize for a new game round."""
        if self.level == GameLevel.BASIC:
            self.answer = self.dictionary.get_random_word()
        else:
            self.answer = self.dictionary.get_random_phrase()
        
        self.guessed_letters.clear()
        self.wrong_guesses.clear()
        self.lives = 6
        self.state = GameState.PLAYING
    
    def _on_timeout(self):
        """Handle when timer runs out."""
        if self.state == GameState.PLAYING:
            self.lives -= 1
            if self.lives <= 0:
                self.state = GameState.LOST
    
    def get_display_word(self):
        """Show current progress with underscores for missing letters."""
        display = ""
        for char in self.answer:
            if char.isalpha():
                if char in self.guessed_letters:
                    display += char
                else:
                    display += "_"
            else:
                display += char  # spaces and punctuation shown
        return display
    
    def make_guess(self, letter):
        """Process a player's guess. Returns (success, message)."""
        if self.state != GameState.PLAYING:
            return False, "Game is not active"
        
        # Stop timer when guess is made
        self.timer.stop_timer()
        
        letter = letter.upper().strip()
        
        # Check if input is valid
        if not letter:
            return False, "Please enter a letter"
        if len(letter) != 1:
            return False, "Please enter just one letter"
        if not letter.isalpha():
            return False, "Please enter a letter, not a number or symbol"
        if letter in self.guessed_letters:
            return False, "You already guessed that letter"
        
        # Process the guess
        self.guessed_letters.add(letter)
        
        if letter in self.answer:
            # Correct guess
            if self._word_complete():
                self.state = GameState.WON
                return True, f"Correct! '{letter}' is in the word. You won!"
            return True, f"Good guess! '{letter}' is in the word."
        else:
            # Wrong guess
            self.wrong_guesses.add(letter)
            self.lives -= 1
            if self.lives <= 0:
                self.state = GameState.LOST
                return False, f"Sorry, '{letter}' is not in the word. Game over!"
            return False, f"Sorry, '{letter}' is not in the word. {self.lives} lives left."
    
    def _word_complete(self):
        """Check if all letters have been guessed."""
        for char in self.answer:
            if char.isalpha() and char not in self.guessed_letters:
                return False
        return True
    
    def start_guess_timer(self):
        """Start the 15-second timer for current guess."""
        if self.state == GameState.PLAYING:
            self.timer.start_timer(15)
    
    # Getter methods
    def get_game_state(self):
        return self.state
    
    def get_lives(self):
        return self.lives
    
    def get_guessed_letters(self):
        return sorted(list(self.guessed_letters))
    
    def get_wrong_guesses(self):
        return sorted(list(self.wrong_guesses))
    
    def get_answer(self):
        return self.answer
    
    def get_timer_remaining(self):
        return self.timer.get_time_left()
    
    def quit_game(self):
        """End the current game."""
        self.timer.stop_timer()
        self.state = GameState.QUIT
    
    def new_game(self, level=None):
        """Start a fresh game."""
        self.timer.stop_timer()
        if level:
            self.level = level
        self._start_new_round()