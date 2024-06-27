import re # data cleaning
import ctypes # to use c func i putted in other file
import random # randomly choose gay type for who failed
import difflib # for name searching typo-insensitive
import numpy as np # i forgot why the hell i added it maybe i was working on something and changed plans
from IPython.display import HTML, display # for color thingie
import sqlite3 # to use sql
from google.colab import files # I'm working on Google colab so i use this to download the database
from itertools import zip_longest

print("been waiting for you\nGAY-DAR ON\n")

# the gay key
PASS_CST = 10

# gay type ( there are like 70 ish of it i included only LGBTQIA )
SPECIES = ["106", "lesbian", "gay", "bisexual", "transgender", "queer", " intersex", "asexual", "FALLAH", "Women ☕"]

# Easter egg
TONY = "IMADEDDINE LOUEI"
STARK = "TAHA NASREDDINE"
JAMES = "AYMEN KHEIR EDDINE"

# Replace commas with dots in the file
!sed -i 's/,/./g' markS1.txt markS2.txt

# Define the struct in Python using ctypes
class CFuncData(ctypes.Structure):
    _fields_ = [("gay_num", ctypes.c_int),
                ("gay_precent", ctypes.c_double)]

# Read and split the content of both files simultaneously
with open('markS1.txt', 'r') as file1, open('markS2.txt', 'r') as file2:
    lines1 = file1.read().split('\n')
    lines2 = file2.read().split('\n')

# Initialize an empty dictionary to store student marks
students = {}

# Define a regular expression pattern to extract floating-point numbers and names
patternForNum = re.compile(r'\d+\.\d+')
patternForNames = re.compile(r'[^a-zA-Z\s]')

for line in lines1:
    if line:
        student_name = re.sub(patternForNames, '', line)
        students[student_name.strip()] = {}

# reading student information and add students
def reader(line, num, lowkey):
    # Extract the student name (remove non-alphabetic characters)
    student_name = re.sub(patternForNames, '', line)
    # top secret soldier information
    soldier_information = "232337099604"
    # Store the student name and mark in the dictionary
    if student_name.strip() not in students:
        return
    students[student_name.strip()][lowkey] = float(num[-1])
    if soldier_information in line:
        if "flag" not in students[student_name.strip()]:
            students[student_name.strip()]["flag"] = "🦇"


# Iterate over each line in both file
for line1, line2 in zip_longest(lines1, lines2, fillvalue=''):
    # Skip empty lines
    if line1.strip():

        # Extract all floating-point numbers from the line
        nums = re.findall(patternForNum, line1)

        # If there are no numbers found, skip this line
        if nums:

            reader(line1,nums, "grade S1")

    # Skip empty lines
    if line2.strip():

        # Extract all floating-point numbers from the line
        nums = re.findall(patternForNum, line2)

        # If there are no numbers found, skip this line
        if nums:

            reader(line2,nums, "grade S2")


#  Extract grades into separate arrays
grades_s1 = []
grades_s2 = []

for student, info in students.items():
    # Get "grade S1" if it exists, otherwise append 0
    grades_s1.append(info.get("grade S1", 0))
    # Get "grade S2" if it exists, otherwise append 0
    grades_s2.append(info.get("grade S2", 0))
for student, info in students.items():
    if "grade S1" not in info:
        students[student]["grade S1"] = 0
    if "grade S2" not in info:
        students[student]["grade S2"] = 0
# Number of students
studentsNum = len(grades_s1)

# Load the shared library into ctypes
_sum_double_arrays = ctypes.CDLL('./sum_double_arrays.so')

# build a c data type in python
array_type = ctypes.c_double * studentsNum

# defining c arrays to pass'm into the c func
array_a = array_type(*grades_s1)
array_b = array_type(*grades_s2)
array_c = array_type()

#calling c func
_sum_double_arrays.sum_double_arrays(array_a, array_b, array_c, studentsNum)
result = list(array_c)


# put the sum in the dictionary with other student's info
for student, total in zip(students.keys(), result):
    # Add the sum to the student's dictionary
    students[student]['sum'] = total

# Convert marks list to a C array

# Load the shared library into ctypes
libeCalc = ctypes.CDLL('./libeCalc.so')

# Declare the return type of the function
libeCalc.gayPercent.restype = CFuncData

# Call the function gayPercent from the library
gay_stat = libeCalc.gayPercent(array_c, studentsNum)


#sorting to get top 10 based on...
def sorter(lowkey):
    return sorted(students.items(), key=lambda item: item[1].get(lowkey, 0), reverse=True)[:10]

#s1 grade
top_s1 = sorter("grade S1")

#s2's
top_s2 = sorter("grade S2")

#and bothe of'm
top_sum = sorter("sum")

top_comeback = sorted(students.items(), key=lambda item: (item[1].get("grade S2", 0) - item[1].get("grade S1", 0)), reverse=True)[:10]

print(f"There are {gay_stat.gay_num} gay out of {studentsNum} students\n"
      f"Or in more fashion way, {gay_stat.gay_precent:.4}% is the percentage of gays in class")

# printing top students based on the sort reasntly
def printer(top):
    for index, (student, info) in enumerate(top, start=1):
        b = ""
        if "flag" in info:
            b = "🦇"
        elif STARK in student:
            b = "🤖"
        grade_s1 = info.get("grade S1", "N/A")
        grade_s2 = info.get("grade S2", "N/A")
        avr_year = info.get("sum", "N/A")
        print(f"{index} - {student}{b}: grade S1: {grade_s1}, grade S2: {grade_s2}, year avr: {avr_year:.4}")

# Print the first ten students with their grades
print("\non the other hand men on top s1:")

printer(top_s1)

print("\nmen on top s2:")

printer(top_s2)

print("\nmen on top overall:")

printer(top_sum)

print("\n best academic comeback:")

printer(top_comeback)

# Function to return word in gay colors as HTML
def get_rainbow_word_html(word):
    gay_flag = ['red', 'orange', 'yellow', 'green', 'blue', 'violet']
    # Ensure the colors cycle through the word
    gay_word = ''.join([f"<span style='color: {gay_flag[i % len(gay_flag)]};'>{letter}</span>"
                            for i, letter in enumerate(word)])
    return gay_word

# check if your friend is gay
def find_student(name):
    # Convert the input and student names to lowercase for case-insensitive comparison
    name = name.lower()
    student_names = [s.lower() for s in students.keys()]

    # Use difflib to find the closest match to the input name
    closest_match = difflib.get_close_matches(name, student_names, n=1, cutoff=0.4)

    if closest_match:
        # Find the original case of the closest match
        closest_name = [key for key in students.keys() if key.lower() == closest_match[0]][0]
        student_info = students[closest_name]

        # deciding gender randomly
        gender = random.choice(SPECIES) if student_info.get("sum", 0) < PASS_CST else "straight"

        if "flag" in students[closest_name]:
            gender = "Batman 🦇"
        # I'm Iron man( but not billionaire)
        if STARK in closest_name:
            gender = "Ironman 🤖"
        elif TONY in closest_name:
            gender = "Engineer 🧰"
        elif JAMES in closest_name:
            gender = "Iron Patriot 🤖"

        print(f"Student: {closest_name}\n"
              f"Grade S1: {student_info.get('grade S1', 'N/A')}\n"
              f"Grade S2: {student_info.get('grade S2', 'N/A')}\n"
              f"Gender: {gender}")
    elif name:
        print("No match found")


# write the name you're looking for
name = input("lookin for someone? ")

find_student(name)

# press enter with empty input to end
while name:
    name = input("again? ")
    find_student(name)

answer = input("wanna display gender list? ")

answer = answer.lower()
closest_answer = difflib.get_close_matches(answer, "yes", n=1, cutoff=0.4)
if closest_answer:
    for index, (student, grades) in enumerate(students.items(), start=1):
        if students[student]['sum'] < PASS_CST:
            gender = random.choice(SPECIES)
            normal_text = f"<span>{index} - {student} S1: {students[student]['grade S1']} S2: {students[student]['grade S2']} </span>"
            gay_text_html = get_rainbow_word_html(gender)
            display(HTML(normal_text + gay_text_html))
            continue

        if "flag" in students[student]:
            gender = "Batman 🦇"
        elif STARK in student:
            gender = "Ironman 🤖"
        elif TONY in student:
            gender = "Engineer 🧰"
        elif JAMES in student:
            gender = "Iron Patriot 🤖"
        else:
            gender = "straight"

        # Concatenate and display the normal text and the gay-flag-colored word
        normal_text = f"<span>{index} - {student} S1: {students[student]['grade S1']} S2: {students[student]['grade S2']} {gender}</span>"
        display(HTML(normal_text))
else:
    print("no? alright than bye bye sunshine")

print("\nGAY-DAR OFF")

# Connect to the database
conn = sqlite3.connect('student_statistics.db')
c = conn.cursor()

# Read SQL from the .sql file
with open('student_database.sql', 'r') as sql_file:
    sql_script = sql_file.read()

# Execute the SQL script
c.executescript(sql_script)

# Iterate over the dictionary and insert data
for student, info in students.items():
    Class = "Rattrapage" if info['sum'] < PASS_CST else "pass"

    c.execute('''
    INSERT INTO students (Name, "Grade S1", "Grade S2", "Year Average", Class)
    VALUES (?, ?, ?, ?, ?)
    ''', (student, info['grade S1'], info['grade S2'], info['sum'], Class))

# Commit the changes and close the connection
conn.commit()
conn.close()
files.download('student_statistics.db')