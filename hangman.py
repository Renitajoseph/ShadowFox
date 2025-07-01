import random
words_with_hints = [
    ("python", "A popular programming language"),
    ("hangman", "The name of this game"),
    ("laptop", "A portable computer"),
    ("umbrella", "Protects from rain"),
    ("banana", "A yellow fruit")
]
word, hint = random.choice(words_with_hints)
guessed = ["_"] * len(word)
attempts_left = 6
guessed_letters = set()

print("🔤 Welcome to Hangman!")
print(f"Hint: {hint}")
while attempts_left > 0 and "_" in guessed:
    print("\nWord: " + " ".join(guessed))
    print(f"Remaining attempts: {attempts_left}")
    guess = input("Enter a letter: ").lower()

    if guess in guessed_letters:
        print("⚠️ You've already guessed that letter.")
        continue
    guessed_letters.add(guess)

    if guess in word:
        for i, letter in enumerate(word):
            if letter == guess:
                guessed[i] = guess
        print("Correct guess!")
    else:
        attempts_left -= 1
        print("Wrong guess!")
if "_" not in guessed:
    print(f"\n You guessed the word: {word}")
else:
    print(f"\n Out of attempts! The word was: {word}")
