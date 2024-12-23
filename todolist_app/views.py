from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from todolist_app.models import TaskList, ContactFormLog
from todolist_app.forms import TaskForm
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone


# Create your views here.
@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
        messages.success(request, ("New Task Added!"))
        return redirect('todolist')
    else:
        all_tasks = TaskList.objects.filter(owner=request.user)
        paginator = Paginator(all_tasks, 5)
        page = request.GET.get('page')
        all_tasks = paginator.get_page(page)
        
        return render(request, 'todolist.html', {'all_tasks': all_tasks})


@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
        messages.success(request, ("Task Edited!"))
        return redirect('todolist')
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request, 'edit.html', {'task_obj': task_obj})


@login_required    
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request, ("Access restricted, you are not allowed."))
    
    return redirect('todolist')


@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:
        task.done = False
        task.save()
    else:
        messages.error(request, ("Access restricted, you are not allowed."))
    return redirect('todolist')


@login_required    
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:
        task.delete()
    else:
        messages.error(request, "Access restricted, you are not allowed.")
    return redirect('todolist')


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = f"Taskmate Contact Us: {request.POST.get('subject')}"
        message = request.POST.get("message")
        
        html_content = render_to_string(
            template_name="email.html",
            context={
                "name": name,
                "email": email,
                "subject": subject,
                "message": message,
            },
        )
        
        is_success = False
        error_message = ""
        
        try:
            send_mail(
                subject=subject,
                message=None,
                html_message=html_content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        except Exception as e:
            error_message = str(e)
            messages.error(request, "There is an error, could not sent the message.")
        else:
            is_success = True
            messages.success(request, "Message sent!")
            
        ContactFormLog.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
            action_time=timezone.now(),
            is_success=is_success,
            error_message=error_message
        )
    
    context = {
        'contact_text': "Contact Us",
    }
    return render(request, 'contact.html', context)


def about(request):
    context = {
        'about_text': "About Us",
    }
    return render(request, 'about.html', context)


def index(request):
    context = {
        'index_text': "Welcome to Index Page.",
    }
    return render(request, 'index.html', context)
