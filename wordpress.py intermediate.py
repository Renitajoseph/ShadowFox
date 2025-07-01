import random
import tkinter as tk
from tkinter import messagebox

class Hangman:
    def __init__(self):
        self.word_list = [
            ("PYTHON", "Programming language"),
            ("JAVASCRIPT", "Web programming language"),
            ("COMPUTER", "Electronic device"),
            ("KEYBOARD", "Input device"),
            ("DEVELOPER", "Person who writes code"),
            ("ALGORITHM", "Step-by-step procedure"),
            ("FUNCTION", "Reusable code block"),
            ("VARIABLE", "Stores data value")
        ]
        self.stages = [
            """
               --------
               |      |
               |      
               |    
               |      
               |     
               -
            """,
            """
               --------
               |      |
               |      O
               |    
               |      
               |     
               -
            """,
            """
               --------
               |      |
               |      O
               |      |
               |      |
               |     
               -
            """,
            """
               --------
               |      |
               |      O
               |     \\|
               |      |
               |     
               -
            """,
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |     
               -
            """,
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |     / 
               -
            """,
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |     / \\
               -
            """
        ]
        self.reset_game()

    def reset_game(self):
        self.word, self.hint = random.choice(self.word_list)
        self.guessed_letters = []
        self.incorrect_guesses = 0
        self.max_attempts = len(self.stages) - 1
        self.display_word = ['_' if char.isalpha() else char for char in self.word]
        self.game_over = False

    def display_game(self):
        print(self.stages[self.incorrect_guesses])
        print("Word: " + " ".join(self.display_word))
        print(f"Hint: {self.hint}")
        print(f"Guessed letters: {', '.join(sorted(self.guessed_letters))}")
        print(f"Incorrect guesses left: {self.max_attempts - self.incorrect_guesses}")
        print("-" * 40)

    def make_guess(self, letter):
        letter = letter.upper()
        
        if len(letter) != 1 or not letter.isalpha():
            print("Please enter a single letter.")
            return
        
        if letter in self.guessed_letters:
            print("You've already guessed that letter.")
            return
            
        self.guessed_letters.append(letter)
        
        if letter in self.word:
            for i, char in enumerate(self.word):
                if char == letter:
                    self.display_word[i] = letter
            print("\nCorrect guess!")
        else:
            self.incorrect_guesses += 1
            print("\nIncorrect guess!")
            
        # Check game status
        if '_' not in self.display_word:
            print("\n" + "=" * 40)
            print(f"Congratulations! You won! The word was: {self.word}")
            print("=" * 40 + "\n")
            self.game_over = True
        elif self.incorrect_guesses >= self.max_attempts:
            print("\n" + "=" * 40)
            print(f"Game over! The word was: {self.word}")
            print(self.stages[-1])
            print("=" * 40 + "\n")
            self.game_over = True

    def play(self):
        print("\n" + "=" * 40)
        print("        WELCOME TO HANGMAN")
        print("=" * 40)
        print("Rules:")
        print("- Try to guess the word before the hangman is complete")
        print("- You'll get hints to help you")
        print("- Each incorrect guess adds a body part")
        print("- Game ends when you win or the hangman is complete\n")
        
        self.reset_game()
        
        while not self.game_over:
            self.display_game()
            guess = input("Enter your guess (a single letter): ").strip()
            self.make_guess(guess)
            
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again in ['yes', 'y']:
            self.play()
        else:
            print("\nThanks for playing Hangman!")

class HangmanGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")
        # Set dark theme colors
        self.bg_color = "#23272e"
        self.fg_color = "#f8f8f2"
        self.entry_bg = "#282c34"
        self.entry_fg = "#f8f8f2"
        self.button_bg = "#44475a"
        self.button_fg = "#f8f8f2"
        self.master.configure(bg=self.bg_color)
        self.master.minsize(500, 500)  # Set minimum window size
        self.game = Hangman()
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        self.stage_label = tk.Label(
            self.master, font=("Courier New", 18), justify="left",
            bg=self.bg_color, fg=self.fg_color
        )
        self.stage_label.pack(pady=(20, 10))

        self.word_label = tk.Label(
            self.master, font=("Consolas", 32, "bold"),
            bg=self.bg_color, fg="#50fa7b"
        )
        self.word_label.pack(pady=20)

        self.hint_label = tk.Label(
            self.master, font=("Arial", 18, "italic"),
            bg=self.bg_color, fg="#8be9fd"
        )
        self.hint_label.pack(pady=(0, 10))

        self.guessed_label = tk.Label(
            self.master, font=("Arial", 16),
            bg=self.bg_color, fg="#bd93f9"
        )
        self.guessed_label.pack(pady=(0, 5))

        self.remaining_label = tk.Label(
            self.master, font=("Arial", 16),
            bg=self.bg_color, fg="#ffb86c"
        )
        self.remaining_label.pack(pady=(0, 15))

        self.entry = tk.Entry(
            self.master, font=("Consolas", 24), width=3,
            bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.fg_color,
            justify="center"
        )
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.process_guess)

        self.guess_button = tk.Button(
            self.master, text="Guess", command=self.process_guess,
            font=("Arial", 16, "bold"),
            bg=self.button_bg, fg=self.button_fg, activebackground="#6272a4", activeforeground=self.fg_color,
            width=10, height=1
        )
        self.guess_button.pack(pady=(0, 10))

        self.reset_button = tk.Button(
            self.master, text="Reset Game", command=self.reset_game,
            font=("Arial", 14),
            bg=self.button_bg, fg=self.button_fg, activebackground="#6272a4", activeforeground=self.fg_color,
            width=12, height=1
        )
        self.reset_button.pack(pady=5)

    def update_display(self):
        self.stage_label.config(text=self.game.stages[self.game.incorrect_guesses])
        self.word_label.config(text=" ".join(self.game.display_word))
        self.hint_label.config(text=f"Hint: {self.game.hint}")
        self.guessed_label.config(text=f"Guessed: {', '.join(sorted(self.game.guessed_letters))}")
        self.remaining_label.config(
            text=f"Incorrect guesses left: {self.game.max_attempts - self.game.incorrect_guesses}"
        )
        self.entry.delete(0, tk.END)
        if self.game.game_over:
            if '_' not in self.game.display_word:
                messagebox.showinfo("Hangman", f"Congratulations! You won!\nThe word was: {self.game.word}")
            else:
                messagebox.showinfo("Hangman", f"Game over! The word was: {self.game.word}")

    def process_guess(self, event=None):
        if self.game.game_over:
            return
        guess = self.entry.get().strip()
        if not guess:
            return
        prev_state = (self.game.display_word[:], self.game.incorrect_guesses)
        self.game.make_guess(guess)
        # Prevent duplicate messageboxes for repeated guesses
        if (self.game.display_word, self.game.incorrect_guesses) != prev_state:
            self.update_display()

    def reset_game(self):
        self.game.reset_game()
        self.update_display()

# Start the game
if __name__ == "__main__":
    # Uncomment the following lines to run the GUI instead of CLI
    root = tk.Tk()
    gui = HangmanGUI(root)
    root.mainloop()

    # CLI version:
    # game = Hangman()
    # game.play()