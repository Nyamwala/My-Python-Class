import random

# List of quiz questions
questions = [
    {
        "question": "What is 8 + 4?",
        "choices": {
            "A": "10",
            "B": "12",
            "C": "13",
            "D": "15"
        },
        "answer": "B"
    },
    {
        "question": "What is the capital city of Kenya?",
        "choices": {
            "A": "Nairobi",
            "B": "Mombasa",
            "C": "Kisumu",
            "D": "Nakuru"
        },
        "answer": "A"
    },
    {
        "question": "Which planet is the larget Planet?",
        "choices": {
            "A": "Earth",
            "B": "Jupiter",
            "C": "Mars",
            "D": "Venus"
        },
        "answer": "B"
    },
    {
        "question": "Who wrote the play 'Romeo and Juliet'?",
        "choices": {
            "A": "William Shakespeare",
            "B": "Charles Dickens",
            "C": "Mark Twain",
            "D": "George Orwell"
        },
        "answer": "A"
    },
    {
        "question": "What is 10 × 8?",
        "choices": {
            "A": "18",
            "B": "70",
            "C": "80",
            "D": "90"
        },
        "answer": "C"
    },
    {
        "question": "Which is the largest ocean on Earth?",
        "choices": {
            "A": "Atlantic Ocean",
            "B": "Indian Ocean",
            "C": "Arctic Ocean",
            "D": "Pacific Ocean"
        },
        "answer": "D"
    },
    {
        "question": "How many continents are there?",
        "choices": {
            "A": "5",
            "B": "6",
            "C": "7",
            "D": "8"
        },
        "answer": "C"
    },
    {
        "question": "What is the chemical symbol for water?",
        "choices": {
            "A": "CO2",
            "B": "H2O",
            "C": "O2",
            "D": "NaCl"
        },
        "answer": "B"
    }
]


def run_quiz():
    score = 0

    # Make a copy so the original question list is not changed
    quiz_questions = questions.copy()

    # Randomly mix the questions
    random.shuffle(quiz_questions)

    print("=" * 50)
    print("        WELCOME TO THE QUIZ APPLICATION")
    print("=" * 50)

    # Loop through every question
    for number, question in enumerate(quiz_questions, start=1):

        print(f"\nQuestion {number}: {question['question']}")

        # Display choices
        for letter, choice in question["choices"].items():
            print(f"{letter}. {choice}")

        # Keep asking until valid input is entered
        while True:
            try:
                user_answer = input("Enter your answer (A, B, C, or D): ").strip().upper()

                if user_answer not in ["A", "B", "C", "D"]:
                    raise ValueError("Invalid answer")

                break

            except ValueError:
                print("Invalid input! Please enter A, B, C, or D.")

        # Compare user's answer with correct answer
        if user_answer == question["answer"]:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect! The correct answer was {question['answer']}.")

    # Calculate percentage
    total_questions = len(quiz_questions)
    percentage = (score / total_questions) * 100

    # Display final results
    print("\n" + "=" * 50)
    print("                 QUIZ RESULTS")
    print("=" * 50)

    print(f"Your score: {score}/{total_questions}")
    print(f"Percentage: {percentage:.1f}%")

    # Provide feedback based on score
    if percentage >= 80:
        print("Feedback: Excellent! 🎉")
    elif percentage >= 50:
        print("Feedback: Good! 👍")
    else:
        print("Feedback: Try Again! 💪")

    print("=" * 50)


# Start the quiz
run_quiz()