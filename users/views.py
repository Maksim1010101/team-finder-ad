from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView

from core.constants import PAGE_SIZE
from projects.models import Project
from users.forms import (
    LoginForm,
    RegistrationForm,
    UserChangePasswordForm,
    UserEditForm,
)
from users.models import User


class UsersListView(ListView):
    model = User
    template_name = "users/participants.html"
    paginate_by = PAGE_SIZE
    context_object_name = "participants"

    def get_queryset(self):
        qs = User.objects.filter(is_active=True).order_by("id")

        if self.request.user.is_authenticated:
            filter_type = self.request.GET.get("filter")
            user = self.request.user
            if filter_type == "owners-of-favorite-projects":
                fav_projects = user.favorites.all()
                qs = User.objects.filter(owned_projects__in=fav_projects).distinct()
            elif filter_type == "owners-of-participating-projects":
                participated_projects = Project.objects.filter(participants=user)
                qs = User.objects.filter(
                    owned_projects__in=participated_projects
                ).distinct()
            elif filter_type == "interested-in-my-projects":
                my_projects = user.owned_projects.all()
                qs = User.objects.filter(favorites__in=my_projects).distinct()
            elif filter_type == "participants-of-my-projects":
                my_projects = user.owned_projects.all()
                qs = (
                    User.objects.filter(participated_projects__in=my_projects)
                    .exclude(id=user.id)
                    .distinct()
                )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_filter"] = self.request.GET.get("filter")
        # Сохраняем параметры фильтра для пагинации
        query_params = self.request.GET.copy()
        if "page" in query_params:
            del query_params["page"]
        context["query_prefix"] = query_params.urlencode()
        if context["query_prefix"]:
            context["query_prefix"] += "&"
        return context


class UserDetailView(DetailView):
    model = User
    template_name = "users/user-details.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = self.object.owned_projects.all()
        return context


def register_user(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("projects:project_list")
    return render(request, "users/register.html", {"form": form})


def login_user(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = form.user
        login(request, user)
        return redirect("projects:project_list")
    return render(request, "users/login.html", {"form": form})


class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = "users/edit_profile.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("users:detail", kwargs={"user_id": self.object.pk})


class UserChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserChangePasswordForm
    template_name = "users/change_password.html"

    def get_success_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


def logout_user(request):
    logout(request)
    return redirect("projects:project_list")
