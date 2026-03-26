from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('info/', views.info, name='info'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('update-avatar/', views.update_avatar, name='update_avatar'),

    path('project/add/', views.add_project, name='add_project'),
    path('project/edit/<int:id>/', views.edit_project, name='edit_project'),
    path('project/delete/<int:id>/', views.delete_project, name='delete_project'),
    path('edit-home/', views.edit_home, name='edit_home'),
]
