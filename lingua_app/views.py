from django.shortcuts import render, redirect
from .data import LESSONS
from .forms import SettingsForm
import json

# Главная страница (список уроков)
def index(request):
    progress = request.COOKIES.get('progress')
    if progress:
        progress = json.loads(progress)
    else:
        progress = {}

    # Добавляем прогресс каждому уроку
    lessons_with_progress = []
    for l in LESSONS:
        lesson_copy = l.copy()
        lesson_copy['progress'] = progress.get(str(l['id']), 0)
        lessons_with_progress.append(lesson_copy)

    context = {
        'lessons': lessons_with_progress,
        'theme': request.COOKIES.get('theme', 'light')
    }
    return render(request, 'lingua_app/index.html', context)

# Страница конкретного урока
def lesson_view(request, lesson_id):
    lesson = next((l for l in LESSONS if l['id'] == lesson_id), None)
    if not lesson:
        return redirect('lingua_app:index')

    progress = request.COOKIES.get('progress')
    if progress:
        progress = json.loads(progress)
    else:
        progress = {}

    # Помечаем урок как пройденный (100%)
    progress[str(lesson_id)] = 100

    lesson_copy = lesson.copy()
    lesson_copy['progress'] = progress[str(lesson_id)]

    context = {
        'lesson': lesson_copy,
        'theme': request.COOKIES.get('theme', 'light')
    }
    response = render(request, 'lingua_app/lesson.html', context)
    response.set_cookie('progress', json.dumps(progress))
    return response

# Настройки приложения (тема)
def settings_view(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            theme = form.cleaned_data['theme']
            response = redirect('lingua_app:index')
            response.set_cookie('theme', theme)
            return response
    else:
        form = SettingsForm(initial={'theme': request.COOKIES.get('theme', 'light')})

    context = {
        'form': form,
        'theme': request.COOKIES.get('theme', 'light')
    }
    return render(request, 'lingua_app/settings.html', context)

# Сброс прогресса
def reset_progress(request):
    response = redirect('lingua_app:index')
    response.delete_cookie('progress')
    return response