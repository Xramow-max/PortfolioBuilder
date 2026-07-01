from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/<str:username>/', views.PublicProfileView.as_view(), name='public_profile'),

    path('projects/add/', views.ProjectCreateView.as_view(), name='project_add'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'), # Новий шлях
    
    path('technologies/add/', views.TechnologyCreateView.as_view(), name='technology_add'), # Новий шлях
]