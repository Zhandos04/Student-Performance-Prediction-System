from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def settings_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Важно, чтобы пользователь не выходил из системы
            messages.success(request, 'Ваш пароль был успешно изменен!')
            return redirect('settings')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки, указанные ниже.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'settings/settings.html', {
        'form': form
    })