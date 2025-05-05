from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.utils import timezone
from .models import Course, Assignment, Grade, Attendance, Participation, Prediction
from .forms import CourseForm, AssignmentForm, GradeForm, AttendanceForm, ParticipationForm
from accounts.models import User
from ml_model.predictor import predict_student_performance

@login_required
def dashboard(request):
    if request.user.role == 'student':
        # Данные для студентов
        courses = request.user.enrolled_courses.all()
        recent_grades = Grade.objects.filter(student=request.user).order_by('-submitted_at')[:5]
        attendance_rates = {}
        for course in courses:
            total_classes = Attendance.objects.filter(course=course, student=request.user).count()
            if total_classes > 0:
                present_count = Attendance.objects.filter(course=course, student=request.user, is_present=True).count()
                attendance_rates[course.name] = (present_count / total_classes) * 100
            else:
                attendance_rates[course.name] = 0
        
        predictions = Prediction.objects.filter(student=request.user)
        predictions_data = {p.course.name: p.predicted_score for p in predictions}
        
        context = {
            'courses': courses,
            'recent_grades': recent_grades,
            'attendance_rates': attendance_rates,
            'predictions': predictions_data,
        }
        return render(request, 'dashboard/student_dashboard.html', context)
    
    elif request.user.role == 'admin':
        # Данные для администраторов
        total_students = User.objects.filter(role='student').count()
        total_courses = Course.objects.count()
        recent_predictions = Prediction.objects.all().order_by('-created_at')[:10]
        
        context = {
            'total_students': total_students,
            'total_courses': total_courses,
            'recent_predictions': recent_predictions,
        }
        return render(request, 'dashboard/admin_dashboard.html', context)
    
    return render(request, 'dashboard/dashboard.html')

@login_required
def notifications(request):
    # Логика получения уведомлений будет добавлена позже
    return render(request, 'dashboard/notifications.html')

@login_required
def support(request):
    return render(request, 'dashboard/support.html')

@login_required
def settings(request):
    return render(request, 'dashboard/settings.html')

@staff_member_required
def admin_courses(request):
    courses = Course.objects.all()
    form = CourseForm()
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_courses')
    
    context = {
        'courses': courses,
        'form': form,
    }
    return render(request, 'dashboard/admin_courses.html', context)

@staff_member_required
def admin_students(request):
    students = User.objects.filter(role='student')
    context = {
        'students': students,
    }
    return render(request, 'dashboard/admin_students.html', context)

@staff_member_required
def run_predictions(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        
        for student in course.students.all():
            # Получение данных для прогнозирования
            grades = Grade.objects.filter(student=student, assignment__course=course)
            avg_grade = grades.aggregate(Avg('score'))['score__avg'] or 0
            
            attendance = Attendance.objects.filter(student=student, course=course)
            attendance_rate = (attendance.filter(is_present=True).count() / attendance.count()) * 100 if attendance.count() > 0 else 0
            
            participation = Participation.objects.filter(student=student, course=course)
            avg_participation = participation.aggregate(Avg('level'))['level__avg'] or 0
            
            # Вызов функции прогнозирования
            prediction, confidence = predict_student_performance(avg_grade, attendance_rate, avg_participation)
            
            # Сохранение результата
            Prediction.objects.update_or_create(
                student=student,
                course=course,
                defaults={
                    'predicted_score': prediction,
                    'confidence': confidence,
                }
            )
        
        return redirect('admin_courses')
    
    return redirect('admin_courses')