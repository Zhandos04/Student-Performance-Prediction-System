from django.core.management.base import BaseCommand
from apps.authentication.models import CustomUser
from apps.dashboard.models import (
    Course, StudentCourse, Attendance, 
    Assignment, StudentAssignment, 
    Participation, PerformancePrediction
)
from apps.notification.models import Notification
from django.utils import timezone
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Initializes the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Initializing database with sample data...')
        
        try:
            # Создаем тестового пользователя, если его еще нет
            if not CustomUser.objects.filter(username='student1').exists():
                test_user = CustomUser.objects.create_user(
                    username='student1',
                    email='student1@example.com',
                    password='password123',
                    student_number='ST12345'
                )
                self.stdout.write(self.style.SUCCESS('Created test user: student1'))
            else:
                test_user = CustomUser.objects.get(username='student1')
                self.stdout.write('Test user already exists: student1')
            
            # Создаем курсы
            courses_data = [
                {'name': 'Математический анализ', 'code': 'MATH101'},
                {'name': 'Введение в программирование', 'code': 'CS101'},
                {'name': 'Статистика', 'code': 'STAT201'},
                {'name': 'Машинное обучение', 'code': 'CS301'},
            ]
            
            courses = []
            for course_data in courses_data:
                course, created = Course.objects.get_or_create(
                    code=course_data['code'],
                    defaults={'name': course_data['name']}
                )
                courses.append(course)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created course: {course.name}'))
                else:
                    self.stdout.write(f'Course already exists: {course.name}')
            
            # Связываем студента с курсами
            for course in courses:
                student_course, created = StudentCourse.objects.get_or_create(
                    student=test_user,
                    course=course
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Enrolled {test_user.username} in {course.name}'))
                else:
                    self.stdout.write(f'{test_user.username} already enrolled in {course.name}')
            
            # Создаем данные о посещаемости
            today = timezone.now().date()
            start_date = today - timedelta(days=90)  # 3 месяца назад
            
            for student_course in StudentCourse.objects.filter(student=test_user):
                current_date = start_date
                while current_date <= today:
                    # Случайно пропускаем некоторые дни (выходные)
                    if current_date.weekday() < 5:  # Понедельник - Пятница
                        attendance, created = Attendance.objects.get_or_create(
                            student_course=student_course,
                            date=current_date,
                            defaults={'present': random.random() > 0.2}  # 80% вероятность присутствия
                        )
                        if created:
                            self.stdout.write(f'Created attendance record for {student_course.student.username} on {current_date}')
                    
                    current_date += timedelta(days=1)
            
            # Создаем задания
            for course in courses:
                for i in range(1, 6):  # 5 заданий на курс
                    due_date = today + timedelta(days=random.randint(7, 30))
                    assignment, created = Assignment.objects.get_or_create(
                        course=course,
                        title=f'Задание {i}',
                        defaults={
                            'description': f'Описание для задания {i} курса {course.name}',
                            'due_date': due_date,
                            'max_score': 100
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created assignment: {assignment.title} for {course.name}'))
                    
                    # Создаем выполненные задания для прошедших сроков
                    if assignment.due_date < today:
                        student_assignment, created = StudentAssignment.objects.get_or_create(
                            student=test_user,
                            assignment=assignment,
                            defaults={
                                'score': random.randint(60, 100),
                                'submitted_date': assignment.due_date - timedelta(days=random.randint(0, 5))
                            }
                        )
                        if created:
                            self.stdout.write(f'Created student assignment for {test_user.username}')
            
            # Создаем данные об активности
            for student_course in StudentCourse.objects.filter(student=test_user):
                current_date = start_date
                while current_date <= today:
                    # Случайно добавляем активность в учебные дни
                    if current_date.weekday() < 5:  # Понедельник - Пятница
                        if random.random() > 0.3:  # 70% вероятность записи активности
                            participation, created = Participation.objects.get_or_create(
                                student_course=student_course,
                                date=current_date,
                                defaults={'score': random.randint(0, 10)}
                            )
                            if created:
                                self.stdout.write(f'Created participation record for {student_course.student.username} on {current_date}')
                    
                    current_date += timedelta(days=1)
            
            # Создаем уведомления
            notification_data = [
                {
                    'title': 'Новое задание',
                    'message': 'Вам назначено новое задание по курсу "Математический анализ". Срок сдачи - 15 мая.',
                    'type': 'assignment'
                },
                {
                    'title': 'Скоро дедлайн',
                    'message': 'Напоминание: срок сдачи задания по "Введение в программирование" истекает через 2 дня.',
                    'type': 'deadline'
                },
                {
                    'title': 'Выставлена оценка',
                    'message': 'Ваша работа по курсу "Статистика" оценена на 85 баллов.',
                    'type': 'grade'
                },
                {
                    'title': 'Объявление по курсу',
                    'message': 'Занятие по "Машинное обучение" в пятницу переносится на 15:00.',
                    'type': 'announcement'
                },
                {
                    'title': 'Обновление системы',
                    'message': 'Система прогнозирования успеваемости была обновлена. Теперь доступны новые функции.',
                    'type': 'system'
                }
            ]
            
            for data in notification_data:
                notification, created = Notification.objects.get_or_create(
                    user=test_user,
                    title=data['title'],
                    defaults={
                        'message': data['message'],
                        'notification_type': data['type'],
                        'created_at': timezone.now() - timedelta(days=random.randint(0, 10)),
                        'read': random.choice([True, False])
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created notification: {notification.title}'))
            
            self.stdout.write(self.style.SUCCESS('Successfully initialized database with sample data!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error initializing database: {e}'))