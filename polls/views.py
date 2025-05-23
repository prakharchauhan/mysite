from django.db.models import F, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout, get_user_model
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question, CustomUser
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .forms import CustomUserCreationForm, OTPVerificationForm
from .tasks import send_otp_email
import random
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache

User = get_user_model()
@method_decorator(login_required(login_url='/polls/login/'), name='dispatch')
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        else:
            return Question.objects.filter(pub_date__lte=timezone.now(), is_restricted=False).order_by("-pub_date")[:5]


@method_decorator(login_required(login_url='/polls/login/'), name='dispatch')
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        user =self.request.user
        if user.is_staff:
            return Question.objects.filter(pub_date__lte=timezone.now())
        return Question.objects.filter(pub_date__lte=timezone.now(), is_restricted=False)
    
@method_decorator(login_required(login_url='/polls/login/'), name='dispatch')
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def custom_login(request):
    #import pdb;pdb.set_trace()
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        
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
    user = request.user
    if question.is_restricted and not user.is_staff:
        messages.error(request, "You cant vote on this question")
        return reverse("polls:detail", kwargs={"pk": question.id})

    if user.is_staff:
        var = 100
    else:
        var =10
    total_votes = Choice.objects.filter(voter=request.user).count()
    print(total_votes)
    if total_votes>=var:
        messages.error(request, "You have exceeded the 10 vote limit")
        return redirect("polls:login")
    try:
        if question.is_multiple_choice:
            selected_choices = request.POST.getlist("choices")
            if not selected_choices:
                messages.error(request, "Select at least one")
                return redirect("polls:login")
            if total_votes + len(selected_choices)>=var:
                messages.error(request, "You have exceeded the 10 vote limit")
                return redirect("polls:login")
            for chid in selected_choices:
                choice = get_object_or_404(Choice, pk=chid)
                choice.votes = F("votes")+1
                choice.save()
                choice.voter.add(request.user)
        else:
            
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
            if total_votes + 1>=var:
                messages.error(request, "You have exceeded the 10 vote limit")
                return redirect("polls:login")
            selected_choice.votes = F("votes") + 1
            selected_choice.save()
            selected_choice.voter.add(request.user)
        
    except (KeyError, Choice.DoesNotExist):
        
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            #user = form.save()
            #login(request, user) 
            request.session["registration_data"]=form.cleaned_data
            email = form.cleaned_data["email"]
            otp =str(random.randint(100000, 999999))
            request.session["otp"] = otp
            send_otp_email.delay(email, otp)
            messages.success(request, "OTP has been sent to your email.")
            return redirect("polls:verify")
        
        else:
            print(form.errors)
            messages.error(request, "Registration failed. Please check the details.")
            return render(request, "polls/register.html", {"form": form})
    else:
        form = CustomUserCreationForm()
    
    return render(request, "polls/register.html", {"form": form})

def otp_verify(request):
    
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        stored_otp = request.session.get("otp")
        registration_data = request.session.get("registration_data")

        if not stored_otp or not registration_data:
            messages.error(request, "Session expired or invalid request. Please register again.")
            return redirect("polls:register")

        if entered_otp == stored_otp:
            
            user = CustomUser.objects.create_user(
                email=registration_data["email"],
                full_name=registration_data["full_name"],
                password=registration_data["password1"]
            )

            del request.session["otp"]
            del request.session["registration_data"]

            login(request, user)
            messages.success(request, "Account created successfully! You are now logged in.")
            return redirect("polls:index")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "polls/verify.html")

"""def go_home(request):
    return reverse("polls:index")"""

def debug_cookies(request):
    return JsonResponse(dict(request.COOKIES))