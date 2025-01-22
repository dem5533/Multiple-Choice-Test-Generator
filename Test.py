class Question:
    """
    Class to represent a single question.

    Attributes:
        text (str): The question's text (the question itself).
        choices (List[dict]): The question's available answer choices.
        correct_answer (str): The question's correct answer.
        user_answer (str): The user's answer to the question.
        correct (bool): Whether the question is correct or not.
    """

    def __init__(self, data):
        self.text = data["question_text"]
        self.choices = data["choices"]
        self.correct_answer = data["answer"]
        self.user_answer = None
        self.correct = None
        self.answer_box = None

    def __str__(self):
        return f'Question({self.text},{self.choices},{self.correct_answer},{self.user_answer},{self.correct})'

    def grade_question(self):
        """
        Return:
            bool: true if answer is correct, false otherwise
        """
        self.user_answer = self.answer_box.get()
        if self.correct_answer == self.user_answer:
            self.correct = True
        else:
            self.correct = False
        return self.correct


class Category:
    """
    Class to represent a category of questions.

    Attributes:
        name (str): The name of the category.
        questions (List[Question]): The list of questions being used.
        pool (List[Question]): The list of available questions.
        correct (int): The no. of questions gotten correct in the category.
        score (float): The categories score.
    """

    def __init__(self, data):
        self.name = data["Name"]
        self.correct = 0
        self.questions = []
        self.pool = []
        self.score = 0

        for question in data["Questions"]:
            self.pool.append(Question(question))

    def __str__(self):
        return f'Category({self.name},{self.correct},{self.questions},{self.pool})'

    def grade_category(self):
        for question in self.questions:
            if question.grade_question():
                self.correct += 1

    def generate_questions(self, number=None):
        """
        Randomly generates what questions to use from questions in pool.

        Args:
            number (int): The number of questions to generate.
        """
        if number is None:
            number = len(self.pool)
        if number > len(self.pool):
            raise ValueError(
                f'Number of questions requested ({number}) is greater than the pool size ({len(self.pool)})')
        else:
            import random
            nums = random.sample(range(len(self.pool)), number)
            for num in nums:
                self.questions.append(self.pool[num])

    def calculate_score(self):
        self.score = round(self.correct / len(self.questions), 2) * 100

    def display_category_score(self):
        print(self.name + ": " + str(self.correct) + "/" + str(len(self.questions)) + " = " + str(self.score) + "%")


class Test:
    """
    Class to represent a test composed of categories, each containing questions.

    Attributes:
        name (str): The name of the test.
        categories (List[Category]): The list of categories.
        total (int): The total number of questions.
        correct (int): The total number of questions gotten correct.
        score (float): The score of the test.
    """
    def __init__(self, filepath):
        self.name = ""
        self.categories = []
        self.total = 0
        self.correct = 0
        self.score = 0
        self.load_test(filepath)

    def __str__(self):
        return f'Test({self.name},{self.categories},{self.total},{self.correct})'

    def grade_test(self):
        for category in self.categories:
            category.grade_category()
            category.calculate_score()
            self.correct += category.correct
            self.total += len(category.questions)
        self.score = (self.correct / self.total) * 100

    def display_test_score(self):
        print("\nScores:")
        for category in self.categories:
            category.display_category_score()
        print("Total: " + str(self.correct) + "/" + str(self.total) + " = " + str(self.score) + "%")

    def load_test(self, filepath):
        with open(filepath, "r") as f:
            import json
            try:
                data = json.load(f)
            except ValueError:
                print("Error loading .json")
            else:
                self.name = data["Name"]
                for category in data["Categories"]:
                    self.categories.append(Category(category))

    def generate_test(self, number=None):
        """
        Generates questions for test based on number of questions requested per category.

        Arguments:
            number (int): The number of questions per category.
            number (ist[int]): List of no. of questions to add per category.
        """
        if number is None:
            for category in self.categories:
                category.generate_questions()
        elif isinstance(number, int):
            for category in self.categories:
                category.generate_questions(number)
        elif isinstance(number, list):
            if len(number) != len(self.categories):
                raise ValueError("Number of categories requested does not match number of categories available")
            else:
                for category, num in zip(self.categories, number):
                    category.generate_questions(num)
        else:
            raise ValueError("Number of questions per category must be an integer or a list of integers")
