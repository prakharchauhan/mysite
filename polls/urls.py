from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    #path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('login/', views.custom_login, name='login'),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("login/", views.custom_login, name="login"),
    path("logout/", views.custom_logout, name="logout"),
    path("register/", views.register, name="register"),
    path("verify/", views.otp_verify, name="verify"),
    path("debug_cookies/", views.debug_cookies, name="debug_cookies")
]