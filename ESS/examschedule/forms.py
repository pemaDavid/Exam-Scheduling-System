from django import forms



from django import forms
import datetime
from .models import Examtable,Programs,YearOfStudy,Semester,Modules




class loginForm(forms.Form):
    userEmail = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class classroomForm(forms.Form):
    name= forms.CharField(max_length=100, widget=forms.TextInput())
    capacity = forms.CharField(max_length=100, widget=forms.TextInput())


class DateForm(forms.Form):
    
    year = forms.IntegerField(
        label='Choose Year',
        widget=forms.NumberInput(attrs={'min': 2023, 'max': 3100, 'type': 'number'}),
        min_value=2023,
        max_value=3100
    )
    examsemester = forms.ChoiceField(
    label="Choose Semester",
    widget=forms.Select(attrs={'class': 'form-control'}),
    choices=(("Autumn", "Autumn"), ("Spring", "Spring")),
    )
    start_date = forms.DateField(
        label='Start date',
        initial=datetime.date.today(),
        widget=forms.DateInput(
            attrs={'type': 'date', 'format': '%A-%d/%m/%Y'}
        )
    )
    end_date = forms.DateField(
        label='End date',
        initial=datetime.date.today(),
        widget=forms.DateInput(
            attrs={'type': 'date', 'format': '%A-%d/%m/%Y'}
        )
    )
    
    
    

    def clean_year(self):
        year = self.cleaned_data['year']
        if len(str(year)) != 4:
            raise forms.ValidationError("Year must be in YYYY format")
        return year
    
    exams = forms.ChoiceField(
    label="Choose examination type",
    widget=forms.Select(attrs={'class': 'form-control'}),
    choices=(("Semester End Examination", "Semester End Examination"), ("Mid Term Examination", "Mid Term Examination")),
    )


   
class ExamtableForm(forms.ModelForm):
    class Meta:
        model = Examtable
        fields = ['id', 'day', 'date', 'time', 'module_code', 'module_name']
        

class moduleForm(forms.Form):
    module_id= forms.CharField(max_length=100, widget=forms.TextInput())
    module_name = forms.CharField(max_length=100, widget=forms.TextInput())

class departmentForm(forms.Form):
    department_name = forms.CharField(max_length=100, widget=forms.TextInput())
    
class programForm(forms.Form):
    program_name= forms.CharField(max_length=100, widget=forms.TextInput())
    department= forms.CharField(max_length=100, widget=forms.TextInput())
    

class studentForm(forms.Form):
    student_id= forms.CharField(max_length=100, widget=forms.TextInput())
    name= forms.CharField(max_length=100, widget=forms.TextInput())
    program = forms.ModelChoiceField(queryset=Programs.objects.all(), label='Program')
    year = forms.ModelChoiceField(queryset=YearOfStudy.objects.all(), label='Year')
   
class modulemappingForm(forms.Form):
    program = forms.ModelChoiceField(queryset=Programs.objects.all(), label='Program')
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), label='Semester')
    year = forms.ModelChoiceField(queryset=YearOfStudy.objects.all(), label='Year')
    module = forms.ModelChoiceField(queryset=Modules.objects.all(), label='Module')
    
class studentrepeatForm(forms.Form):
    student_id = forms.CharField(max_length=100, widget=forms.TextInput())
    student_name = forms.CharField(max_length=100, widget=forms.TextInput())
    program = forms.ModelChoiceField(queryset=Programs.objects.all(), label='Program')
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), label='Semester')
    year = forms.ModelChoiceField(queryset=YearOfStudy.objects.all(), label='Year')
    module = forms.ModelChoiceField(queryset=Modules.objects.all(), label='Module')
    

class CAForm(forms.Form):
    
    year = forms.IntegerField(
        label='Choose Year',
        widget=forms.NumberInput(attrs={'min': 2023, 'max': 3100, 'type': 'number'}),
        min_value=2023,
        max_value=3100
    )
    examsemester = forms.ChoiceField(
    label="Choose Semester",
    widget=forms.Select(attrs={'class': 'form-control'}),
    choices=(("Autumn", "Autumn"), ("Spring", "Spring")),
    )
    

    def clean_year(self):
        year = self.cleaned_data['year']
        if len(str(year)) != 4:
            raise forms.ValidationError("Year must be in YYYY format")
        return year
    
    exams = forms.ChoiceField(
    label="Choose examination type",
    widget=forms.Select(attrs={'class': 'form-control'}),
    choices=(("Semester End Examination", "Semester End Examination"), ("Mid Term Examination", "Mid Term Examination")),
    )
