from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SupportTicket, SupportTicketResponse

@login_required
def support_view(request):
    tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'tickets': tickets
    }
    
    return render(request, 'support/support.html', context)