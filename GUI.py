import tkinter as tk
import tkinter.ttk as ttk


class GUI:
    def __init__(self, test):
        self.test = test
        self.test.generate_test()
        self.test_window = tk.Tk()
        self.generate_test_window()

    def generate_test_window(self):
        self.test_window.title(self.test.name)
        self.test_window.geometry()

        self.display_questions()

        submit_button = ttk.Button(self.test_window, text="Submit", command=self.grade)
        submit_button.grid()

        self.test_window.mainloop()

    def display_questions(self):

        FONT = "Arial"
        NAME_FONT_SIZE = 20
        CATEGORY_FONT_SIZE = 16
        QUESTION_FONT_SIZE = 12
        row = 0

        test_label = ttk.Label(self.test_window)
        test_label.configure(text=self.test.name, font=(FONT, NAME_FONT_SIZE))
        test_label.grid(row=row)

        for category in self.test.categories:

            row += 1
            category_label = ttk.Label(self.test_window)
            category_label.configure(text="\n" + category.name, font=(FONT, CATEGORY_FONT_SIZE))
            category_label.grid(row=row)

            for question in category.questions:

                row += 1
                question_label = ttk.Label(self.test_window)
                question_label.configure(text=question.text + ":", font=(FONT, QUESTION_FONT_SIZE))
                question_label.grid(row=row, column=0)

                question.answer_box = ttk.Combobox(self.test_window)
                question.answer_box.configure(values=question.choices, font=(FONT, QUESTION_FONT_SIZE))
                question.answer_box.grid(row=row, column=1)

    def grade(self):

        self.test.grade_test()

        grade = "\nOverall Score: " + str(self.test.score) + "%"
        test_grade_label = ttk.Label(self.test_window, text=grade)
        test_grade_label.grid()

        breakdown_label = ttk.Label(self.test_window, text="Category Breakdown:")
        breakdown_label.grid()

        for category in self.test.categories:

            category_grade_text = category.name + " Score: " + str(category.score) + "%"
            category_grade_label = ttk.Label(self.test_window, text=category_grade_text)
            category_grade_label.grid()
