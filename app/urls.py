from django.urls import path
from app.views import (user_dashboard,
                       user_login, user_signup, reset_password, user_create,
                       user_logout, user_admin, user_profile, user_update, change_password,
                       user_delete, user_activate)
from django.contrib.auth import views as auth_views

app_name = "app"
urlpatterns = [
    path('sign-up/', user_signup, name="signup"),
    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('admin-page/', user_admin, name="user_admin"),
    path('', user_dashboard, name="dashboard"),
    path('profile/', user_profile, name="profile"),
    path('change-password/', change_password, name="change_password"),
    path('update/<int:pk>/', user_update, name="user_update"),
    path('create/', user_create, name="user_create"),
    path('delete/<int:pk>/', user_delete, name="user_delete"),
    path('activate-reactivate/<int:pk>/', user_activate, name="user_activate"),
    path('password-reset/', reset_password, name="reset_password"),
    path("password-reset/done/",
         auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done",
         ),
]
