from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Sum
from .models import (
    Course, StudentCourse, Attendance, 
    Assignment, StudentAssignment, 
    Participation, PerformancePrediction
)
from apps.authentication.models import CustomUser
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from .ml_models.predict import predict_student_performance

@login_required
def dashboard_view(request):
    user = request.user
    
    # Получаем курсы студента
    student_courses = StudentCourse.objects.filter(student=user)
    
    # Получаем последние прогнозы для студента
    predictions = PerformancePrediction.objects.filter(
        student=user
    ).order_by('-prediction_date')[:5]
    
    # Получаем данные о посещаемости
    attendance_data = Attendance.objects.filter(
        student_course__student=user
    ).values('date', 'present').order_by('date')
    
    # Преобразуем данные посещаемости для визуализации
    attendance_df = pd.DataFrame(list(attendance_data))
    if not attendance_df.empty:
        attendance_df['date'] = pd.to_datetime(attendance_df['date'])
        attendance_df['month'] = attendance_df['date'].dt.month_name()
        monthly_attendance = attendance_df.groupby('month')['present'].mean() * 100
        
        attendance_labels = monthly_attendance.index.tolist()
        attendance_values = monthly_attendance.values.tolist()
    else:
        attendance_labels = []
        attendance_values = []
    
    # Получаем данные о баллах по заданиям
    assignment_data = StudentAssignment.objects.filter(
        student=user
    ).select_related('assignment')
    
    # Преобразуем данные о заданиях для визуализации
    assignment_scores = []
    for assignment in assignment_data:
        if assignment.score is not None:
            percentage = (assignment.score / assignment.assignment.max_score) * 100
            assignment_scores.append({
                'title': assignment.assignment.title,
                'percentage': percentage
            })
    
    # Получаем данные для прогнозирования успеваемости
    # Предполагаем, что у нас есть модель ML, которая делает прогнозы
    try:
        predictions_data = []
        for course in student_courses:
            # Получаем историческую и текущую информацию о студенте
            attendance_rate = Attendance.objects.filter(
                student_course=course, present=True
            ).count() / Attendance.objects.filter(student_course=course).count() * 100 if Attendance.objects.filter(student_course=course).count() > 0 else 0
            
            participation_score = Participation.objects.filter(
                student_course=course
            ).aggregate(avg_score=Avg('score'))['avg_score'] or 0
            
            avg_assignment_score = StudentAssignment.objects.filter(
                student=user,
                assignment__course=course.course
            ).aggregate(avg_score=Avg('score'))['avg_score'] or 0
            
            # Вызываем функцию прогнозирования
            predicted_score, confidence = predict_student_performance(
                attendance_rate, participation_score, avg_assignment_score
            )
            
            # Сохраняем прогноз в базу данных
            PerformancePrediction.objects.create(
                student=user,
                course=course.course,
                predicted_score=predicted_score,
                confidence=confidence
            )
            
            predictions_data.append({
                'course': course.course.name,
                'predicted_score': predicted_score,
                'confidence': confidence
            })
    except Exception as e:
        print(f"Error in prediction: {e}")
        predictions_data = []
    
    context = {
        'user': user,
        'student_courses': student_courses,
        'predictions': predictions,
        'attendance_labels': attendance_labels,
        'attendance_values': attendance_values,
        'assignment_scores': assignment_scores,
        'predictions_data': predictions_data,
    }
    
    return render(request, 'dashboard/dashboard.html', context)