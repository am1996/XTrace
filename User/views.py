from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, RedirectURLMixin
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required  
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from urllib.parse import urlsplit
# Create your views here.

class UserDashboard(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'User/details.html'
    context_object_name = 'users'
    def get_object(self, queryset = ...):
        if self.request.user.is_authenticated:
            return get_object_or_404(User, pk=self.request.user.pk)
        return None

class UserDelete(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'User/delete.html'
    success_url = reverse_lazy('user:user_dashboard')
    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user

# Logged in users can not access this view, and will be redirected to the dashboard

class UserLogin(LoginView):
    next_page = '/'
    template_name = 'User/login.html'
    redirect_authenticated_user = True
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

class UserLogout(LogoutView):
    next_page = 'user:user_login'


class UserRegister(CreateView,RedirectURLMixin):
    model = User
    redirect_authenticated_user = True
    form_class = UserCreationForm
    template_name = 'User/register.html'
    success_url = reverse_lazy('user:user_login')
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = "/"
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

class UserDetails(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'User/details.html'
    context_object_name = 'user'

class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'update.html'
    success_url = reverse_lazy('user:user_list')
    context_object_name = 'user'
