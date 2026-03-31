from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Quiz, QuizAttempt, Question, Choice
from apps.courses.models import Lesson, Enrollment


@login_required
def take_quiz(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    quiz = get_object_or_404(Quiz, lesson=lesson)

    enrollment = get_object_or_404(Enrollment, user=request.user, course=lesson.course)
    questions = quiz.questions.prefetch_related('choices').all()

    if request.method == 'POST':
        answers = {}
        correct = 0
        for question in questions:
            choice_id = request.POST.get(f'q_{question.pk}')
            answers[str(question.pk)] = int(choice_id) if choice_id else None
            if choice_id:
                try:
                    choice = Choice.objects.get(pk=choice_id, question=question)
                    if choice.is_correct:
                        correct += 1
                except Choice.DoesNotExist:
                    pass

        total = questions.count()
        score = int((correct / total) * 100) if total > 0 else 0
        passed = score >= quiz.passing_score

        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            passed=passed,
            answers=answers,
        )
        return redirect('quizzes:result', attempt_id=attempt.pk)

    context = {
        'quiz': quiz,
        'lesson': lesson,
        'questions': questions,
    }
    return render(request, 'courses/quiz.html', context)


@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, pk=attempt_id, user=request.user)
    questions = attempt.quiz.questions.prefetch_related('choices').all()

    context = {
        'attempt': attempt,
        'questions': questions,
    }
    return render(request, 'courses/quiz_result.html', context)
