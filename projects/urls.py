from django.urls import path
from .views import (ProjectListView, 
                    ProjectDetailsView, 
                    toggle_favorite, 
                    FavoriteProjectsView, 
                    complete_project, 
                    toggle_participate, 
                    CreateProjectView, 
                    ProjectUpdateView)

app_name = 'projects'

urlpatterns = [
    path('list/', ProjectListView.as_view(), name="project_list"),
    path('<int:pk>/toggle-favorite/', toggle_favorite, name='toggle_favorite'),
    path('favorites/', FavoriteProjectsView.as_view(), name='favorite_projects'),
    path('<int:pk>/complete/', complete_project, name='complete_project'),
    path('<int:pk>/toggle-participate/', toggle_participate, name='toggle_participate'),
    path('create-project/', CreateProjectView.as_view(), name='create_project'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='edit_project'),
    path('<int:pk>/', ProjectDetailsView.as_view(), name='project_details')
]