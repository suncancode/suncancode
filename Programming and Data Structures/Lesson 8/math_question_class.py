# This file demonstrate designing the MathQuestion class

import random

class MathQuestion:
    """
    Represents a math question with attributes:
    number1: first number
    number2: second number
    operation: +, -, x, /
    solution: correct answer
    """
    def __init__(self, number1, number2, operation, solution):
        self.number1 = number1
        self.number2 = number2
        self.operation = operation
        self.solution = solution

    def __str__(self):
        return "{0} {1} {2} = {3}".format(
            self.number1,
            self.operation,
            self.number2,
            self.solution
        )
    
    def question_text(self):
        """
        Rerturns the question text without the solution
        """
        return "{0} {1} {2} = ".format(
            self.number1,
            self.operation,
            self.number2,
        )
    
    def check_answer(self, answer):
        """
        Returns True if the answer matchs the solution
        """
        return answer == self.solution
    
    @staticmethod
    def generate_question_add():
        """
        Generate a random addtion question
        """
        operation = "+"
        number1 = random.randint(0, 20)
        number2 = random.randint(0, 20)
        solution = number1 + number2
        return MathQuestion(number1, number2, operation, solution)
    
    @staticmethod
    def generate_question_subtract():
        """
        Generate a random subtraction question
        """
        operation = "-"
        number1 = random.randint(0, 20)
        number2 = random.randint(0, 20)
        solution = number1 - number2
        return MathQuestion(number1, number2, operation, solution)
    
    @staticmethod
    def generate_question_multiply():
        """
        Generate a random multiplication question
        """
        operation = "x"
        number1 = random.randint(0, 20)
        number2 = random.randint(0, 20)
        solution = number1 * number2
        return MathQuestion(number1, number2, operation, solution)
    
    @staticmethod
    def generate_question_divide():
        """
        Generate a random division question
        """
        operation = "/"
        number1 = random.randint(0, 20)
        number2 = random.randint(0, 20)
        solution = number1 / number2
        return MathQuestion(number1, number2, operation, solution)
    
    @staticmethod
    def generate_question():
        """
        Generate a random question of anytype
        """
        question_type = random.randint(1, 4)
        if question_type == 1:
            return MathQuestion.generate_question_add()
        elif question_type == 2:
            return MathQuestion.generate_question_subtract()
        elif question_type == 3:
            return MathQuestion.generate_question_multiply()
        else:
            return MathQuestion.generate_question_divide()
        
