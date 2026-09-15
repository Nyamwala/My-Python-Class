"""A command-line Guess the Number game with difficulty levels."""

import random
from pathlib import Path


DIFFICULTIES = {
    "easy": 10,
    "medium": 7,
    "hard": 5,
}

SCORES_FILE = Path(__file__).with_name("high_scores.txt")


def choose_difficulty():
    """Prompt until the player chooses a supported difficulty."""
    while True:
        choice = input("Choose a difficulty (Easy, Medium, Hard): ").strip().lower()
        if choice in DIFFICULTIES:
            return choice
        print("Please enter Easy, Medium, or Hard.")


def get_guess():
    """Prompt until the player enters a whole number from 1 through 100."""
    while True:
        try:
            guess = int(input("Enter your guess (1-100): "))
            if 1 <= guess <= 100:
                return guess
            print("Your guess must be between 1 and 100.")
        except ValueError:
            print("Please enter a whole number.")


def get_hint(number):
    """Return a useful fact about the secret number."""
    for divisor in range(2, 11):
        if number % divisor == 0:
            return f"Hint: the number is divisible by {divisor}."
    return "Hint: the number is not divisible by any whole number from 2 to 10."


def save_score(username, difficulty, attempts_used):
    """Save a winning result. Higher scores reward harder modes and fewer guesses."""
    difficulty_points = {"easy": 100, "medium": 200, "hard": 300}
    score = difficulty_points[difficulty] + (DIFFICULTIES[difficulty] - attempts_used) * 10

    with SCORES_FILE.open("a", encoding="utf-8") as score_file:
        score_file.write(f"{username}|{difficulty.title()}|{score}\n")
    return score


def show_leaderboard():
    """Display saved scores from highest to lowest."""
    if not SCORES_FILE.exists():
        print("\nLeaderboard: no high scores yet.")
        return

    scores = []
    for line in SCORES_FILE.read_text(encoding="utf-8").splitlines():
        parts = line.split("|")
        if len(parts) == 3:
            try:
                scores.append((parts[0], parts[1], int(parts[2])))
            except ValueError:
                continue

    if not scores:
        print("\nLeaderboard: no high scores yet.")
        return

    print("\n--- Leaderboard ---")
    for rank, (username, difficulty, score) in enumerate(
        sorted(scores, key=lambda entry: entry[2], reverse=True)[:10], start=1
    ):
        print(f"{rank}. {username} — {score} points ({difficulty})")


def play_game():
    username = input("Enter your username: ").strip() or "Player"
    difficulty = choose_difficulty()
    max_attempts = DIFFICULTIES[difficulty]
    secret_number = random.randint(1, 100)

    print(f"\n{difficulty.title()} mode: you have {max_attempts} guesses.")

    for attempt in range(1, max_attempts + 1):
        guess = get_guess()

        if guess == secret_number:
            score = save_score(username, difficulty, attempt)
            print(
                f"Correct! You guessed the number in {attempt} attempt(s) "
                f"and earned {score} points."
            )
            show_leaderboard()
            return

        if guess > secret_number:
            print("Too High")
        else:
            print("Too Low")

        if attempt == 3:
            print(get_hint(secret_number))

        remaining = max_attempts - attempt
        if remaining:
            print(f"Guesses remaining: {remaining}")

    print(f"Out of guesses! The number was {secret_number}.")
    show_leaderboard()


if __name__ == "__main__":
    print("Welcome to Guess the Number!")
    play_game()
