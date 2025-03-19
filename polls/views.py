from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils.decorators import method_decorator

@method_decorator(login_required(login_url='/polls/login/'), name='dispatch')
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

@method_decorator(login_required(login_url='/polls/login/'), name='dispatch')
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        
        return Question.objects.filter(pub_date__lte=timezone.now())
@method_decorator(login_required(login_url='/polls/login/'), name='dispatch')
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def custom_login(request):
    #import pdb;pdb.set_trace()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', reverse("polls:index"))
            return HttpResponseRedirect(next_url)       
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, "polls/login.html")

def custom_logout(request):
    
    logout(request)
    return redirect("polls:login")

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        selected_choice.voter.add(request.user)
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect("polls:index")
        else:
            messages.error(request, "Registration failed. Please check the details.")
    else:
        form = UserCreationForm()
    
    return render(request, "polls/register.html", {"form": form})