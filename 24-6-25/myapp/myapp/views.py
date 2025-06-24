from django.shortcuts import render, redirect
from django import forms

tasks = {}

class TaskForm(forms.Form):
    task = forms.CharField(label='New Task', max_length=100)

def index(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Generate new task ID
            task_id = max(tasks.keys()) + 1 if tasks else 1
            tasks[task_id] = form.cleaned_data['task']
            return redirect('/')
    else:
        form = TaskForm()
    return render(request, 'index.html', {'form': form, 'tasks': tasks})

def delete_task(request, task_id):
    tasks.pop(task_id, None)
    return redirect('/')

def edit_task(request, task_id):
    if task_id not in tasks:
        return redirect('/')
        
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            tasks[task_id] = form.cleaned_data['task']
            return redirect('/')
    else:
        initial_data = {'task': tasks.get(task_id, '')}
        form = TaskForm(initial=initial_data)
    
    return render(request, 'edit_task.html', {
        'form': form, 
        'task_id': task_id,
        'current_task': tasks.get(task_id, '')
    })