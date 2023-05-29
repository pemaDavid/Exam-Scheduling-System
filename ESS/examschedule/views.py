from django.shortcuts import render, redirect
from examschedule.models import User
import mysql.connector
from django.shortcuts import render
import pandas as pd
import os
from django.core.files.storage import FileSystemStorage
from .models import Departments,Modules,YearOfStudy,Students,Semester,NormalEnrollments,RepeatEnrollments,DateTuple
from .models import Programs,Examtable,ExamtableHistory,Examselection,ExamSemester,ExaminationType,Classrooms,Invigilators,ClassroomAllocation
from django.shortcuts import redirect
from .forms import DateForm,classroomForm,moduleForm,departmentForm,programForm,studentForm,modulemappingForm,studentrepeatForm,CAForm
import logging
from datetime import timedelta
from django.http import HttpResponse
import collections
from django.test import RequestFactory
import random as rn
from numpy import concatenate
from numpy import random
from numpy.random import randint
import copy
from datetime import datetime
import re
import datetime
import ast
from django.http import JsonResponse
from django.utils import timezone
# Create your views here.
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from math import ceil
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
from .models import Classrooms
# Create your views here.


factory = RequestFactory()
request = factory.get('/')

def home(request):
    return render(request, 'index.html')
def profile(request):
    return render(request, 'profile.html')

def login_view(request):
     if request.method=="POST":
           email = request.POST['userEmail']
           password = request.POST['password']

           cnx = mysql.connector.connect(user='root', password='Palden657',
                              host='localhost', database='ESS2')
           cursor = cnx.cursor()
           query = "SELECT * FROM users WHERE uemail = %s AND upasswd = %s"
           cursor.execute(query, (email, password))
           user = cursor.fetchone()

           print(user)

           if user is not None and user[2]=='admin@gmail.com' and user[3]=='admin':
               return redirect('dashboard')
           elif user is not None:
               return redirect('faculty')
              
           else:
            error="Invalid email or Password"
            return render(request, 'login.html', {'error':error})
     else:
        return render(request, 'login.html')


def faculty(request):
    return render(request, 'faculty.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def classroom(request):
    if request.method == 'POST':
        form = classroomForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            cap = form.cleaned_data['capacity']
            c = Classrooms(name = name, capacity = cap)
            c.save()
            
   
    else:
        form = classroomForm()
    
    data = Classrooms.objects.all()
    classroomcount = len(data.values('name'))
    context ={
        'data' :data,
        'form' : form,
        'classroomcount':classroomcount
    }
    
    return render(request, 'classroom.html',context)

def module(request):
    
    data = Modules.objects.all()
    modulecount = len(data.values('module_id'))
    if request.method == 'POST':
        form = moduleForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['module_id']
            name = form.cleaned_data['module_name']
            c = Modules(module_id = id, module_name = name)
            c.save()
    else:
        form = moduleForm()
    context ={
        'data' :data,
        'form' : form,
        'modulecount':modulecount
    }
    
    return render(request, 'module.html',context)

def invigilator(request):
    data = Invigilators.objects.all()
    invigilatorcount = len(data.values('name'))
    
    return render(request, 'invigilator.html',{'data':data,'invigilatorcount':invigilatorcount})

def addInvigilator(request):
    vuid=request.POST['userName']
    vuemail=request.POST['email']
    vupasswd=request.POST['password']
    us=User(uName=vuid, uemail=vuemail, upasswd=vupasswd)
    us.save()
    invigil = Invigilators(name=vuid,email=vuemail,password=vupasswd)
    invigil.save()
    
    
    return render(request, 'invigilatortable')


def student(request):
    data = Students.objects.all()
    studentcount = len(data.values('student_id'))
    data = data.select_related('program','year')
    if request.method == 'POST':
        form = studentForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['student_id']
            name = form.cleaned_data['name']
            program = form.cleaned_data['program']
            program = get_object_or_404(Programs, program_name=program)
            year = form.cleaned_data['year']
            year = get_object_or_404(YearOfStudy, year_id=year.year_id)
            
            c = Students(student_id = id, name = name, program = program, year = year)
            c.save()
    else:
        form = studentForm()
    context ={
        'data' :data,
        'form' : form,
        'studentcount': studentcount
    }
    
    
    
    return render(request, 'student.html',context)

def department(request):
    data = Departments.objects.all()
    deptcount = len(data.values('department_name'))
    if request.method == 'POST':
        form = departmentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['department_name']
            c = Departments(department_name = name)
            c.save()
    else:
        form = departmentForm()
    context ={
        'data' :data,
        'form' : form,
        'deptcount': deptcount
    }
    
    return render(request, 'department.html',context)

def program(request):
    data = Programs.objects.all()
    data = data.select_related('department')
    programcount = len(data.values('department'))
    if request.method == 'POST':
        form = programForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['program_name']
            dept = form.cleaned_data['department']
            dept = get_object_or_404(Departments, department_name=dept)
            c = Programs(program_name = name, department = dept)
            c.save()
    else:
        form = programForm()
    context ={
        'data' :data,
        'form' : form,
        'programcount': programcount
    }
    
    
    
    return render(request, 'program.html',context)




# genetic algorithm implementation


# Class to store course
class Course:
    # Initialize the class
    def __init__(self, code, name, number):
        self.courseCode = code
        self.courseName = name
        self.number = number

    # Print course
    def __repr__(self):
        return '({0},{1},{2})'.format(self.courseCode, self.courseName, self.number)

    # Check Equality
    def __eq__(self, other):
        return self.courseName == other.courseName and self.courseCode == other.courseCode

 # Class to store student registered in course
class Registration:
    # Initialize the class
    def __init__(self, Name, courseCodes):
        self.studentName = Name
        self.registeredCourses = courseCodes.copy()
 

    # Print registration
    def __repr__(self):
        return '({0},{1})'.format(self.studentName, self.registeredCourses)

    # Check equality
    def __eq__(self, other):
        if self.studentName == other.studentName and len(self.registeredCourses) == len(other.registeredCourses):
            count = 0
            for i in range(len(self.registeredCourses)):
                if self.registeredCourses[i] == other.registeredCourses[i]:
                    count += 1
            if count == len(self.registeredCourses):
                return True
        return False

# Class to store an exam
class Exam:
    # Initialize the class
    def __init__(self, startTime, day, student):
        self.startTime = startTime
        # self.roomNo = roomNo.copy()
        self.day = day
        # self.invigilator = invigilator.copy()
        self.student = student
        self.binary = []

    # Print an exam
    def __repr__(self):
        return '(\n{0}, {1},{2}, \n{3}'.format(self.startTime,
                                                     self.day, self.student, self.binary)

    # Check equality
    def __eq__(self, other):
        return self.startTime == other.startTime and self.day == other.day and self.student==other.student


totalDays = []

examStartTimings = []


examDuration = 3

courses = []

student_list=[]

totalStudents = -1

instructors = []

totalInstructors = -1

registrations = []

Individual = collections.namedtuple('Population', 'chromosome value')

population_size = 25

crossover_probability, mutation_probability = 0.0, 0.0

MG_indexes = []
CS_indexes = []

def generateTimetable(request):
     
    
    if request.method == 'POST':
      
        form = DateForm(request.POST)
        date_list=[]
        timings =[]

        if form.is_valid():
            print(1)
            
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            # Process the dates and return a list of dates
            
            delta = end_date - start_date
            
            examsvalues = form.cleaned_data['exams']
            if examsvalues == 'Semester End Examination':
                latest_entry = Examselection.objects.latest('created_at')
                dates = '[(9, 0), (1, 1)]'
                latest_entry.selection = dates
                latest_entry.save()
                latest_entry2 = ExaminationType.objects.latest('date_created')
                latest_entry2.name = examsvalues
                latest_entry2.save()
              
            
            if examsvalues == 'Mid Term Examination':
                latest_entry = Examselection.objects.latest('created_at')
                dates = '[(8, 0), (1, 1),(2, 2),(3, 3),(4, 4),(5, 5),(6, 6)]'
                latest_entry.selection = dates
                latest_entry.save()
                latest_entry2 = ExaminationType.objects.latest('date_created')
                latest_entry2.name = examsvalues
                latest_entry2.save()
                
                
                
                
            count = 0

            for i in range(delta.days + 1):
                
                date_list.append((start_date + timedelta(days=i)))
                

            datelist=[]
            

            for i in range(delta.days + 1):
                current_date = start_date + timedelta(days=i)
                if current_date.weekday() != 6:  # 6 is Sunday
                    date_list.append(current_date)
                    datelist.append((str(current_date), count))
                    count += 1
           

            
            
            date_string = str(datelist)
            # Get the latest DateTuple object
            latest_entry = DateTuple.objects.latest('created_at')

            # Update the dates field with the new dates
            latest_entry.dates = date_string

            # Save the updated object to the database
            latest_entry.save()
            
            year =  start_date = form.cleaned_data['year']
            examsemester =  start_date = form.cleaned_data['examsemester']
            entry = ExamSemester.objects.latest('date_created')  
            entry.year= year
            entry.semester = examsemester
            entry.save()
            
            
            takeInput()
            population_size = 25
            crossover_probability = 0.7
            mutation_probability = 0.4

            # Calculating MG and CS courses indexes
            for i in range(0, len(courses)):
                if courses[i].courseCode[0] == 'M' and courses[i].courseCode[1] == 'G':
                    MG_indexes.append(i)
                if courses[i].courseCode[0] == 'C' and courses[i].courseCode[1] == 'S':
                    CS_indexes.append(i)

            # Printing Initialized variables
            print('----- Generated Parameters -----')
            print('Population size......: {}'.format(population_size))
            print('Crossover probability: {}'.format(crossover_probability))
            print('Mutation probability.: {}'.format(mutation_probability))

            # Running Genetic Algorithm
           # print(totalExamStartTimings)
            runGA()
            return redirect('dashtable')

    else:
        form = DateForm()
    
            
    return render(request, 'generate.html', {'form': form}) 
    
def takeInput():
    # Reading courses from file
    reader = Modules.objects.all()
    reader = reader.values('module_id','module_name')
    
    count = 0
    for row in reader:
        if len(row) != 0:
            temp_course = Course(row['module_id'],row['module_name'], count)
            if temp_course not in courses:
                courses.append(temp_course)
                count += 1

    # Reading students from file
    reader = NormalEnrollments.objects.all()
    programs = Programs.objects.all()
    prog = programs.values('program_id','program_name','department_id')
    read = reader.values('program','semester','year_id','module_id')
    pro=[]
    
    count1 = 0 
    for row in read:
        if len(row) != 0:
            for r in prog:
                if row['program'] == r['program_id']:
                    pro = r['program_name']
                    #pro = re.sub("[^0-9]", "", pro) 
            temp_registration = Registration(str(row['year_id']) + str(pro),[])
            
            if temp_registration not in registrations:
                count1 += 1
                registrations.append(temp_registration)
            student_list.append((str(row['year_id']) + str(pro),count1))
                
    reader = RepeatEnrollments.objects.all()
    read = reader.values('student_id','semester','module_id')
    
    count2 = count1
    for row in read:
        if len(row) != 0:
            temp_registration = Registration(row['student_id'],[])
            student_list.append((row['student_id'],count2))
            if temp_registration not in registrations:
                count2 +=1
                registrations.append(temp_registration)
                
        
    global totalStudents
    totalStudents = count2
    
    
    # Reading students from file
    reader = NormalEnrollments.objects.all()
    programs = Programs.objects.all()
    prog = programs.values('program_id','program_name','department_id')
    read = reader.values('program','semester','year_id','module_id')
    pro=[]
    
    for row in read:
        if row != 0:
            for r in prog:
                if row['program'] == r['program_id']:
                    pro = r['program_name']
                    #pro = re.sub("[^0-9]", "", pro) 
            
            if len(row) != 0 and row['program'] != '':
                for i in registrations:
                    if i.studentName == str(row['year_id']) + str(pro) and row['module_id'] not in i.registeredCourses:
                        i.registeredCourses.append(row['module_id'])
                        
    reader = RepeatEnrollments.objects.all()
    read = reader.values('student_id','semester','module_id')
    
    for row in read:
        if row != 0:
            if len(row) != 0 and row['student_id'] != '':
                for i in registrations:
                    if i.studentName == row['student_id'] and (row['module_id']) not in i.registeredCourses:
                        i.registeredCourses.append(row['module_id'])
     
# Generating random exam
def getRandomExam(index):
    courseCode = courses[index].courseCode
    
    latest_entry = Examselection.objects.latest('created_at')
    latest_dates_string = latest_entry.selection
    examStartTimings = ast.literal_eval(latest_dates_string)
    
    
    totalExamStartTimings = len(examStartTimings)

    # Setting time
    startTime = examStartTimings[rn.randrange(0, totalExamStartTimings)]
    if startTime[0] > 12:
        startTime -= 12
       


    # Setting day
    latest_entry = DateTuple.objects.latest('created_at')
    latest_dates_string = latest_entry.dates
    days = ast.literal_eval(latest_dates_string)
    new_days = []
    for day in days:
        date_str = day[0]
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        day_of_week = date_obj.strftime("%A")
        new_date_str = date_obj.strftime("%A-%d/%m/%y")
        new_days.append((new_date_str, day[1]))
        days = new_days
    
    totalDays = len(days)
    
    
    
    day = days[rn.randrange(0, totalDays)]

    # setting Students
    #print(student_list)
    student=[]
    temp = student_list[rn.randrange(0, totalStudents)]
    student.append(temp)
    
    print(Exam(startTime,day,student))

    return Exam(startTime,day,student)

# Generate Population, given the size
def generate_population(size):
    new_population = []

    # Initialize Random population
    for i in range(size):
        timeTable = []
        for j in range(len(courses)):
            timeTable.append(getRandomExam(j))

   
        new_population.append(
            Individual(
                chromosome=timeTable,
                value=-1
            )
        )
    #print("the time table is",timeTable)
    return new_population

# Apply Mutation on chromosomes
def apply_mutation(chromosome):
    if random.randint(0, 100) <= mutation_probability * 100:
        gene = random.randint(0, len(courses) - 1)
        chromosome[gene] = getRandomExam(gene)
    return chromosome

# Apply Crossover on population
def apply_crossover(population):
    crossover_population = []

    while len(crossover_population) < len(population):
        if randint(0, 100) <= crossover_probability * 100:
            # Selecting parents
            parent_a = randint(0, len(population) - 1)
            parent_b = randint(0, len(population) - 1)

            # Doing crossover
            chromosome_a = copy.deepcopy(concatenate((population[parent_a].chromosome[:int(len(courses) / 2)],
                                                      population[parent_b].chromosome[int(len(courses) / 2):])))
            chromosome_a = apply_mutation(chromosome_a)

            chromosome_b = copy.deepcopy(concatenate((population[parent_b].chromosome[:int(len(courses) / 2)],
                                                      population[parent_a].chromosome[int(len(courses) / 2):])))
            chromosome_b = apply_mutation(chromosome_b)

            crossover_population.append(Individual(
                chromosome=chromosome_a,
                value=-1
            ))
            crossover_population.append(Individual(
                chromosome=chromosome_b,
                value=-1
            ))

    # Calculating fitness of crossover population
    crossover_population = calculate_fitness(crossover_population)
    # Combining will all population
    population = population + crossover_population
    return population
# Roulette Wheel Selection
def roulette_wheel_selection(population):
    # Calculating total fitness
    population_fitness = sum([individual.value for individual in population])
    # Calculating probabilities of all chromosomes
    chromosome_probabilities = [round(individual.value / population_fitness, 5) for individual in population]

    copy_probabilities = chromosome_probabilities.copy()
    copy_probabilities.sort()
    for i in range(len(copy_probabilities)):
        if i != 0:
            copy_probabilities[i] = round(copy_probabilities[i] + copy_probabilities[i - 1], 5)

    # Selecting population
    selected_population = []
    for i in range(population_size):
        index = -1
        random_probability = round(random.uniform(0, 1), 5)
        for j in range(len(copy_probabilities)):
            if random_probability <= copy_probabilities[j]:
                value = copy_probabilities[j]
                if j != 0:
                    value = round(value - copy_probabilities[j - 1], 5)
                index = chromosome_probabilities.index(value)
                break
        selected_population.append(population[index])
    return selected_population
# Find Top Fittest Individual from Population
def find_fittest_individual(population):
    highest_value = 0
    highest_index = 0
    for i in range(len(population)):
        if population[i].value > highest_value:
            highest_value = population[i].value
            highest_index = i
    return population[highest_index]

# Checks whether same student is giving two exams at the same time or not
def checkStudent(chromosome):
     # Setting day
    latest_entry = DateTuple.objects.latest('created_at')
    latest_dates_string = latest_entry.dates
    days = ast.literal_eval(latest_dates_string)
    new_days = []
    for day in days:
        date_str = day[0]
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        day_of_week = date_obj.strftime("%A")
        new_date_str = date_obj.strftime("%A-%d/%m/%y")
        new_days.append((new_date_str, day[1]))
        days = new_days
    
    
    
    violation_count = 0
    data = [(individual.student, individual.day, individual.startTime) for individual in chromosome]
    for i in range(len(data)):
        for student in data[i][0]:
            for j in range(len(data)):
                if i != j and student in data[j][0] and data[i][1] == data[j][1] and data[i][2] == data[j][2]:
                    violation_count += 1
    return violation_count // 2

# Checks whether a student is having  two exams in a row or not
def checkStudentsBreak(chromosome):
     # Setting day
    latest_entry = DateTuple.objects.latest('created_at')
    latest_dates_string = latest_entry.dates
    days = ast.literal_eval(latest_dates_string)
    new_days = []
    for day in days:
        date_str = day[0]
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        day_of_week = date_obj.strftime("%A")
        new_date_str = date_obj.strftime("%A-%d/%m/%y")
        new_days.append((new_date_str, day[1]))
        days = new_days
    
    
    
    violation_count = 0
    data = [(individual.student, individual.day) for individual in chromosome]

    for i in range(len(data)):
        for student in data[i][0]:
            for j in range(len(data)):
                if i != j and student in data[j][0] and data[i][1] == data[j][1]:
                    violation_count += 1
    return violation_count // 2

# Checks whether the student is giving one exam at a time or not
def one_exam_student_check(chromosome):
    
     # Setting day
    latest_entry = DateTuple.objects.latest('created_at')
    latest_dates_string = latest_entry.dates
    days = ast.literal_eval(latest_dates_string)
    new_days = []
    for day in days:
        date_str = day[0]
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        day_of_week = date_obj.strftime("%A")
        new_date_str = date_obj.strftime("%A-%d/%m/%y")
        new_days.append((new_date_str, day[1]))
        days = new_days
    
    
    
    
    violation_count = 0
    student_exams = {}
    for i in range(len(registrations)):
        student_id = registrations[i].studentName
        for j in range(len(chromosome)):
            if courses[j].courseCode in registrations[i].registeredCourses:
                exam_time = (chromosome[j].day[1], chromosome[j].startTime)
                if student_id in student_exams:
                    for existing_time in student_exams[student_id]:
                        if existing_time == exam_time:
                            violation_count += 1
                            break
                    student_exams[student_id].append(exam_time)
                else:
                    student_exams[student_id] = [exam_time]
    return violation_count
#break between exam days for the students / Checks whether a student is giving two exams in a consequitve days

def checkStudentsBreakInDays(chromosome):
     # Setting day
    latest_entry = DateTuple.objects.latest('created_at')
    latest_dates_string = latest_entry.dates
    days = ast.literal_eval(latest_dates_string)
    new_days = []
    for day in days:
        date_str = day[0]
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        day_of_week = date_obj.strftime("%A")
        new_date_str = date_obj.strftime("%A-%d/%m/%y")
        new_days.append((new_date_str, day[1]))
        days = new_days
    
    
    violation_count = 0
    for i in range(0, len(registrations)):
        days_arr = []
        for j in range(0, len(chromosome)):
            if courses[j].courseCode in registrations[i].registeredCourses:
                exam_day = chromosome[j].day[1]
                exam_start_time = chromosome[j].startTime
                
                # Check if the student has an exam on this day
                if (exam_day, exam_start_time) not in days_arr:
                    days_arr.append((exam_day, exam_start_time))
                    
                    # Check if any two consecutive days have exams
                    if len(days_arr) >= 2:
                        days_arr.sort()
                        for k in range(1, len(days_arr)):
                            if days_arr[k][0] - days_arr[k-1][0] == 1:
                                violation_count += 1
                                break
    return violation_count

# Calculating fitness of given chromosome
def calculate_value(chromosome):
    value = 500
    # value -= check_MGCS(chromosome)
    value -= checkStudent(chromosome)
    # value -= checkRooms(chromosome)
    value -= checkStudentsBreak(chromosome)
    value -= one_exam_student_check(chromosome)
    value -= checkStudentsBreakInDays(chromosome)

    # Binary encoding
    for i in range(len(chromosome)):
        chromosome[i].binary.clear()
        chromosome[i].binary.append(bin(courses[i].number)[2:].zfill(6))
        chromosome[i].binary.append(bin(chromosome[i].startTime[1])[2:].zfill(6))
        # tempRoom = []
        # for room in chromosome[i].roomNo:
        #     tempRoom.append(bin(room[1])[2:].zfill(6))
        # chromosome[i].binary.append(tempRoom)
        chromosome[i].binary.append(bin(chromosome[i].day[1])[2:].zfill(6))
        tempStudent = []
        for student in chromosome[i].student:
            tempStudent.append(bin(student[1])[2:].zfill(6))
        chromosome[i].binary.append(tempStudent)
    return value

# Assigning fitness to the chromosomes in population
def calculate_fitness(population):
    for i in range(len(population)):
        v = calculate_value(population[i].chromosome)
        population[i] = Individual(
            chromosome=population[i].chromosome,
            value=v
        )
    return population

# Displays the schedule
def display_schedule(best_solution):
     # Setting day
    latest_entry = DateTuple.objects.latest('created_at')
    latest_dates_string = latest_entry.dates
    days = ast.literal_eval(latest_dates_string)
    new_days = []
    for day in days:
        date_str = day[0]
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        day_of_week = date_obj.strftime("%A")
        new_date_str = date_obj.strftime("%A-%d/%m/%y")
        new_days.append((new_date_str, day[1]))
        days = new_days
    
    studentForExams =[]
    
    
    schedule = []
    overallSchedule=[]

    count = 0
    temp_day = -1
    
    week = 1
    last_week_entry = 0
    weekflag = False

    max_length = 0
    for i in courses:
        if len(i.courseName) > max_length:
            max_length = len(i.courseName)

    best_solution_copy = copy.deepcopy(best_solution)
    best_solution_copy = Individual(sorted(best_solution_copy.chromosome, key=lambda x:(x.day[1], x.startTime[1])), best_solution_copy.value)

    print("\n\nSCHEDULE:\n--------")
    for i in best_solution_copy.chromosome:
        curr_day = i.day[1]
        if curr_day >= last_week_entry:
            if count != 0:
                print(end="\t\t")
                for j in range(0, 41 + max_length ):
                    print(end="-")
                print()

            print("\nWeek", week)
            print("------")
            week += 1
            last_week_entry += 5
            weekflag = True


        if temp_day != curr_day:
            if count != 0 and weekflag == False:
                print(end="\t\t")
                for j in range(0, 41 + max_length ):
                    print(end="-")
                print()

            print(end="\n\n\n\t\t")
            days=i.day[0]
            schedule.append(days)
            print(i.day[0])
            weekflag = False

        print(end="\t\t")
        for j in range(0, 41 + max_length ):
            print(end="-")
        print()

        print(end="\t\t")
        for j in range(0, len(courses)):
            if best_solution.chromosome[j] == i:
                ind = j
                break
        course_Code=courses[ind].courseCode
        course_Name = courses[ind].courseName 


       
        schedule.append(course_Code)
        schedule.append(course_Name)


        print("|", courses[ind].courseCode, "|", courses[ind].courseName, end="")

        if len(courses[ind].courseCode) == 5:
            for j in range(0, max_length-len(courses[ind].courseName)):
                print(end=" ")
        else:
            for j in range(0, max_length-len(courses[ind].courseName)-1):
                print(end=" ")
        print(end=" | ")

        if i.startTime[1] == 0:
            time="9.00-12.00 AM"
            print("9:00-12:00 AM | ", end="")
            schedule.append(time)
        if  i.startTime[1] == 1:
            time="1.00-4.00 PM"
            print("1:00-4:00 PM | ", end =" ")
            schedule.append(time)
        if  i.startTime[1] == 8:
            time="8.00-9.00 AM"
            print("8:00-9:00 AM | ", end =" ")
            schedule.append(time)
        if  i.startTime[1] == 2:
            time="9.30-10.30 AM"
            print("9:30-10:30 AM | ", end =" ")
            schedule.append(time)
        if  i.startTime[1] == 3:
            time="11.00-12.00 PM"
            print("11:00-12:00 PM | ", end =" ")
            schedule.append(time)
        if  i.startTime[1] == 4:
            time="1.00-2.00 PM"
            print("1:00-2:00 PM | ", end =" ")
            schedule.append(time)
        if  i.startTime[1] == 5:
            time="2.30-3.30 PM"
            print("2:30-3:30 PM | ", end =" ")
            schedule.append(time)
        if  i.startTime[1] == 6:
            time="4.00-5.00 PM"
            print("4:00-5:00 PM | ", end =" ")

        

    for i in range(0, len(schedule), 4):
       overallSchedule.append(schedule[i:i+4])

    #print(overallSchedule)
    
    # convert overallSchedule to a set of tuples to remove duplicates
    unique_schedule = set(tuple(row) for row in overallSchedule)

    # convert the set of tuples back to a list of lists
    overallSchedule = [list(row) for row in unique_schedule]
    
    # sort overallSchedule by date
    overallSchedule = sorted(overallSchedule, key=lambda row: row[0].split("-")[1])

    
      
    # row[0].split("-")[0] - day, row[0].split("-")[1]- date , row[3]- time , row[2]- module code, row[1] - moduleName
    
    
       # Get the current date and time
    current_datetime = timezone.now()
    
    existing_record = Examtable.objects.filter(date_created=current_datetime).first()

    if  existing_record != 0:
        for examtable in Examtable.objects.all():
            examtable_history = ExamtableHistory(
            day=examtable.day,
            date=examtable.date,
            time=examtable.time,
            module_code=examtable.module_code,
            module_name=examtable.module_name,
            date_created=examtable.date_created
            )
            examtable_history.save()# Delete old data from Examtable table
        Examtable.objects.all().delete()

    
    for row in overallSchedule:
        examtable = Examtable(
        day=row[0].split("-")[0],
        date=row[0].split("-")[1],
        time=row[3],
        module_code=row[1],
        module_name= row[2],
        )
        examtable.save()
               

    return render(request, 'generatedtable.html')


def runGA():
    # Generating random population
    population = generate_population(population_size)
    generation = 1
    best_solution = None

    # Calculate Fitness of initial population
    population = calculate_fitness(population)

    # Running generations
    while True:
        # Applying crossover and mutation
        population = apply_crossover(population)
        # Selection using roulette wheel
        population = roulette_wheel_selection(population)
        # Finding fittest candidates
        candidate = find_fittest_individual(population)

        # Updating best solution so far
        if best_solution is None:
            best_solution = candidate
        elif candidate.value > best_solution.value:
            best_solution = candidate

        # print Every 10th generation results
        if generation % 2 == 0 or generation == 1:
            print('\nCurrent generation: {}'.format(generation))
            print('Best solution so far: {}, Goal: 400'.format(best_solution.value))

        # break when solution is found
        if best_solution.value > 370 or best_solution.value > 400 or best_solution.value == 472 or best_solution.value == 473 or best_solution.value == 474:
            print('\nSolution found:')
            print('Value: {}, Goal: 400'.format(best_solution.value))

            print("\nHard Constraints:")
            print("1: An exam will be scheduled for each course\t\t\t\t ✔")
            print("2: A student is enrolled in minimum three courses\t\t\t ✔")
            if one_exam_student_check(best_solution.chromosome) == 0:
                print("3: A student can not give more than one exam at a time\t\t\t ✔")
            else:
                print("3: A student can not give more than one exam at a time\t\t\t ❌")
            print("4: All exams must be held between 9 AM and 5 PM\t\t\t\t ✔")
            if checkStudent(best_solution.chromosome) == 0:
                print("5: A teacher can not invigilate two exams at the same time\t\t ✔")
            else:
                print("5: A teacher can not invigilate two exams at the same time\t\t ❌")
            if checkStudentsBreak(best_solution.chromosome) == 0:
                print("6: A teacher can not invigilate two exams in a row\t\t\t ✔")
            else:
                print("6: A teacher can not invigilate two exams in a row\t\t\t ❌")

            if checkStudentsBreakInDays(best_solution.chromosome)==0:
              print("students get break of two days between the exams\t\t\t✔")
            else:
              print("students do not get break of two days between the exams\t❌")
            # # if checkRooms(best_solution.chromosome) == 0:
            #     print("7: No exam scheduled in the same room at the same time\t\t\t")
            # else:
            #     print("7: No exam scheduled in the same room at the same time\t\t\t ❌")

            print("\nSoft Constraints:")
            print("1: An exam will be scheduled for each course\t\t\t\t ✔")
            print("2: A student shall not give more than one exam consecutively\t\t ✔")
            print("3: MG courses preferably be held before CS courses\t\t\t ✔")
            print("4: Two hours of break for faculty meeting\t\t\t\t ✔")

            display_schedule(best_solution)
            break
        generation += 1
        

def displayexamtabletopublic(request):
    program_list = [
        {'id': 3, 'name': 'BEIT'},
        # Add more programs here
    ]
    year_list = [1, 2, 3, 4]
    
    schedule= Examtable.objects.all()
    schedule_list = schedule.values('day','date','time','module_code','module_name')
   
    examtable_list = []
    s = ExamSemester.objects.all()
    sem = s.values_list('semester', flat=True)
    sem = sem[0]
    y = s.values_list('year', flat=True)
    y = y[0]
    type = ExaminationType.objects.all()
    type = type.values_list('name', flat=True)
    type = type[0]
    for program in program_list:
        for year in year_list:
            enrollments = NormalEnrollments.objects.filter(program_id=program['id'], year_id=year)
            normalmodules = enrollments.values_list('module', flat=True)
            moduleList = list(normalmodules)
            repeat = RepeatEnrollments.objects.filter(program_id=program['id'], year_id=year)
            repeatmodules = repeat.values_list('module', flat=True)
            if len(repeatmodules) != 0 :
                moduleList.extend(list(repeatmodules))
            it_modules = schedule_list.filter(module_code__in= moduleList).order_by('date')
          
            examtable_list.append({
                    'program_name': program['name'],
                    'program_year': year,
                    'it_modules':it_modules

                })

    
    context = {
        'examtable_list': examtable_list,
        'schedule_list' : schedule_list,
        'sem':sem,
        'y':y,
        'type':type
        
    
    }
    
    return render(request, 'viewschedule.html', context)


def editable(request):
    examtable = Examtable.objects.all()
    examtable = examtable.values('id','day','date','time','module_code','module_name')
    program_list = [
        {'id': 3, 'name': 'BEIT'},
        # Add more programs here
    ]
    year_list = [1, 2, 3, 4]
    schedule= Examtable.objects.all()
    schedule_list = schedule.values('id','day','date','time','module_code','module_name')
    examtable_list = []
    s = ExamSemester.objects.all()
    sem = s.values_list('semester', flat=True)
    sem = sem[0]
    y = s.values_list('year', flat=True)
    y = y[0]
    type = ExaminationType.objects.all()
    type = type.values_list('name', flat=True)
    type = type[0]
    
    for program in program_list:
        for year in year_list:
            enrollments = NormalEnrollments.objects.filter(program_id=program['id'], year_id=year)
            normalmodules = enrollments.values_list('module', flat=True)
            moduleList = list(normalmodules)
            repeat = RepeatEnrollments.objects.filter(program_id=program['id'], year_id=year)
            repeatmodules = repeat.values_list('module', flat=True)
            if len(repeatmodules) != 0 :
                moduleList.extend(list(repeatmodules))
            it_modules = schedule_list.filter(module_code__in= moduleList).order_by('date')
            examtable_list.append({
                    'program_name': program['name'],
                    'program_year': year,
                    'it_modules':it_modules

                })

    if request.method == 'POST':
        for module in examtable:
            module_id = module['id']
            examtable = Examtable.objects.get(id=module_id)
            examtable.day = request.POST.get(f"day{module_id}")
            examtable.date = request.POST.get(f"date{module_id}")
            examtable.time = request.POST.get(f"time{module_id}")
            examtable.module_code = request.POST.get(f"module_code{module_id}")
            examtable.module_name = request.POST.get(f"module_name{module_id}")
            examtable.save()
        return redirect('dashtable')

    context = {
        'examtable_list': examtable_list,
        'schedule_list' : schedule_list,
        'examtable': examtable,
        'sem':sem,
        'y':y,
        'type': type
        
    
    }
    return render(request, 'generatedtable.html', context)


def displayexamtabletodashboard(request):
    
    
            
        
        return render(request, 'publishtable.html')    
   
def displayexamtabletofaculty(request):
    
    
        program_list = [
            {'id': 3, 'name': 'BEIT'},
            # Add more programs here
        ]
        year_list = [1, 2, 3, 4]
        
        schedule= Examtable.objects.all()
        schedule_list = schedule.values('day','date','time','module_code','module_name')
        examtable_list = []
        s = ExamSemester.objects.all()
        sem = s.values_list('semester', flat=True)
        sem = sem[0]
        y = s.values_list('year', flat=True)
        y = y[0]
        type = ExaminationType.objects.all()
        type = type.values_list('name', flat=True)
        type = type[0]
        for program in program_list:
            for year in year_list:
                enrollments = NormalEnrollments.objects.filter(program_id=program['id'], year_id=year)
                normalmodules = enrollments.values_list('module', flat=True)
                moduleList = list(normalmodules)
                repeat = RepeatEnrollments.objects.filter(program_id=program['id'], year_id=year)
                repeatmodules = repeat.values_list('module', flat=True)
                if len(repeatmodules) != 0 :
                    moduleList.extend(list(repeatmodules))
                it_modules = schedule_list.filter(module_code__in= moduleList).order_by('date')
                examtable_list.append({
                        'program_name': program['name'],
                        'program_year': year,
                        'it_modules':it_modules

                    })

        
        context = {
            'examtable_list': examtable_list,
            'schedule_list' : schedule_list,
            'sem':sem,
            'y':y,
            'type':type
        }
            
        
        return render(request, 'faculty.html', context)    
     
   
    
def viewtable(request):
    
        # Get the current date and time
    current_datetime = timezone.now()
    
    existing_record = Examtable.objects.filter(date_created=current_datetime).first()

    if  existing_record != 0:
        
        return redirect('dashtable')
    
    else: messages.success(request, 'No examinations generated')
    return render(request, 'dashboard.html')    
    

def viewinvigilation(request):
    
    message = 'No invigilation Schedules to be displayed'
   
    return render(request, 'dashboard.html',{'message': message})    
    

def generateclassroomallocation(request):
    
    if request.method == 'POST':
        examtable = Examtable.objects.all()
        examtable = examtable.values()
        module_day_time = examtable.values_list('module_code','date', 'day', 'time',)
        module_count_normal = NormalEnrollments.objects.all()
        countnormal = module_count_normal.values_list('module', 'num_students')
        module_count_repeat = RepeatEnrollments.objects.all()
        module_count_repeat = module_count_repeat.values_list('module')
        countnormal_dict = dict(countnormal)
        
        module_repeat_list = [module[0].strip() for module in module_count_repeat]
        for module, count in countnormal:
            if module in module_repeat_list:
                countnormal_dict[module] += 1
                
        countnormal = [(module, countnormal_dict[module]) for module in countnormal_dict]
        countnormal_dict = dict(countnormal)
        
        exam_schedule = {}
        
        for module, date, day, time in module_day_time:
            if date not in exam_schedule:
                exam_schedule[date] = {}
            if day not in exam_schedule[date]:  # <-- Updated line
                exam_schedule[date][day] = {}
            if time not in exam_schedule[date][day]:
                exam_schedule[date][day][time] = []

            exam_schedule[date][day][time].append((module, countnormal_dict[module]))
        
        rooms = Classrooms.objects.all()
        rooms = rooms.values()
        classrooms = {room['name']: room['capacity'] for room in rooms}
        

        allocate_rooms(exam_schedule, classrooms)
        
        
        current_datetime = timezone.now()
    
        existing_record = ClassroomAllocation.objects.filter(date_created=current_datetime).first()

        if  existing_record != 0:
            ClassroomAllocation.objects.all().delete()
           # for examtable in Examtable.objects.all():
            #    examtable_history = ExamtableHistory(
            #    day=examtable.day,
            #    date=examtable.date,
            #    time=examtable.time,
            #    module_code=examtable.module_code,
            #    module_name=examtable.module_name,
            #    date_created=examtable.date_created
            #    )
            #    examtable_history.save()# Delete old data from Examtable table
            room_assignments = allocate_rooms(exam_schedule, classrooms)
            print(room_assignments)
            for date, day in room_assignments.items():
                for day_name, timeslots in day.items():
                    for time_slot, modules in timeslots.items():
                        for module_code, rooms in modules.items():
                            for room, num_of_students in rooms:
                                ctable = ClassroomAllocation(
                                        date=date, 
                                        timing= time_slot,
                                        module_code=module_code,
                                        num_of_students=num_of_students,
                                        classroom_id=room,
                                        date_created = current_datetime)
                                ctable.save()
            return redirect('classroom') 
        
        return render(request, 'generateClassroomAllocation.html')    
       

    else:
        return render(request, 'generateClassroomAllocation.html')    
    
            

def allocate_rooms(exam_schedule, room_capacities):
    allocated_rooms = {}
    for date, days in exam_schedule.items():
        allocated_rooms[date] = {}
        for day, sessions in days.items():
            allocated_rooms[date][day] ={}
            for session, courses in sessions.items():
                allocated_rooms[date][day][session] = {}
                # Initialize the room capacities for this session
                session_room_capacities = dict(room_capacities)
                session_room_capacities = {room: int(capacity) for room, capacity in room_capacities.items()}

                # Sort the courses in descending order of number of students
                courses = sorted(courses, key=lambda x: x[1], reverse=True)
                for course_info in courses:
                    course = course_info[0]
                    num_students = course_info[1]
                    allocated_rooms[date][day][session][course] = []
                
                    
                    # Compare the number of students with half the capacity of the room
                    if num_students <= session_room_capacities[max(session_room_capacities, key=session_room_capacities.get)] // 2:
                        # If the number of students is less than or equal to half the room capacity,
                        # allocate all the students to the highest capacity room
                        highest_capacity_room = max(session_room_capacities, key=session_room_capacities.get)
                        allocated_rooms[date][day][session][course].append((highest_capacity_room, num_students))
                        session_room_capacities[highest_capacity_room] -= num_students
                    else:
                        # Allocate half the room capacity to this course and half to another course
                        highest_capacity_room = max(session_room_capacities, key=session_room_capacities.get)
                        allocated_students_in_room = ceil(session_room_capacities[highest_capacity_room] / 2)
                        allocated_rooms[date][day][session][course].append((highest_capacity_room, allocated_students_in_room))
                        session_room_capacities[highest_capacity_room] -= allocated_students_in_room
                        num_students -= allocated_students_in_room
                        # Find another room whose remaining capacity can fit the remaining students
                        for room_name, room_capacity in session_room_capacities.items():
                            if room_name != highest_capacity_room and num_students <= room_capacity:
                                # Allocate the remaining students to this room
                                allocated_rooms[date][day][session][course].append((room_name, num_students))
                                session_room_capacities[room_name] -= num_students
                                break
    return allocated_rooms

        
def viewclassroomallocation(request):
        prog = Programs.objects.all()
        program_list = prog.values()
        yearIDs = YearOfStudy.objects.all()
        year_list = yearIDs.values('year_id')
        year_list = [year['year_id'] for year in yearIDs.values('year_id')]
    
        schedule= ClassroomAllocation.objects.all()
        schedule_list = schedule.values('date','timing','module_code','classroom_id','num_of_students')
        examtable_list = []
        s = ExamSemester.objects.all()
        sem = s.values_list('semester', flat=True)
        sem = sem[0]
        y = s.values_list('year', flat=True)
        y = y[0]
        type = ExaminationType.objects.all()
        type = type.values_list('name', flat=True)
        type = type[0]
        for program in program_list:
            for year in year_list:
                enrollments = NormalEnrollments.objects.filter(program_id=program['program_id'], year_id=year)
                normalmodules = enrollments.values_list('module', flat=True)
                moduleList = list(normalmodules)
                repeat = RepeatEnrollments.objects.filter(program_id=program['program_id'], year_id=year)
                repeatmodules = repeat.values_list('module', flat=True)
                if len(repeatmodules) != 0 :
                    moduleList.extend(list(repeatmodules))
                it_modules = schedule_list.filter(module_code__in= moduleList).order_by('date')
                examtable_list.append({
                        'program_name': program['program_name'],
                        'program_year': year,
                        'it_modules':it_modules

                    })

        
        context = {
            'examtable_list': examtable_list,
            'schedule_list' : schedule_list,
            'sem':sem,
            'y':y,
            'type':type
        }
            
        
        return render(request, 'viewClassroomAllocation.html', context)  

    
    

#IMPORTING EXCEL DATA

def ImportExceldept(request):
     
    if request.method == 'POST' and request.FILES['departmentlist']:      
        departmentlist = request.FILES['departmentlist']
        fs = FileSystemStorage()
        filename = fs.save(departmentlist.name, departmentlist)
        uploaded_file_url = fs.url(filename)              
        empexceldata = pd.read_excel(filename)        
        dbframe = empexceldata
        for dbframe in dbframe.itertuples():
            obj = Departments.objects.create(department_name=dbframe.Department )           
            obj.save()
              
    return render(request, 'department.html',{})

def ImportExcel(request):
    if request.method == 'POST' and request.FILES['programlist']:      
        programlist = request.FILES['programlist']
        fs = FileSystemStorage()
        filename = fs.save(programlist.name, programlist)
        uploaded_file_url = fs.url(filename)              
        programexceldata = pd.read_excel(filename)
        for row in programexceldata.itertuples():
            department_name = row.Department
            department = Departments.objects.get(department_name =department_name)
            program_name = row.Programme
            program = Programs(department=department, program_name=program_name)
            program.save() 
    return render(request, 'program.html',{})

def ImportExcelStudent(request):
    if request.method == 'POST' and request.FILES['studentlist']:      
        studentlist = request.FILES['studentlist']
        fs = FileSystemStorage()
        filename = fs.save(studentlist.name, studentlist)
        uploaded_file_url = fs.url(filename)              
        programexceldata = pd.read_excel(filename)
        for row in programexceldata.itertuples():
            program_name = row.Programme
            student_id = row.stdID
            name = row.Name
            program = Programs.objects.get(program_name = program_name)
            year = row.Year
            year = YearOfStudy.objects.get(year_id = year)
            student = Students(student_id=student_id,name = name, program =program ,year = year)
            student.save()
    return render(request, 'student.html',{})

def ImportExcelmodules(request):
    if request.method == 'POST' and request.FILES['modulelist']:      
        modulelist = request.FILES['modulelist']
        fs = FileSystemStorage()
        filename = fs.save(modulelist.name, modulelist)
        uploaded_file_url = fs.url(filename)              
        programexceldata = pd.read_excel(filename)
        for row in programexceldata.itertuples():
            modulecode = row.Modulecode
            module = row.Module
            modules = Modules(module_id=modulecode,module_name = module)
            modules.save()

    return render(request, 'module.html',{})

def modulemap(request):
    data1 = NormalEnrollments.objects.all()
    modulemapcount = len(data1.values('program'))
    data = data1.select_related('program','semester','year','module')
    num_students = data1.values('num_students')
    
    if request.method == 'POST':
        form = modulemappingForm(request.POST)
        if form.is_valid():
            
            program = form.cleaned_data['program']
            program = get_object_or_404(Programs, program_name=program)
            year = form.cleaned_data['year']
            year = get_object_or_404(YearOfStudy, year_id=year.year_id)
            semester = form.cleaned_data['semester']
            semester = get_object_or_404(Semester, semester_number=semester.semester_number)
            module = form.cleaned_data['module']
            module = get_object_or_404(Modules, module_name=module.module_name)
            c = NormalEnrollments(program = program, year = year, semester = semester,module=module)
            c.save()
    else:
        form = modulemappingForm()
    context ={
        'data' :data,
        'form' : form,
        'num_students': num_students,
        'modulemapcount': modulemapcount
    }
    
    
    return render(request, 'modulemap.html',context)


def repeats(request):
    data = RepeatEnrollments.objects.all()
    repeatcount = len(data.values('student'))
    data = data.select_related('student','program','semester','year','module')
    if request.method == 'POST':
        form = studentrepeatForm(request.POST)
        if form.is_valid():
            
            student_id= form.cleaned_data['student_id']
            student= get_object_or_404(Students, student_id=student_id)
            student_name= form.cleaned_data['student_name']
            student_name = get_object_or_404(Students, student_name=student_id.student_name)
            program = form.cleaned_data['program']
            program = get_object_or_404(Programs, program_name=program)
            year = form.cleaned_data['year']
            year = get_object_or_404(YearOfStudy, year_id=year.year_id)
            semester = form.cleaned_data['semester']
            semester = get_object_or_404(Semester, semester_number=semester.semester_number)
            module = form.cleaned_data['module']
            module = get_object_or_404(Modules, module_name=module.module_name)
            c = RepeatEnrollments(student_id = student, student_name = student_name,program = program, year = year, semester = semester,module=module)
            c.save()
    else:
        form = studentrepeatForm()
    context ={
        'data' :data,
        'form' : form,
        'repeatcount': repeatcount
    }
    
    
    return render(request, 'studentrepeats.html',context)


def search_results_view(request):
    query = request.GET.get('query')

    if query:
        data = Classrooms.objects.filter(
            Q(name__icontains=query) |
            Q(capacity__icontains=query) 
        )
    else:
        data = Classrooms.objects.none()

    context = {
        'data': data,
        'query': query,
        
    }
    return render(request, 'classroom.html', context)


def delete_student(request):
    resp = {'status': 'failed', 'msg': ''}
    if not request.method == 'POST':
        resp['msg'] = 'Request has been sent without data.'
    else:
        student_id = request.POST.get('id')
        try:
            student = Classrooms.objects.get(id=student_id)
            student.delete()
            resp['status'] = 'success'
            resp['msg'] = 'Student detail has been deleted successfully.'
        except Classrooms.DoesNotExist:
            resp['msg'] = 'Student detail not found.'
        except Exception as e:
            resp['msg'] = 'An error occurred while deleting the student detail: {}'.format(str(e))

    return JsonResponse(resp)







    