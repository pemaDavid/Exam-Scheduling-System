from django.db import models

from django.db import models
from django.urls import reverse 

class User(models.Model):
    uName = models.CharField(max_length=30)
    uemail = models.CharField(max_length=30)
    upasswd = models.CharField(max_length=15)
   
    class Meta:
        db_table="users"

class Invigilators(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'invigilators'

class Classrooms(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    capacity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'classrooms'

class ClassroomAllocation(models.Model):
    allocation_id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=10, blank=True, null=True)
    num_of_students = models.IntegerField()
    timing = models.CharField(max_length=50)
    module_code = models.CharField(max_length=50)
    date_created = models.DateTimeField()
    classroom_id = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'Classroom_Allocation'

class Programs(models.Model):
    program_id = models.AutoField(primary_key=True, unique= True)
    program_name = models.CharField(max_length=255, unique=True)
    department = models.ForeignKey('Departments', models.DO_NOTHING)

    class Meta:
        db_table = 'Programs'
    def __str__(self):
        return self.program_name
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('Departments', args=[str(self.program_id)])


class Students(models.Model):
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    program = models.ForeignKey(Programs, models.DO_NOTHING)
    year = models.ForeignKey('YearOfStudy', models.DO_NOTHING, db_column='year', blank=True, null=True)

    class Meta:
        db_table = 'Students'
    def __str__(self):
        return self.student_id
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('Programs', args=[str(self.student_id)]),reverse('YearOfStudy', args=[str(self.student_id)])
    
    

class Departments(models.Model):
    department_id = models.AutoField(primary_key=True,unique= True)
    department_name = models.CharField(max_length=255,unique=True)

    class Meta:
        db_table = 'departments'
    def __str__(self):
        return self.department_name
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('Departments', args=[str(self.department_id)])

class Modules(models.Model):
    module_id = models.CharField(primary_key=True, max_length=6, unique= True)
    module_name = models.CharField(max_length=255,unique=True)

    class Meta:
        db_table = 'modules'
    def __str__(self):
        return self.module_id

class Semester(models.Model):
    semester_number = models.IntegerField(primary_key=True)
    year_id = models.IntegerField()

    class Meta:
        db_table = 'semester'
    def __str__(self):
        return f'{self.semester_number}'

class YearOfStudy(models.Model):
    year_id = models.IntegerField(primary_key=True)
    year_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'year_of_study'
    def __str__(self):
        return f'{self.year_id}'
    


class NormalEnrollments(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    semester = models.ForeignKey('Semester', models.DO_NOTHING)
    year = models.ForeignKey('YearOfStudy', models.DO_NOTHING)
    program = models.ForeignKey('Programs', models.DO_NOTHING)
    module = models.ForeignKey('Modules', models.DO_NOTHING)
    num_students = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'normalenrollments'
    
class RepeatEnrollments(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('Students', models.DO_NOTHING)
    year = models.ForeignKey('YearOfStudy', models.DO_NOTHING)
    semester = models.ForeignKey('Semester', models.DO_NOTHING)
    module = models.ForeignKey('Modules', models.DO_NOTHING)
    program = models.ForeignKey('Programs', models.DO_NOTHING)
    
    class Meta:
        db_table = 'studentrepeats'

    #def get_absolute_url(self):
    #    """Returns the URL to access a detail record for this book."""
    #    return reverse('Semester', args=[str(self.id)]),reverse('Modules', args=[str(self.id)]),reverse('Students', args=[str(self.id)]),reverse('YearOfStudy', args=[str(self.id)])
    
class DateTuple(models.Model):
    dates = models.CharField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table ='DateTuple'
            
class Examselection(models.Model):
    selection = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table ='exam_selection'

class Examtable(models.Model):
    day = models.CharField(max_length=10)
    date = models.CharField(max_length=10)
    time = models.CharField(max_length=25)
    module_code = models.CharField(max_length=10)
    module_name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'examTable'

class ExamtableHistory(models.Model):
    day = models.CharField(max_length=10)
    date = models.CharField(max_length=10)
    time = models.CharField(max_length=25)
    module_code = models.CharField(max_length=10)
    module_name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'examtable_history'
        
class ExamSemester(models.Model):
    semester = models.CharField(max_length=6)
    year = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'exam_semester'
        
class ExaminationType(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = False
        db_table = 'examination_type'