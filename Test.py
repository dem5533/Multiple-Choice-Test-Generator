class Question:
    def __init__(self, data):
        self.text = data["question_text"]
        self.choices = data["choices"]
        self.correct_answer = data["answer"]
        self.user_answer = None
        self.correct = None

    def __str__(self):
        return f'Question({self.text},{self.choices},{self.correct_answer},{self.user_answer},{self.correct})'

    def grade(self):
        if self.correct_answer == self.user_answer:
            self.correct = True
        else:
            self.correct = False
        return self.correct


class Category:
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

    def grade(self):
        for question in self.questions:
            if question.grade():
                self.correct += 1

    def generate_questions(self, number):
        import random
        nums = random.sample(range(len(self.pool)), number)
        for num in nums:
            self.questions.append(self.pool[num])

    def calculate_score(self):
        self.score = round(self.correct / len(self.questions), 2) * 100

    def display_score(self):
        print(self.name + ": " + str(self.correct) + "/" + str(len(self.questions)) + " = " + str(self.score) + "%")


class Test:
    def __init__(self, filepath):
        self.name = ""
        self.categories = []
        self.total = 0
        self.correct = 0
        self.score = 0
        self.load_test(filepath)

    def __str__(self):
        return f'Test({self.name},{self.categories},{self.total},{self.correct})'

    def grade(self):
        for category in self.categories:
            category.grade()
            category.calculate_score()
            self.correct += category.correct
            self.total += len(category.questions)
        self.score = round(self.correct / self.total, 2) * 100

    def add_category(self, category):
        self.categories.append(category)
        self.total += category.total

    def display_score(self):
        print("\nScores:")
        for category in self.categories:
            category.display_score()
        print("Total: " + str(self.correct) + "/" + str(self.total) + " = " + str(self.score) + "%")

    def load_test(self, filepath):
        import json
        with open(filepath, "r") as f:
            data = json.load(f)
            self.name = data["Name"]
            for category in data["Categories"]:
                self.categories.append(Category(category))
