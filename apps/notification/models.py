from django.db import models
from django.utils import timezone
from apps.authentication.models import CustomUser

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('assignment', 'Задание'),
        ('deadline', 'Срок сдачи'),
        ('grade', 'Оценка'),
        ('announcement', 'Объявление'),
        ('system', 'Системное'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications', verbose_name='Пользователь')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    message = models.TextField(verbose_name='Сообщение')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, verbose_name='Тип уведомления')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    read = models.BooleanField(default=False, verbose_name='Прочитано')
    
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"