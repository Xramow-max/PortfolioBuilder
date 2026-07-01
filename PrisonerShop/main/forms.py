from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# --- Додайте цей код у ваш існуючий forms.py ---
from .models import Portfolio, Project, Technology


# --- Додайте цей код у ваш існуючий forms.py ---

from django import forms
from .models import Portfolio, Project, Technology


class PortfolioForm(forms.ModelForm):
    """Форма для заповнення/редагування профілю користувача."""

    class Meta:
        model = Portfolio
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Розкажіть про себе, свій досвід, цілі...',
                'class': 'form-control',
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'bio': 'Про себе',
            'avatar': 'Аватар',
        }


class ProjectForm(forms.ModelForm):
    """Форма для додавання проєкту в портфоліо."""

    technologies = forms.ModelMultipleChoiceField(
        queryset=Technology.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Технології',
    )

    class Meta:
        model = Project
        fields = ['title', 'description', 'technologies', 'project_url', 'github_url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Назва проєкту',
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control',
                'placeholder': 'Опис проєкту...',
            }),
            'project_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com',
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username/repo',
            }),
        }
        labels = {
            'title': 'Назва проєкту',
            'description': 'Опис',
            'project_url': 'Посилання на сайт',
            'github_url': 'Посилання на GitHub',
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Введіть пароль'
            }
        ),
        help_text=""
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Повторіть пароль'
            }
        ),
        help_text=""
    )

    class Meta(UserCreationForm.Meta):
        model = User

        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )

class TechnologyForm(forms.ModelForm):
    """Форма для створення нової технології."""
    class Meta:
        model = Technology
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Назва технології (напр., Docker)',
            }),
        }
        labels = {
            'name': 'Назва технології',
        }