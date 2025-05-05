from django.contrib import admin
from .models import SupportTicket, SupportTicketResponse

class SupportTicketResponseInline(admin.TabularInline):
    model = SupportTicketResponse
    extra = 0

class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('subject', 'description', 'user__username')
    inlines = [SupportTicketResponseInline]

admin.site.register(SupportTicket, SupportTicketAdmin)
admin.site.register(SupportTicketResponse)