# Multiple Choice Test Generator

Software to create, proctor, and grade a multiple choice test.

A test composed of categories, and each category is composed of questions. 
The categories and questions are loaded in from a user provided .json file. 
Each category contains a pool of questions that the test pulls from randomly during test generation. 

The generated test can be customized to change the number of questions from each category that appears in the test.  
The test can also be generated from a list of predefined templates
that contain standard numbers of questions per category.

## How to run this program:

To use this program, you must have a python interpreter installed.
The easiest way is to install the python language package.

### Download and install python:

First, download python from www.python.org/downloads by clicking the yellow button labeled "Download Python 3.XX.X."  

Next, launch the executable and follow the installation wizard to install python.  
Use all default options using the "Install Now" options.  

Python and its interpreter should now be installed on your system!

### Launch the program:

I don't have a machine that runs macOS, so I can't go over that here,
and if you run Linux, you should hopefully be able to figure out how to run a python script on your own,
so I'm only going to be covering Windows here. 

First, you need to download the repo. 
To do this, on the GitHub page go to the green `<> Code` button, click it, and click `Download ZIP`.
Unzip this package where ever you'd like (desktop would probably be easiest).

Now, open command prompt. The easiest way to do this is by typing `cmd` in your Windows search bar and hit 'enter'. 

In your command prompt window, you will need to switch the "working directory" to the unzipped program.
To do this, you will run the command:

`cd [directory]`

Where the [directory] is the location of the unzipped program.
If the program folder is on your desktop, this should be "C:\Users\[usr]\Desktop\Multiple-Choice-Test-Generator",
where [usr] is your username.
This will make the command look like:

`cd C:\Users\[usr]\Desktop\Multiple-Choice-Test-Generator`

If this worked,
the text to the left of your typing cursor should be `C:\Users\[usr]\Desktop\Multiple-Choice-Test-Generator`.

Once you have changed the directory, to run the program, you type:

`python Main.py`

and the program should launch. 

## How to edit test.json

Open the test.json file in your JSON editor of choice (notepad will work for this).

It should look like this:

    {
      "Name":"Example Test",
      "Templates": [
        {
          "Short":  [1, 1, 1, 1]
        },
        {
          "Medium": [2, 2, 2, 2]
        },
        {
          "Long":   [3, 3, 3, 3]
        }
      ],
      "Categories":[
        {
          "Name": "Science",
          "Questions": [
            {
              "question_text": "What is the color of the sky?",
              "choices": [
                  "A: Red",
                  "B: Yellow",
                  "C: Green",
                  "D: Blue"
              ],
              "answer": "D: Blue"
            },
            ...
          ]
        },
        {
          "Name": "English",
          "Questions": [
            {
              "question_text": "What category of word is 'Run'?",
              "choices": [
                "A: Verb",
                "B: Noun",
                "C: Adverb",
                "D: Pronoun"
              ],
              "answer": "A: Verb"
            },
            ...
          ]
        }
        ...
      ]
    }

It may look confusing, but don't worry, we'll break it down section by section.  
First, a little crash-course on JSON files.

### JSON crash course:

Information is stored in key/value pairs. These take the form of: `"Key":"Value"`

A key **must** a string (text) inside double quotation marks: `"..."`  
A value can either be a string, object, or list for this program.

An object is denoted by curly brackets: `{...}`  
Objects store key/value pairs.

A list is denoted by square brackets: `[...]`  
Lists can store strings, key/value pairs, or objects. 

Elements (key/value pairs and objects) in objects/lists are seperated by commas: `,`  
If additional elements need to be stored in an object or list,
you **must** separate them with a comma after the previous element.  
If an object or list is ending, there **cannot** be a comma.

**These special characters are the most important thing to remember.**  
*If a bracket is missing, the JSON will not load.*  
*If a double quote is missing, the JSON will not load.*  
*If there is a comma without an element after it, the JSON will not load.*  
*If there isn't a comma where there should be a comma, the JSON will not load.*  

There can be additional spaces/indents or newlines and the JSON will load properly.

### NOTE: There is only one time you will be editing the keys in a key/value pair. If you edit a key in any other instance, the JSON will not load.

To ensure the JSON was written properly, I recommend running it through a JSON validator.
You can use https://jsonformatter.curiousconcept.com/.

Just copy and paste it into the field and click 'process'.
It will tell you if it's formated properly, and adjust the spaces/newlines to follow JSON standards.

Now, onto the file formatting breakdown.

### Test object:

To start off, we'll look at the test object.  
The test object is bounded by the outermost curly braces.  
It holds 3 elements, *Name*, *Templates*, and *Categories*:

    {
      "Name":"Example Test",
      "Templates":[
      ...
      ],
      "Categories":[
      ...
      ]
    }

The `Name` will be the name of the test.
The `Name` key cannot be changed, only the value paired with it.  
The `Templates` holds a list of templates the test can be generated from.  
The `Categories` holds a list of categories the test is composed of. 

Now we'll break down the templates and categories:

### Templates:

The `Templates` key/value pair looks like:

    "Templates": [
      {
        "Short":  [1, 1, 1, 1]
      },
      {
        "Medium": [2, 2, 2, 2]
      },
      {
        "Long":   [3, 3, 3, 3]
      }
    ],

The key `Templates` **cannot** be changed or the JSON will not load.  
The value of `Templates` is a list of templates to generate the test from.
Each element in this value list has an object storing a key/value pair for each template specification.
This is the information you will be editing. 

The key for each template object will be the name of the template that appears in the program.  
The value for each template is a list containing the number of questions from each category to generate for the test. 

### IMPORTANT NOTES: 
#### This is the *only* time you will be editing keys of key/value pairs. If you edit any other keys outside the template objects, the JSON will not load.
#### The quantity of numbers in each template value list must match the number of categories in the test.json file. If you don't want a category to appear, a 0 **must** be inserted. If the number of values in each list does not match the no. of categories, the JSON will not load. 

Other interesting notes:
1. The number of templates is dynamic! You can add or remove as many templates as you would like. 
2. There will automatically be a `Full` template option that generates a test with *every* question in *every* category.  
There is no need to add one here in the JSON.

### Categories:

The `Categories` key/value pair looks like:

    "Categories": [
      {
      ...
      },
      ...
      {
      ...
      }
    ]

The key `Categories` **cannot** be changed or the JSON will not load. 
As previously stated, no key in a key/value pair should be changed from here on out. 
*This will be the last time this is stated.*  
The value of `Categories` is a list of objects that will hold each category for the test.
This is the information you will be editing.

If you don't want to break the test down into categories, just put ever question into a single category.
Make sure the template lists only have a single number in them *but are still in lists bounded buy square brackets*.

Each category looks like:

    {
      "Name":"Science",
      "Questions":[
        {
        ...
        },
        ...
        {
        ...
        }
      ]
    }

The value of the `Name` key is the name of the category.  
The value of the `Questions` key is a list of objects that hold a question the program can choose from.

Finally, we'll break down how the questions are stored:

### Questions:

A question object looks like:

    {
      "question_text": "What is the color of the sky?",
      "choices": [
        "A: Red",
        "B: Yellow",
        "C: Green",
        "D: Blue"
      ],
      "answer": "D: Blue"
    }

The value of the `question_text` key will be the text of the question being asked. 
The value of the `choices` key is a list of strings that hold answers for the user to choose from.  
The value of the `answer` key will be the correct answer to the given question.

The number of choices in the `choices` value is fully dynamic. 
There can be as many or as few choices as you would like. 
You can do true/false questions with two choices, 4 or 5 choice multiple choice questions,
or 100 choices if you really feel like it (the display might run off the screen in that event though).

### IMPORTANT NOTE:
#### The `answer` value string and the corresponding `choices` string must be *identical* for grading to mark it as correct. If a single character is out of place, it will mark the choice incorrect.

### Wrap up

That should be everything you need to get the program up and running and studying your own custom test! 

Happy studying!