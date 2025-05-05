from django.db import models
from apps.authentication.models import CustomUser

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название курса')
    code = models.CharField(max_length=20, verbose_name='Код курса')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class StudentCourse(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses', verbose_name='Студент')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students', verbose_name='Курс')
    
    class Meta:
        verbose_name = 'Курс студента'
        verbose_name_plural = 'Курсы студентов'
        unique_together = ('student', 'course')
    
    def __str__(self):
        return f"{self.student.username} - {self.course.name}"

class Attendance(models.Model):
    student_course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE, related_name='attendances', verbose_name='Курс студента')
    date = models.DateField(verbose_name='Дата')
    present = models.BooleanField(default=False, verbose_name='Присутствовал')
    
    class Meta:
        verbose_name = 'Посещаемость'
        verbose_name_plural = 'Посещаемость'
        unique_together = ('student_course', 'date')
    
    def __str__(self):
        return f"{self.student_course.student.username} - {self.student_course.course.name} - {self.date}"

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments', verbose_name='Курс')
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    due_date = models.DateField(verbose_name='Срок сдачи')
    max_score = models.PositiveIntegerField(default=100, verbose_name='Максимальный балл')
    
    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
    
    def __str__(self):
        return f"{self.course.name} - {self.title}"

class StudentAssignment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assignments', verbose_name='Студент')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='student_assignments', verbose_name='Задание')
    score = models.PositiveIntegerField(blank=True, null=True, verbose_name='Балл')
    submitted_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата сдачи')
    
    class Meta:
        verbose_name = 'Выполненное задание'
        verbose_name_plural = 'Выполненные задания'
        unique_together = ('student', 'assignment')
    
    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

class Participation(models.Model):
    student_course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE, related_name='participations', verbose_name='Курс студента')
    date = models.DateField(verbose_name='Дата')
    score = models.PositiveIntegerField(default=0, verbose_name='Балл')
    
    class Meta:
        verbose_name = 'Активность'
        verbose_name_plural = 'Активность'
        unique_together = ('student_course', 'date')
    
    def __str__(self):
        return f"{self.student_course.student.username} - {self.student_course.course.name} - {self.date}"

class PerformancePrediction(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='predictions', verbose_name='Студент')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='predictions', verbose_name='Курс')
    prediction_date = models.DateField(auto_now_add=True, verbose_name='Дата прогноза')
    predicted_score = models.FloatField(verbose_name='Прогнозируемый балл')
    confidence = models.FloatField(verbose_name='Уверенность прогноза')
    
    class Meta:
        verbose_name = 'Прогноз успеваемости'
        verbose_name_plural = 'Прогнозы успеваемости'
        ordering = ['-prediction_date']
    
    def __str__(self):
        return f"{self.student.username} - {self.course.name} - {self.prediction_date}"