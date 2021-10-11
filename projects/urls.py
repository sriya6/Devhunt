from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('create/', views.createProject, name='create-project'),
    path('<str:pk>/', views.project, name='project'),
    path('<str:pk>/update', views.updateProject, name='update-project'),
    path('<str:pk>/delete', views.deleteProject, name='delete-project'),
]
