# This file is the complete main program for the math practice app

from math_question_class import MathQuestion

while True:
    # Generate a random question
    question = MathQuestion.generate_question()

    # Get question text and prompt user
    prompt = question.question_text()
    user_input = input(prompt)

    # Check if user wants to quit
    if user_input == "q":
        print("Good bye!")
        break

    # Convert input to int and check answer
    try:
        answer = int(user_input)
        if question.check_answer(answer):
            print("Correct")
        else:
            print("Incorrect")
    except ValueError:
        print("Invalid input.")