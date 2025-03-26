import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb


class Init_Frame:
    def __init__(self, root, test):
        self.root = root
        self.test = test
        self.selected_template_size = tk.StringVar()
        self.selected_template_size.set(None)
        self.custom_sizes = []

        self.init_frame = ttk.Frame(root,
                                    padding=5,
                                    borderwidth=5,
                                    relief=tk.SOLID)
        self.init_frame.pack()

        self.init_label = ttk.Label(self.init_frame,
                                    text="Create your custom test:",
                                    padding=(3, 3, 3, 0))
        self.init_label.pack()

        self.options_frame = ttk.Frame(self.init_frame, padding=10, borderwidth=5, relief=tk.SOLID)
        self.options_frame.pack(padx=5, pady=5, fill=tk.X)

        self.template_frame = self.create_template_frame(self.options_frame, test)
        self.template_frame.grid(row=0, column=0)

        self.custom_frame = self.display_custom_frame(self.options_frame, test)
        self.custom_frame.grid(row=0, column=1)

    def create_template_frame(self, root, test):
        template_frame = ttk.Frame(root, padding=(5, 5, 5, 5))

        template_label = ttk.Label(template_frame, text="Template Test:")
        template_label.grid(row=0, column=0)

        i = 1
        for size in list(test.template_category_sizes.keys()):
            r = tk.Radiobutton(template_frame,
                               text=size,
                               value=size,
                               variable=self.selected_template_size)
            r.grid(row=i, column=0)
            i += 1

        template_button = ttk.Button(template_frame,
                                     text="Create Template Test",
                                     command=self.generate_template_test)
        template_button.grid(row=len(test.template_category_sizes) + 1, column=0)

        return template_frame

    def display_custom_frame(self, root, test):
        custom_frame = ttk.Frame(root, padding=(5, 5, 5, 5))

        custom_label = ttk.Label(custom_frame, text="Custom Test:")
        custom_label.grid(row=0, column=0)

        i = 1
        for category in test.categories:
            l: ttk.Label = ttk.Label(custom_frame, text=category.name + ":")
            l.grid(row=i, column=0)
            size = tk.StringVar()
            self.custom_sizes.append(size)
            e: ttk.Entry = ttk.Entry(custom_frame, width=5, textvariable=size)
            e.grid(row=i, column=1)
            i += 1

        custom_button = ttk.Button(custom_frame,
                                   text="Create Custom Test",
                                   command=self.generate_custom_test)
        custom_button.grid(row=len(self.custom_sizes) + 1, column=0)

        return custom_frame

    def generate_template_test(self):
        template_array = self.test.template_category_sizes.get(self.selected_template_size.get())
        self.test.generate_test(template_array)
        self.init_frame.destroy()
        Test_Frame(self.root, self.test)

    def generate_custom_test(self):

        category_sizes = []

        for custom_size, category in zip(self.custom_sizes, self.test.categories):
            if custom_size.get() == '':
                mb.showwarning(title="Warning!",
                               message=f'{category.name} value is empty!')
            elif not custom_size.get().isnumeric():
                mb.showwarning(title="Warning!",
                               message=f'Size for category "{category.name}" is not a number!')
            elif int(custom_size.get()) > len(category.pool):
                mb.showwarning(title="Warning!",
                               message=f'Size {custom_size.get()} for category "{category.name}"'
                                       f' is bigger than categories pool ({len(category.pool)})!')
            else:
                category_sizes.append(int(custom_size.get()))

        self.test.generate_test(category_sizes)
        self.init_frame.destroy()
        Test_Frame(self.root, self.test)


class Test_Frame:
    def __init__(self, root, test):
        self.root = root
        self.test = test
        self.response = tk.StringVar()
        self.response.set(None)
        self.questions = []
        for category in test.categories:
            for question in category.questions:
                self.questions.append(question)
        self.question_index = 0
        self.question_frame = None

        self.test_frame = ttk.Frame(root, padding=5)
        self.test_frame.pack()

        self.display_question(self.questions[self.question_index])

        self.nav_frame = ttk.Frame(self.test_frame, padding=5)
        self.nav_frame.grid(row=1, column=0)

        self.prev_button = ttk.Button(self.nav_frame,
                                      text="Previous",
                                      command=self.prev_question)
        self.prev_button.grid(row=0, column=0)

        self.next_button = ttk.Button(self.nav_frame,
                                      text="Next",
                                      command=self.next_question)
        self.next_button.grid(row=0, column=1)

    def display_question(self, question):
        self.response.set(question.user_answer)
        self.question_frame = ttk.Frame(self.test_frame, padding=5)
        self.question_frame.grid(row=0, column=0)

        question_label = ttk.Label(self.question_frame, text=question.text)
        question_label.grid()

        for choice in question.choices:
            r = tk.Radiobutton(self.question_frame, text=choice, value=choice, variable=self.response)
            r.grid()

    def next_question(self):
        if self.response.get() is None:
            mb.showwarning(title="Warning!",
                           message="Please select an answer before moving on.")
        else:
            self.questions[self.question_index].user_answer = self.response.get()
            self.question_frame.destroy()
            self.question_index += 1
            if self.question_index == len(self.questions) - 1:
                self.next_button.configure(text="Submit", command=self.submit_test)
            self.display_question(self.questions[self.question_index])

    def prev_question(self):
        if self.question_index == 0:
            mb.showwarning(title="Warning!",
                           message="No previous question in test.")
        else:
            if self.question_index == len(self.questions) - 1:
                self.next_button.configure(text="Next", command=self.next_question)
            self.questions[self.question_index].user_answer = self.response.get()
            self.question_frame.destroy()
            self.question_index -= 1
            self.display_question(self.questions[self.question_index])

    def submit_test(self):
        self.questions[self.question_index].user_answer = self.response.get()
        self.test.grade_test()
        self.test_frame.destroy()
        Score_Window(self.root, self.test)


class Score_Window:
    def __init__(self, root, test):
        self.root = root
        self.test = test

        self.categories = []
        for category in test.categories:
            self.categories.append(category)
        self.category_index = 0

        self.score_frame = ttk.Frame(self.root, padding=5, borderwidth=5, relief=tk.SOLID)
        self.score_frame.pack()

        self.display_frame = None
        self.nav_frame = None
        self.next_button = None
        self.prev_button = None

        self.display_score_overview()

    def display_score_overview(self):

        self.display_frame = ttk.Frame(self.score_frame, padding=5)
        self.display_frame.grid(row=0, column=0)

        score_label = ttk.Label(self.display_frame,
                                text="Overall Score: " + str(self.test.score) + "%",
                                font=("Arial", 20))
        score_label.grid()

        for category in self.categories:
            category_label = ttk.Label(self.display_frame,
                                       text=category.name + ": " + str(category.score) + "%",
                                       font=("Arial", 15))
            category_label.grid()

        self.nav_frame = ttk.Frame(self.score_frame, padding=5)
        self.nav_frame.grid(row=1, column=0)

        breakdown_button = ttk.Button(self.nav_frame,
                                      text="Question Breakdown",
                                      command=self.init_question_breakdown)
        breakdown_button.pack()

    def init_question_breakdown(self):

        self.nav_frame.destroy()

        self.nav_frame = ttk.Frame(self.score_frame, padding=5)
        self.nav_frame.grid(row=1, column=0)

        self.display_category()

    def display_category(self):

        self.display_frame.destroy()

        self.display_frame = ttk.Frame(self.score_frame, padding=5)
        self.display_frame.grid(row=0, column=0)

        category_label = ttk.Label(self.display_frame,
                                   text="Category: " + self.categories[self.category_index].name,
                                   font=("Arial", 15))
        category_label.grid()

        category_score_label = ttk.Label(self.display_frame,
                                         text="Score: " + str(self.categories[self.category_index].score) + "% - " +
                                              str(self.categories[self.category_index].correct) + "/" +
                                              str(self.categories[self.category_index].total),
                                         font=("Arial", 15))
        category_score_label.grid()

        for question in self.categories[self.category_index].questions:
            question_label = ttk.Label(self.display_frame, font=("Arial", 10))
            if question.user_answer == question.correct_answer:
                question_label.configure(text="\n" + question.text + ": Correct - " + question.user_answer)
            else:
                question_label.configure(text="\n" + question.text + ": Incorrect\nYour answer: " +
                                              question.user_answer + "\nCorrect answer: " + question.correct_answer)
            question_label.grid()

        if self.category_index > 0 and self.prev_button is None:
            self.prev_button = ttk.Button(self.nav_frame,
                                          text="Previous",
                                          command=self.prev_category)
            self.prev_button.grid(row=0, column=0)

        if self.category_index < len(self.categories) - 1 and self.next_button is None:
            self.next_button = ttk.Button(self.nav_frame,
                                          text="Next",
                                          command=self.next_category)
            self.next_button.grid(row=0, column=1)

    def prev_category(self):
        if self.category_index == 0:
            mb.showwarning(title="Warning!",
                           message="No previous category to display scores for!.")
        else:
            self.category_index -= 1
            if self.category_index == 0:
                self.prev_button.destroy()
                self.prev_button = None
            self.display_category()

    def next_category(self):
        if self.category_index == len(self.categories) - 1:
            mb.showwarning(title="Warning!",
                           message="No next category to display scores for!")
        else:
            self.category_index += 1
            if self.category_index == len(self.categories) - 1:
                self.next_button.destroy()
                self.next_button = None
            self.display_category()
            