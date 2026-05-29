from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.urls import reverse
from .models import Project
from .forms import ProjectForm


class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    paginate_by = 12
    ordering = ["-created_at"]


class ProjectDetailsView(DetailView):
    model = Project
    template_name = "projects/project-details.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        context["participants"] = project.participants.all()
        context["user"] = self.request.user
        context["request"] = self.request
        context["is_participant"] = (
            self.request.user in project.participants.all()
        )
        return context


class CreateProjectView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = "projects/create-project.html"
    form_class = ProjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = False
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        self.object.participants.add(self.request.user)
        return response

    def get_success_url(self):
        return reverse("projects:detail", kwargs={"pk": self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/create-project.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        return context

    def get_success_url(self):
        return reverse("projects:detail", kwargs={"pk": self.object.pk})


class FavoriteProjectsView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/favorite-projects.html"
    paginate_by = 12

    def get_queryset(self):
        return self.request.user.favorites.all().order_by("-created_at")


@login_required
@require_http_methods(["POST"])
def toggle_favorite(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project in request.user.favorites.all():
        request.user.favorites.remove(project)
        favorited = False
    else:
        request.user.favorites.add(project)
        favorited = True
    return JsonResponse({"status": "ok", "favorited": favorited})


@login_required
@require_http_methods(["POST"])
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user = request.user
    is_participant = project.participants.filter(id=user.id).exists()
    if is_participant:
        project.participants.remove(user)
        joined = False
    else:
        project.participants.add(user)
        joined = True
    return JsonResponse(
        {
            "status": "ok",
            "joined": joined,
            "participants_count": project.participants.count(),
        }
    )


@login_required
@require_http_methods(["POST"])
def complete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.owner != request.user and not request.user.is_staff:
        return JsonResponse(
            {"status": "error", "message": "Нет прав"},
            status=403)
    if project.status == "open":
        project.status = "closed"
        project.save()
        return JsonResponse({"status": "ok", "project_status": "closed"})
    return JsonResponse(
        {"status": "error", "message": "Проект уже закрыт"},
        status=400)
