from django.db import models
from django.contrib.auth.models import User
from apps.courses.models import Lesson


class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=200)
    passing_score = models.PositiveIntegerField(default=70, help_text='Minimum % to pass')
    time_limit_minutes = models.PositiveIntegerField(default=0, help_text='0 = no limit')

    def __str__(self):
        return f'Quiz: {self.title}'

    @property
    def question_count(self):
        return self.questions.count()


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    explanation = models.TextField(blank=True, help_text='Shown after answering')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'Q{self.order}: {self.text[:60]}'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        marker = '✓' if self.is_correct else '✗'
        return f'{marker} {self.text}'


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)
    answers = models.JSONField(default=dict, help_text='{"question_id": choice_id}')

    class Meta:
        ordering = ['-attempted_at']

    def __str__(self):
        return f'{self.user.username} — {self.quiz.title} ({self.score}%)'
