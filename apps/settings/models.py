from django.db import models
from apps.authentication.models import CustomUser

class UserPreference(models.Model):
    THEME_CHOICES = (
        ('light', 'Светлая тема'),
        ('dark', 'Темная тема'),
    )
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='preferences', verbose_name='Пользователь')
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light', verbose_name='Тема')
    
    class Meta:
        verbose_name = 'Настройка пользователя'
        verbose_name_plural = 'Настройки пользователей'
    
    def __str__(self):
        return f"{self.user.username} - {self.theme}"
