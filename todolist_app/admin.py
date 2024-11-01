from django.contrib import admin
from todolist_app.models import TaskList, ContactFormLog

# Register your models here.
admin.site.register(TaskList)

@admin.register(ContactFormLog)
class ContactFormLogAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'subject',
        'is_success',
        'action_time',
    ]