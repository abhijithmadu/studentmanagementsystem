from django import forms
from .models import Assignment,Courses, Semester, Staffs,Subjects,Students
from django.forms import ChoiceField

class AssignementForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields =['answer']
# class EditResultForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         self.staff_id=kwargs.pop("staff_id")
#         staff = Staffs.objects.get(admin=self.staff_id)
#         course = Courses.objects.get(id=staff.course_id.id)
#         print(course)
#         super(EditResultForm,self).__init__(*args,**kwargs)
#         subject_list=[]
#         try:
#             subjects=Subjects.objects.filter(staff_id=self.staff_id)
#             for subject in subjects:
#                 subject_single=(subject.id,subject.subject_name)
#                 subject_list.append(subject_single)
#         except:
#             subject_list=[]
#             self.fields['subject_id'].choices=subject_list

#     semester_list=[]
#     course = Courses.objects.get(id=staff.course_id.id)
#     try:
#         semester = Semester.objects.filter(course_id=course)
#         for semester in semester:
#             semester_single=(semester.id,str(semester.semester_name))
#             semester_list.append(semester_single)
#     except:
#         semester_list=[]

#     subject_id=forms.ChoiceField(label="Subject",widget=forms.Select(attrs={"class":"form-control"}))
#     semester_ids=forms.ChoiceField(label="Semester",choices=semester_list,widget=forms.Select(attrs={"class":"form-control"}))
#     # student_ids=ChoiceNoValidation(label="Student",widget=forms.Select(attrs={"class":"form-control"}))
#     assignment_marks=forms.CharField(label="Assignment Marks",widget=forms.TextInput(attrs={"class":"form-control"}))
#     exam_marks=forms.CharField(label="Exam Marks",widget=forms.TextInput(attrs={"class":"form-control"}))

