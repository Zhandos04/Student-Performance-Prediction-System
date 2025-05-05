from django.db import models
from django.utils import timezone
from apps.authentication.models import CustomUser

class SupportTicket(models.Model):
    STATUS_CHOICES = (
        ('open', 'Открыто'),
        ('in_progress', 'В процессе'),
        ('resolved', 'Решено'),
        ('closed', 'Закрыто'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='support_tickets', verbose_name='Пользователь')
    subject = models.CharField(max_length=100, verbose_name='Тема')
    description = models.TextField(verbose_name='Описание')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name='Статус')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Тикет поддержки'
        verbose_name_plural = 'Тикеты поддержки'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.subject}"

class SupportTicketResponse(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='responses', verbose_name='Тикет')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Ответ на тикет'
        verbose_name_plural = 'Ответы на тикеты'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.ticket.subject} - {self.user.username}"
