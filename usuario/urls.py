from django.urls import path,include
from . import views
from django.urls import path
from usuario.views import login, cadastro, logout
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="usuario/reset_password.html"),
        name='reset_password'
    ),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="usuario/reset_password.html"),
        name='reset_password'
    ),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="usuario/reset_password_sent.html"),
        name='password_reset_done'
    ),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="usuario/reset.html"),
        name='password_reset_confirm'
    ),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="usuario/reset_password_complete.html"),
        name='password_reset_complete'
    ),

]

