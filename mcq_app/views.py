from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import QuizProfile, Question, AttemptedQuestion, Story
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, UserLoginForm
# # Create your views here

def home(request):
    context = {}
    return render(request, 'mcq_app/home.html', context=context)

@login_required()
def index(request):
    return render(request, 'mcq_app/index.html')

@login_required()
def quiz(request):
    storys = Story.objects.all()
    quiz_profile, created = QuizProfile.objects.get_or_create(user=request.user)
    
    percent = quiz_profile.update_score()

    if request.method == 'POST':
        question_pk = request.POST.get('question_pk')

        attempted_question = quiz_profile.attempts.select_related('question').get(question__pk=question_pk)
        choice_pk = request.POST.get('choice_pk')

        try:
            selected_choice = attempted_question.question.choices.get(pk=choice_pk)
        except ObjectDoesNotExist:
            raise Http404

        quiz_profile.evaluate_attempt(attempted_question, selected_choice)

        return redirect(attempted_question)

    else:
        question = quiz_profile.get_new_question()
        if question is not None:
            quiz_profile.create_attempt(question)

        context = {
            'question': question,
            'storys': storys,
            'percent': percent
        }

        return render(request, 'mcq_app/quiz.html', context)

@login_required()
def submission_result(request, attempted_question_pk):
    attempted_question = get_object_or_404(AttemptedQuestion, pk=attempted_question_pk)
    context = {
        'attempted_question': attempted_question,
    }
    return render(request, 'mcq_app/submission_result.html', context=context)

@login_required()
def countdown(request):
    return redirect('/quiz')


def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/index')
    return render(request, 'mcq_app/login.html', {"form": form, "title": title})


def register(request):
    title = "Create account"
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = RegistrationForm()

    context = {'form': form, 'title': title}
    return render(request, 'mcq_app/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')