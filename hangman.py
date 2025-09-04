#!/usr/bin/env python3
"""
Hangman Game – Main Program
Author: Yuan Li
Student ID: s390310
Course: PRT582 - Software Unit Testing
Institution: Charles Darwin University
GitHub Repository: https://github.com/leo2588-go/hangman-tdd-implementation

Main entry point for the hangman game.
Developed using TDD methodology for unit testing coursework.

To run: python hangman.py
Requirements: Python 3.7+ (no external dependencies)
"""


import sys
import os

# Make sure we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ui import HangmanUI
except ImportError as e:
    print("Error: Can't find required game modules.")
    print(f"Details: {e}")
    print("\nMake sure these files are in the same folder:")
    print("  - hangman.py (this file)")
    print("  - game.py")  
    print("  - ui.py")
    print("  - timer.py")
    print("  - word_dictionary.py")
    sys.exit(1)


def check_python_version():
    """Make sure we have a compatible Python version."""
    if sys.version_info < (3, 7):
        print(f"Sorry, this game needs Python 3.7 or newer.")
        print(f"You have Python {sys.version}")
        print("Please upgrade Python and try again.")
        return False
    return True


def check_modules():
    """Check that all required modules can be imported."""
    required = ['game', 'ui', 'timer', 'word_dictionary']
    missing = []
    
    for module_name in required:
        try:
            __import__(module_name)
        except ImportError:
            missing.append(module_name)
    
    if missing:
        print(f"Error: Missing modules: {', '.join(missing)}")
        print("Please make sure all game files are present.")
        return False
    
    return True


def show_welcome():
    """Show startup banner."""
    print()
    print("=" * 50)
    print("          HANGMAN GAME")
    print("      TDD Implementation")
    print()  
    print("  Student: Yuan Li (s390310)")
    print("  Course: PRT582 - Unit Testing")
    print("  https://github.com/leo2588-go/hangman-tdd-implementation")
    print("=" * 50)
    print()


def main():
    """Main program entry point."""
    try:
        show_welcome()
        
        print("Checking system requirements...")
        
        if not check_python_version():
            sys.exit(1)
            
        if not check_modules():
            sys.exit(1)
            
        print("✓ All checks passed!")
        print()
        
        # Start the game
        print("Starting Hangman Game...")
        ui = HangmanUI()
        ui.run_game()
        
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
        sys.exit(0)
        
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print(f"Error type: {type(e).__name__}")
        print("\nIf this keeps happening, please check:")
        print(f"  - Python version: {sys.version}")
        print(f"  - Operating system: {os.name}")
        print("  - All game files are present")
        sys.exit(1)


if __name__ == "__main__":
    main()