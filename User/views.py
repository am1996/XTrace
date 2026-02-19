from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout as auth_logout
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required  
from django.urls import reverse_lazy
from django.contrib.auth.models import User
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

def logout_view(request):
    """Simple logout view that works with GET and POST and redirects to login."""
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect(reverse_lazy('user:login'))


class UserRegister(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'User/register.html'
    success_url = reverse_lazy('user:login')
    
    def dispatch(self, request, *args, **kwargs):
        # Only Admin or SuperUser group can register users
        if not request.user.is_superuser and not request.user.groups.filter(name__in=['Admin', 'SuperUser']).exists():
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden('Access denied. Admin or SuperUser group required to register users.')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Add new users to Operator group by default
        from django.contrib.auth.models import Group
        operator_group = Group.objects.get(name='Operator')
        self.object.groups.add(operator_group)
        return response

class UserDetails(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'User/details.html'
    context_object_name = 'user'

class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'User/update.html'
    success_url = reverse_lazy('user:dashboard')
    context_object_name = 'user'
