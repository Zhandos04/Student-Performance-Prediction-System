from django.contrib import admin
from .models import (
    Course, StudentCourse, Attendance, 
    Assignment, StudentAssignment, 
    Participation, PerformancePrediction
)

admin.site.register(Course)
admin.site.register(StudentCourse)
admin.site.register(Attendance)
admin.site.register(Assignment)
admin.site.register(StudentAssignment)
admin.site.register(Participation)
admin.site.register(PerformancePrediction)