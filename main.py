import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import mysql.connector as mys

name = input("Please enter the students name: ")

myconnect = mys.connect(host="localhost", user="root", passwd="123", database="marks")
cursor = myconnect.cursor()

L = []
k = []
cursor.execute("show tables")
for i in cursor:
    k.append(i)

students = []
for i in range(len(k)):
    students.append(k[i][0])

while True:
    if name not in students:
        print("Sorry, the student doesn't exist in the database")
        print("Available tables are: ", students)
        name = input("Please enter a valid student name: ")
    else:
        break

records = "select * from {}".format(name)
cursor.execute(records)
for i in cursor:
    print("\nGrade: ", i[0], "|", "Exam: ", i[1], "|", "Overall Percentage: ", i[2])
    L.append(i[2])

#  Performing various SQL operations


def sqloperations():
    while True:
        operation = int(input("""\nPlease enter the operation you want to perform
        1) Update an element
        2) Add new record
        3) Quit
        Your Selection (Serial No.): """))
        if operation == 1:
            col1 = int(input("""\nPlease enter the exam you wish to amend
             Your options are:
            1) cyt1
            2) cyt2
            3) mid term
            4) cyt3
            5) cyt4
            6) annual exam
            Your selection (Serial No.): """))
            sel = {1: "cyt1", 2: "cyt2", 3: "midterm", 4: "cyt3", 5: "cyt4", 6: "annualexam"}
            g1 = int(input("\nEnter the grade in which you wish to make the amendment (11 or 12): "))
            nv = int(input("\nPlease enter the new value you wish to add: "))
            query = """update {0} set overallpercentage = {1} where grade = {2} and exam = "{3}" """.format(name, nv, g1, sel[col1])
            cursor.execute(query)
            cursor.commit()
            print("\nRecord Updated")
            desc = input("\nWould you like to modify the records further (y,n) ?  ")
            if desc in "Nn":
                break
            else:
                sqloperations()
        elif operation == 2:
            g3 = int(input("\nEnter the grade in which you would like to add a new record: "))
            exam = int(input("""\nPlease enter the exam you wish to add
             Your options are:
            1) cyt1
            2) cyt2
            3) mid term
            4) cyt3
            5) cyt4
            6) annual exam
            Your selection (Serial No.): """))
            sel = {1: "cyt1", 2: "cyt2", 3: "midterm", 4: "cyt3", 5: "cyt4", 6: "annualexam"}
            g4 = int(input("enter the overall percentage: "))
            query = "insert into {0} values({1},'{2}',{3})".format(name, g3, sel[exam], g4)
            cursor.execute(query)
            cursor.commit()
            print("\nRecord Updated")
            desc = input("\nWould you like to modify the records further (y,n) ?  ")
            if desc in "Nn":
                break
        elif operation == 3:
            break

        details = input("Are you satisfied with your dataset? (y/n)")
        if details in "Nn":
            sqloperations()
        else:
            print("\nPerfect!")
            break


details = input("\nPlease enter 'y' if the details are correct or 'n' if the details are to be amended: ")
if details not in "Nn" and details not in "Yy":
    details = input("Please enter a valid choice(y/n): ")
else:
    if details in "Nn":
        sqloperations()

# Prediction
sel1 = {1: "cyt1", 2: "cyt2", 3: "midterm", 4: "cyt3", 5: "cyt4", 6: "annualexam"}
sel = {1: [11.16], 2: [11.32], 3: [11.5], 4: [11.6], 5: [11.82], 6: [12]}

o = ["cyt1", "cyt2", "midterm", "cyt3", "cyt4", "annualexam"]

print("\nPlease enter the Grade 12 exam you wish to predict")

cursor.execute("select * from {} where grade = 12".format(name))
i = 0
n = []
for j in o[len(cursor.fetchall()):]:
    print("{}) {}".format(i+1, j))
    i += 1
    n.append(j)
h = list(sel1.keys())  # all the serial numbers
f = list(sel1.values())  # all the exams
t = {}
for i in n:
    t[f.index(i) + 1] = i

exam2 = int(input("\nYour selection: ")) + len(n)

eno = [10.16, 10.32, 10.5, 10.66, 10.82, 11, 11.16, 11.32, 11.5, 11.66, 11.82, 12]
cursor.execute("select * from {}".format(name))
elements = len(cursor.fetchall())
len1 = eno[0: elements]

a = pd.DataFrame(len1)  # grades
b = pd.DataFrame(L)  # overall percentage

x = np.array(a).reshape(-1, 1)
y = np.array(b).reshape(-1, 1)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)
clf = LinearRegression()
clf.fit(x_train, y_train)

print("\n{0}'s overall predicted score in {1} is: ".format(name, t[exam2]), round(clf.predict([sel[exam2]])[0][0]), "%")
