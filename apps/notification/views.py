from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'notifications': notifications
    }
    
    # Отмечаем все уведомления как прочитанные
    notifications.update(read=True)
    
    return render(request, 'notification/notification.html', context)
