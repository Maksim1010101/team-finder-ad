from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.constants import PAGE_SIZE
from projects.forms import ProjectForm
from projects.models import Project


class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    paginate_by = PAGE_SIZE
    ordering = ["-created_at"]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("owner")
            .prefetch_related("participants")
        )


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
        context["is_participant"] = project.participants.filter(
            pk=self.request.user.pk
        ).exists()
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
    paginate_by = PAGE_SIZE

    def get_queryset(self):
        return (
            self.request.user.favorites.all()
            .select_related("owner")
            .prefetch_related("participants")
            .annotate(participants_count=Count("participants"))
            .order_by("-created_at")
        )


@login_required
@require_http_methods(["POST"])
def toggle_favorite(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if is_favorite := request.user.favorites.filter(pk=pk).exists():
        request.user.favorites.remove(project)
    else:
        request.user.favorites.add(project)
    return JsonResponse({"status": "ok", "favorited": not is_favorite})


@login_required
@require_http_methods(["POST"])
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if is_participant := project.participants.filter(pk=request.user.pk).exists():
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)
    return JsonResponse({"status": "ok", "joined": not is_participant})


@login_required
@require_http_methods(["POST"])
def complete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.owner != request.user and not request.user.is_staff:
        return JsonResponse(
            {"status": "error", "message": "Нет прав"}, status=HTTPStatus.FORBIDDEN
        )
    if project.status == Project.OPEN:
        project.status = Project.CLOSED
        project.save()
        return JsonResponse({"status": "ok", "project_status": Project.CLOSED})
    return JsonResponse(
        {"status": "error", "message": "Проект уже закрыт"},
        status=HTTPStatus.BAD_REQUEST,
    )
