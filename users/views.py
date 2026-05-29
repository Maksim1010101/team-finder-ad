from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from .forms import RegistrationForm, LoginForm, UserEditForm, UserChangePasswordForm
from django.contrib.auth import login
from .models import User

class UsersListView(ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participants'
    def get_queryset(self):
        queryset = User.objects.filter(is_active=True).order_by('id')
        return queryset

class UserDetailView(DetailView):
    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'user'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.object.owned_projects.all()
        return context

def register_user(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('projects:project_list')

    return render(request, 'users/register.html', {'form': form})

def login_user(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = form.user
        login(request, user)
        return redirect('projects:project_list')
    return render(request, 'users/login.html', {'form': form})

class UserEditView(UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'users/edit_profile.html'
    context_object_name = 'user'

    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:detail', kwargs={'user_id': self.object.pk})

class UserChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    model = User
    form_class = UserChangePasswordForm
    template_name = 'users/change_password.html'

    def form_valid(self, form):
        if form.is_valid():
            return super().form_valid(form)

def logout_user(request):
    logout(request)
    return redirect('projects:project_list')