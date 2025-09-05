"""
User Interface for Hangman Game
Author: CDU Software Engineering Student

Console-based UI for the hangman game.
Handles all the display and user input.
"""

import time
import sys
from game import GameLevel, GameState, HangmanGame


class HangmanUI:
    """Handles display and user interaction."""
    def __init__(self):
        self.game = None
    def show_welcome(self):
        """Display welcome screen and rules."""
        print("\n" + "=" * 60)
        print("🎯 HANGMAN GAME 🎯")
        print("=" * 60)
        print("\n📋 RULES:")
        print("• Guess letters to find the hidden word or phrase")
        print("• You have 15 seconds for each guess")
        print("• Wrong guesses cost you a life (you start with 6)")
        print("• Find the word before lives run out!")
        print("\n🎮 LEVELS:")
        print("1. Basic - Programming terms")
        print("2. Intermediate - Technical phrases")
        print("\n" + "=" * 60)
    def get_difficulty(self):
        """Get player's choice of difficulty level."""
        while True:
            try:
                choice = input("\nSelect difficulty (1=Basic, 2=Intermediate): ").strip()
                if choice == "1":
                    print("✅ Basic level selected!")
                    return GameLevel.BASIC
                elif choice == "2":
                    print("✅ Intermediate level selected!")
                    return GameLevel.INTERMEDIATE
                else:
                    print("❌ Please enter 1 or 2")
            except (EOFError, KeyboardInterrupt):
                print("\n👋 Goodbye!")
                sys.exit(0)
    def show_game_status(self, game):
        """Display current game state."""
        print("\n" + "-" * 50)
        print(f"💖 Lives: {game.get_lives()}")
        print(f"🎯 Word: {game.get_display_word()}")
        guessed = game.get_guessed_letters()
        wrong = game.get_wrong_guesses()
        if guessed:
            correct = [letter for letter in guessed if letter not in wrong]
            if correct:
                print(f"✅ Correct guesses: {', '.join(correct)}")
            if wrong:
                print(f"❌ Wrong guesses: {', '.join(wrong)}")
        else:
            print("📝 No guesses yet")
        # Show timer if active
        time_left = game.get_timer_remaining()
        if time_left > 0:
            print(f"⏰ Time left: {time_left} seconds")
        print("-" * 50)
    def get_player_guess(self):
        """Get letter guess from player."""
        try:
            return input("\n🎯 Enter your guess (or 'quit' to exit): ").strip()
        except (EOFError, KeyboardInterrupt):
            return "quit"
    def show_guess_result(self, success, message):
        """Display the result of a guess."""
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
    def show_game_end(self, game):
        """Display end game screen."""
        print("\n" + "=" * 60)
        state = game.get_game_state()
        if state == GameState.WON:
            print("🎉 CONGRATULATIONS! YOU WON! 🎉")
            print(f"✅ The word was: {game.get_answer()}")
        elif state == GameState.LOST:
            print("💀 GAME OVER 💀")
            print(f"💡 The answer was: {game.get_answer()}")
        elif state == GameState.QUIT:
            print("👋 Thanks for playing!")
            print(f"💡 The answer was: {game.get_answer()}")
        print("=" * 60)
    def ask_play_again(self):
        """Ask if player wants another game."""
        while True:
            try:
                choice = input("\n🔄 Play again? (y/n): ").strip().lower()
                if choice in ['y', 'yes']:
                    return True
                elif choice in ['n', 'no']:
                    return False
                else:
                    print("❌ Please enter 'y' or 'n'")
            except (EOFError, KeyboardInterrupt):
                return False
    def run_game(self):
        """Main game loop."""
        self.show_welcome()
        while True:
            # Get difficulty and start new game
            level = self.get_difficulty()
            self.game = HangmanGame(level)
            print(f"\n🚀 Starting {level.value} level game...")
            time.sleep(1)
            # Main game loop
            while self.game.get_game_state() == GameState.PLAYING:
                self.show_game_status(self.game)
                self.game.start_guess_timer()
                guess = self.get_player_guess()
                if guess.lower() == 'quit':
                    self.game.quit_game()
                    break
                success, message = self.game.make_guess(guess)
                self.show_guess_result(success, message)
                # Brief pause for user to read result
                time.sleep(1)
            # Show end game
            self.show_game_end(self.game)
            # Ask to play again
            if not self.ask_play_again():
                break
        print("\n🎮 Thanks for playing Hangman!")
        print("👋 Goodbye!")


def main():
    """Entry point if running UI directly."""
    try:
        ui = HangmanUI()
        ui.run_game()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
