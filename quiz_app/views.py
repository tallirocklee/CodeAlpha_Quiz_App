from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, render, redirect
from .models import Quiz, Question, Choice

def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_app/home.html', {'quizzes': quizzes})

def quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.question_set.all()

    if request.method == 'POST':
        user_answers = {}
        for question in questions:
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id is not None:
                user_answers[question.id] = choice_id

        request.session['user_answers'] = user_answers
        return redirect('results', quiz_id=quiz.id)

    return render(request, 'quiz_app/quiz.html', {'quiz': quiz, 'questions': questions})

def results(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    user_answers = request.session.get('user_answers', {})

    total_questions = quiz.question_set.count()
    correct_answers = 0
    incorrect_answers = 0
    detailed_results = []

    for question in quiz.question_set.all():
        user_answer = user_answers.get(str(question.id), None)
        if user_answer is not None:
            user_answer = int(user_answer)
            correct_choice_ids = list(question.choice_set.filter(is_correct=True).values_list('id', flat=True))
            correct_choices_text = list(Choice.objects.filter(id__in=correct_choice_ids).values_list('text', flat=True))
            if user_answer in correct_choice_ids:
                correct_answers += 1
                detailed_results.append({'question_text': question.text, 'user_answer': user_answer, 'correct': True})
            else:
                incorrect_answers += 1
                detailed_results.append({'question_text': question.text, 'user_answer': user_answer, 'correct': False, 'correct_answers_text': correct_choices_text})
        else:
            detailed_results.append({'question_text': question.text, 'user_answer': 'Not attempted', 'correct': False})

    if total_questions > 0:
        percentage_correct = (correct_answers / total_questions) * 100
    else:
        percentage_correct = 0

    context = {
        'quiz': quiz,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'percentage_correct': percentage_correct,
        'score': correct_answers,
        'detailed_results': detailed_results
    }

    return render(request, 'quiz_app/results.html', context)
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'quiz_app/signup.html', {'form': form})
