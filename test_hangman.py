"""
Unit Tests for Hangman Game
Author: Yuan Li
Student ID: s390310
Course: PRT582 - Software Unit Testing
Institution: Charles Darwin University

Test suite for the modular hangman game implementation.
Follows TDD principles with comprehensive coverage of all modules.

To run tests: python -m unittest test_hangman.py -v
Framework: unittest (Python standard library)
"""

import unittest
import time
import sys
import os
from unittest.mock import Mock, patch
import threading

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from word_dictionary import WordDictionary

from timer import GameTimer  
from game import GameLevel, GameState, HangmanGame
from ui import HangmanUI


class TestWordDictionary(unittest.TestCase):
    """Tests for the word dictionary module."""
    
    def setUp(self):
        """Create a dictionary for testing."""
        self.dictionary = WordDictionary()
    
    def test_get_random_word_returns_string(self):
        """Basic word should be a non-empty string."""
        word = self.dictionary.get_random_word()
        self.assertIsInstance(word, str)
        self.assertGreater(len(word), 0)
    
    def test_get_random_word_returns_uppercase(self):
        """Words should be returned in uppercase."""
        word = self.dictionary.get_random_word()
        self.assertTrue(word.isupper())
    
    def test_get_random_phrase_returns_string(self):
        """Phrases should be non-empty strings."""
        phrase = self.dictionary.get_random_phrase()
        self.assertIsInstance(phrase, str)
        self.assertGreater(len(phrase), 0)
    
    def test_get_random_phrase_has_spaces(self):
        """Phrases should contain spaces (multiple words)."""
        phrase = self.dictionary.get_random_phrase()
        self.assertIn(' ', phrase)
    
    def test_is_valid_word_with_known_word(self):
        """Should recognize words from our dictionary."""
        # We know 'python' is in the basic words
        self.assertTrue(self.dictionary.is_valid_word('python'))
        self.assertTrue(self.dictionary.is_valid_word('PYTHON'))
    
    def test_is_valid_word_with_unknown_word(self):
        """Should reject words not in our dictionary."""
        self.assertFalse(self.dictionary.is_valid_word('invalidword123'))
    
    def test_word_and_phrase_counts(self):
        """Should return correct counts for word lists."""
        word_count = self.dictionary.word_count()
        phrase_count = self.dictionary.phrase_count()
        self.assertGreater(word_count, 0)
        self.assertGreater(phrase_count, 0)


class TestGameTimer(unittest.TestCase):
    """Tests for the timer module."""
    
    def setUp(self):
        """Set up timer for testing."""
        self.callback_triggered = False
        
        def test_callback():
            self.callback_triggered = True
        
        self.timer = GameTimer(test_callback)
    
    def tearDown(self):
        """Clean up timer."""
        if self.timer:
            self.timer.stop_timer()
    
    def test_timer_starts_inactive(self):
        """New timer should not be running."""
        self.assertFalse(self.timer.is_running())
        self.assertEqual(self.timer.get_time_left(), 0)
    
    def test_timer_can_start(self):
        """Should be able to start the timer."""
        self.timer.start_timer(5)
        self.assertTrue(self.timer.is_running())
    
    def test_timer_can_stop(self):
        """Should be able to stop a running timer."""
        self.timer.start_timer(5)
        self.assertTrue(self.timer.is_running())
        self.timer.stop_timer()
        self.assertFalse(self.timer.is_running())
    
    def test_timer_callback_on_timeout(self):
        """Callback should be called when timer expires."""
        self.timer.start_timer(0.1)  # Very short timer
        time.sleep(0.2)  # Wait for it to expire
        # Give callback thread time to execute
        time.sleep(0.1)
        self.assertTrue(self.callback_triggered)
    
    def test_real_time_countdown(self):
        """Timer should count down in real time."""
        self.timer.start_timer(3)
        initial_time = self.timer.get_time_left()
        time.sleep(1)
        later_time = self.timer.get_time_left()
        # Should have decreased
        self.assertLess(later_time, initial_time)
    
    def test_progress_percentage(self):
        """Should track progress as percentage."""
        self.timer.start_timer(2)
        time.sleep(0.1)
        progress = self.timer.get_progress_percent()
        self.assertGreater(progress, 0)
        self.assertLess(progress, 100)


class TestHangmanGame(unittest.TestCase):
    """Tests for core game logic."""
    
    def setUp(self):
        """Set up game for testing."""
        self.game = HangmanGame(GameLevel.BASIC)
        # Use a known word for predictable testing
        self.game.answer = "PYTHON"
        self.game.guessed_letters = set()
        self.game.wrong_guesses = set()
    
    def tearDown(self):
        """Clean up game."""
        if self.game:
            self.game.quit_game()
    
    def test_game_starts_properly(self):
        """New game should be in correct initial state."""
        self.assertEqual(self.game.get_game_state(), GameState.PLAYING)
        self.assertEqual(self.game.get_lives(), 6)
        self.assertEqual(len(self.game.get_guessed_letters()), 0)
    
    def test_display_word_shows_underscores(self):
        """Should show underscores for unguessed letters."""
        display = self.game.get_display_word()
        self.assertEqual(display, "______")  # PYTHON = 6 letters
    
    def test_correct_guess_reveals_letter(self):
        """Correct guess should reveal the letter."""
        success, msg = self.game.make_guess('P')
        self.assertTrue(success)
        self.assertIn('P', self.game.get_guessed_letters())
        self.assertEqual(self.game.get_display_word(), "P_____")
    
    def test_wrong_guess_loses_life(self):
        """Wrong guess should cost a life."""
        initial_lives = self.game.get_lives()
        success, msg = self.game.make_guess('Z')
        self.assertFalse(success)
        self.assertEqual(self.game.get_lives(), initial_lives - 1)
    
    def test_duplicate_guess_rejected(self):
        """Should reject guesses that were already made."""
        self.game.make_guess('P')
        success, msg = self.game.make_guess('P')
        self.assertFalse(success)
        self.assertIn('already', msg.lower())
    
    def test_invalid_input_rejected(self):
        """Should reject invalid inputs."""
        # Empty string
        success, msg = self.game.make_guess('')
        self.assertFalse(success)
        
        # Multiple characters  
        success, msg = self.game.make_guess('ABC')
        self.assertFalse(success)
        
        # Numbers
        success, msg = self.game.make_guess('1')
        self.assertFalse(success)
    
    def test_winning_condition(self):
        """Should win when all letters guessed."""
        # Guess all letters in PYTHON
        for letter in "PYTHON":
            if self.game.get_game_state() == GameState.PLAYING:
                self.game.make_guess(letter)
        
        self.assertEqual(self.game.get_game_state(), GameState.WON)
    
    def test_losing_condition(self):
        """Should lose when lives reach zero."""
        # Make enough wrong guesses to lose all lives
        wrong_letters = ['A', 'B', 'C', 'D', 'E', 'F']
        for letter in wrong_letters:
            if self.game.get_lives() > 0:
                self.game.make_guess(letter)
        
        self.assertEqual(self.game.get_game_state(), GameState.LOST)
        self.assertEqual(self.game.get_lives(), 0)


class TestHangmanUI(unittest.TestCase):
    """Tests for user interface components."""
    
    def setUp(self):
        """Set up UI for testing."""
        self.ui = HangmanUI()
    
    @patch('builtins.input', return_value='1')
    def test_difficulty_choice_basic(self, mock_input):
        """Should handle basic difficulty selection."""
        choice = self.ui.get_difficulty()
        self.assertEqual(choice, GameLevel.BASIC)
    
    @patch('builtins.input', return_value='2') 
    def test_difficulty_choice_intermediate(self, mock_input):
        """Should handle intermediate difficulty selection."""
        choice = self.ui.get_difficulty()
        self.assertEqual(choice, GameLevel.INTERMEDIATE)
    
    @patch('builtins.input', return_value='a')
    def test_get_player_guess(self, mock_input):
        """Should get player input."""
        guess = self.ui.get_player_guess()
        self.assertEqual(guess, 'a')
    
    @patch('builtins.print')
    def test_show_guess_result_success(self, mock_print):
        """Should display successful guess correctly."""
        self.ui.show_guess_result(True, "Good guess!")
        mock_print.assert_called()
    
    @patch('builtins.print') 
    def test_show_guess_result_failure(self, mock_print):
        """Should display failed guess correctly."""
        self.ui.show_guess_result(False, "Wrong letter!")
        mock_print.assert_called()


class TestGameIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def setUp(self):
        """Set up for integration testing."""
        self.game = HangmanGame(GameLevel.BASIC)
        self.game.answer = "TEST"  # Known word for predictable testing
    
    def tearDown(self):
        """Clean up integration tests."""
        if self.game:
            self.game.quit_game()
    
    def test_complete_winning_game(self):
        """Test a complete winning game scenario."""
        # Guess all letters correctly
        for letter in "TEST":
            if self.game.get_game_state() == GameState.PLAYING:
                success, msg = self.game.make_guess(letter)
                
        self.assertEqual(self.game.get_game_state(), GameState.WON)
        self.assertEqual(self.game.get_display_word(), "TEST")
    
    def test_complete_losing_game(self):
        """Test a complete losing game scenario."""
        # Make wrong guesses until game over
        wrong_letters = ['A', 'B', 'C', 'D', 'F', 'G']
        for letter in wrong_letters:
            if self.game.get_game_state() == GameState.PLAYING:
                self.game.make_guess(letter)
        
        self.assertEqual(self.game.get_game_state(), GameState.LOST)
    
    def test_mixed_correct_and_wrong_guesses(self):
        """Test game with both correct and wrong guesses."""
        # Some correct guesses
        self.game.make_guess('T')
        self.assertEqual(self.game.get_display_word(), 'T__T')
        
        # Some wrong guesses
        self.game.make_guess('X')
        self.assertEqual(self.game.get_lives(), 5)
        
        # Game should still be active
        self.assertEqual(self.game.get_game_state(), GameState.PLAYING)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def test_single_letter_word(self):
        """Test with very short word."""
        game = HangmanGame(GameLevel.BASIC)
        game.answer = "A"
        
        success, msg = game.make_guess('A')
        self.assertTrue(success)
        self.assertEqual(game.get_game_state(), GameState.WON)
        game.quit_game()
    
    def test_word_with_repeated_letters(self):
        """Test word with duplicate letters."""
        game = HangmanGame(GameLevel.BASIC)
        game.answer = "HELLO"
        
        success, msg = game.make_guess('L')
        self.assertTrue(success)
        # Both L's should be revealed
        self.assertEqual(game.get_display_word(), "__LL_")
        game.quit_game()
    
    def test_case_insensitive_guessing(self):
        """Test that uppercase and lowercase work the same."""
        game = HangmanGame(GameLevel.BASIC)
        game.answer = "TEST"
        
        # Try lowercase
        success, msg = game.make_guess('t')
        self.assertTrue(success)
        self.assertIn('T', game.get_guessed_letters())
        game.quit_game()


if __name__ == '__main__':
    # Set up test suite
    test_classes = [
        TestWordDictionary,
        TestGameTimer,
        TestHangmanGame, 
        TestHangmanUI,
        TestGameIntegration,
        TestEdgeCases
    ]
    
    loader = unittest.TestLoader()
    suites = []
    
    for test_class in test_classes:
        suite = loader.loadTestsFromTestCase(test_class)
        suites.append(suite)
    
    # Run all tests
    combined_suite = unittest.TestSuite(suites)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(combined_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"TEST RESULTS SUMMARY")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
        print(f"Success rate: {success_rate:.1f}%")
    
    if result.failures:
        print(f"\nFAILURES ({len(result.failures)}):")
        for test, error in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for test, error in result.errors:
            print(f"  - {test}")
    
    if len(result.failures) == 0 and len(result.errors) == 0:
        print(f"\n✓ All tests passed!")
    
    print(f"{'='*50}")