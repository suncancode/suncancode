def get_assessment_mark(assessment_name, mark_min, mark_max):
    # Check if assessment name is Assignment 1, mark_min = 0, mark_max = 20
    if (
        assessment_name == "Assignment 1",
        mark_min == 0,
        mark_max == 20
    ):
        # Check if user input is a non-integer
        try:
            user_input = input("Enter {0} mark ({1}-{2}): ".format(assessment_name, mark_min, mark_max))
            mark = int(user_input)
        except ValueError:
            raise ValueError("{0} mark is invalid".format(assessment_name))
        
        # Check if user enter a valid mark between the correct range
        if mark < mark_min or mark > mark_max:
            raise ValueError("{0} mark must be between {1} and {2}".format(assessment_name, mark_min, mark_max))
        
        return mark
