from django.shortcuts import render, redirect
from django import forms
import sqlite3
import os

class TaskForm(forms.Form):
    task = forms.CharField(label='New Task', max_length=100)

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'tasks.db')
    conn = sqlite3.connect(db_path)
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)''')
    return conn

def index(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            conn = get_db_connection()
            conn.execute('INSERT INTO tasks (task) VALUES (?)', (form.cleaned_data['task'],))
            conn.commit()
            conn.close()
            return redirect('/')
    else:
        form = TaskForm()
    
    conn = get_db_connection()
    cursor = conn.execute('SELECT id, task FROM tasks')
    tasks = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    
    return render(request, 'index.html', {'form': form, 'tasks': tasks})

def delete_task(request, task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

def edit_task(request, task_id):
    conn = get_db_connection()
    cursor = conn.execute('SELECT task FROM tasks WHERE id = ?', (task_id,))
    task_row = cursor.fetchone()
    
    if not task_row:
        conn.close()
        return redirect('/')
        
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            conn.execute('UPDATE tasks SET task = ? WHERE id = ?', 
                        (form.cleaned_data['task'], task_id))
            conn.commit()
            conn.close()
            return redirect('/')
    else:
        initial_data = {'task': task_row[0]}
        form = TaskForm(initial=initial_data)
    
    conn.close()
    return render(request, 'edit_task.html', {
        'form': form, 
        'task_id': task_id,
        'current_task': task_row[0] if task_row else ''
    })