import Test

test = Test.Test('example_test.json')
test.generate_test(1)

for category in test.categories:
    print(category.name)
    for question in category.questions:
        print(question.text)
        for choice in question.choices:
            print(choice)
        question.user_answer = input("Enter your answer:")

test.grade_test()
test.display_test_score()
