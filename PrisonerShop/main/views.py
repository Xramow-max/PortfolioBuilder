from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth import login

from .models import Portfolio, Project, Technology
from .forms import RegisterForm, PortfolioForm, ProjectForm, TechnologyForm

from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

from django.http import HttpResponse


def home(request):
    # Отримуємо пошуковий запит з URL (наприклад, ?q=admin)
    query = request.GET.get('q', '').strip()
    
    # Початковий запит для всіх портфоліо
    portfolios = Portfolio.objects.select_related('user').all()
    
    # Якщо користувач щось ввів у пошук, фільтруємо за іменем користувача
    if query:
        portfolios = portfolios.filter(user__username__icontains=query)
        
    context = {
        'portfolios': portfolios,
        'query': query,  # Повертаємо запит назад у шаблон, щоб показати його в інпуті
    }
    return render(request, 'main/main.html', context)

class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = "portfolio:register"



class RegisterView(CreateView):
    template_name = "accounts/register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()

        Portfolio.objects.create(
            user=user
        )

        login(self.request, user)

        return redirect('portfolio:home')



class ProfileView(LoginRequiredMixin, DetailView):
    """Профіль поточного користувача (з можливістю редагування)."""
    model = Portfolio
    template_name = 'accounts/profile.html'
    context_object_name = 'portfolio'

    def get_object(self):
        return self.request.user.portfolio


class PublicProfileView(DetailView):
    """Публічний перегляд профілю будь-якого користувача за username."""
    model = Portfolio
    template_name = 'accounts/profile.html'
    context_object_name = 'portfolio'

    def get_object(self):
        return get_object_or_404(Portfolio, user__username=self.kwargs['username'])


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Дозволяє користувачу заповнити/відредагувати свій профіль (біо, аватар)."""
    model = Portfolio
    form_class = PortfolioForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('portfolio:profile')

    def get_object(self):
        return self.request.user.portfolio


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """Додавання нового проєкту до власного портфоліо."""
    model = Project
    form_class = ProjectForm
    template_name = 'accounts/project_form.html'
    success_url = reverse_lazy('portfolio:profile')

    def form_valid(self, form):
        form.instance.portfolio = self.request.user.portfolio
        return super().form_valid(form)
    
class TechnologyCreateView(LoginRequiredMixin, CreateView):
    """Додавання нової технології до загальної бази."""
    model = Technology
    form_class = TechnologyForm
    template_name = 'accounts/technology_form.html'
    
    # Після створення технології повертаємо користувача до сторінки створення проєкту
    success_url = reverse_lazy('portfolio:project_add')


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """Видалення проєкту. Дозволено тільки власнику."""
    model = Project
    template_name = 'accounts/project_confirm_delete.html'
    success_url = reverse_lazy('portfolio:profile')

    def get_queryset(self):
        # Обмежуємо queryset так, щоб користувач міг видаляти лише свої проєкти
        return Project.objects.filter(portfolio__user=self.request.user)