from django.urls import path

from users.views import (UserChangePasswordView, UserDetailView, UserEditView,
                         UsersListView, login_user, logout_user, register_user)

app_name = "users"

urlpatterns = [
    path("list/", UsersListView.as_view(), name="list"),
    path("<int:pk>/", UserDetailView.as_view(), name="detail"),
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("edit-profile/", UserEditView.as_view(), name="edit_profile"),
    path("change-password/", UserChangePasswordView.as_view(),
         name="change_password"),
    path("logout/", logout_user, name="logout"),
]
