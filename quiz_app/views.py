from django.shortcuts import render, get_object_or_404, redirect
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
                user_answers[question.id] = int(choice_id)

        user_score = 0 

        for question_id, user_choice_id in user_answers.items():
            question = get_object_or_404(Question, pk=question_id)
            correct_choice_ids = list(question.choice_set.filter(is_correct=True).values_list('id', flat=True))
            
           
            if not isinstance(user_choice_id, list):
                user_choice_id = [user_choice_id]

            
            if set(correct_choice_ids).issubset(user_choice_id):
                user_score += 1


        request.session['user_score'] = user_score

       
        return redirect('results', quiz_id=quiz.id)

   
    return render(request, 'quiz_app/quiz.html', {'quiz': quiz, 'questions': questions})

def results(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

   
    user_score = request.session.get('user_score', 0)

    total_questions = quiz.question_set.count()
    correct_answers = user_score  

    incorrect_answers = total_questions - correct_answers

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
        'score': user_score, 
    }

    return render(request, 'quiz_app/results.html', context)
