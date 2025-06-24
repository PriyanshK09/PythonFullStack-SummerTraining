from django.shortcuts import render, redirect
from django import forms

tasks = {}

class TaskForm(forms.Form):
    task = forms.CharField(label='New Task', max_length=100)

def index(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task_id = len(tasks) + 1
            tasks[task_id] = form.cleaned_data['task']
            return redirect('/')
    else:
        form = TaskForm()
    return render(request, 'index.html', {'form': form, 'tasks': tasks})

def delete_task(request, task_id):
    tasks.pop(task_id, None)
    return redirect('/')
