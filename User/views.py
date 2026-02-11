from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView,DetailView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
# Create your views here.

class UserLogin(LoginView):
    next_page = ''
    template_name = 'User/login.html'
    redirect_authenticated_user = True
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

class UserLogout(LogoutView):
    next_page = 'user:user_login'

class UserRegister(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'User/register.html'
    success_url = reverse_lazy('user:user_login')
    
class UserDetails(DetailView):
    model = User
    template_name = 'User/details.html'
    context_object_name = 'user'