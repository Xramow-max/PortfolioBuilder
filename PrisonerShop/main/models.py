from django.db import models
from django.contrib.auth.models import User

class Technology(models.Model):
    """Модель для збереження технологій (напр., Python, Django, React)."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва технології")

    class Meta:
        verbose_name = "Технологія"
        verbose_name_plural = "Технології"

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    """Модель портфоліо, яка прив'язана до конкретного користувача (1 до 1)."""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='portfolio', 
        verbose_name="Користувач"
    )
    bio = models.TextField(blank=True, null=True, verbose_name="Про себе / Біографія")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    class Meta:
        verbose_name = "Портфоліо"
        verbose_name_plural = "Портфоліо"

    def __str__(self):
        return f"Портфоліо користувача: {self.user.username}"


class Project(models.Model):
    """Модель проєкту, що містить опис, назву та стек технологій."""
    portfolio = models.ForeignKey(
        Portfolio, 
        on_delete=models.CASCADE, 
        related_name='projects', 
        verbose_name="Портфоліо"
    )
    title = models.CharField(max_length=200, verbose_name="Назва проекту")
    description = models.TextField(verbose_name="Опис проекту")
    technologies = models.ManyToManyField(
        Technology, 
        related_name='projects', 
        verbose_name="Стек технологій"
    )
    # Додаткові корисні поля для портфоліо (за бажанням)
    project_url = models.URLField(blank=True, null=True, verbose_name="Посилання на сайт")
    github_url = models.URLField(blank=True, null=True, verbose_name="Посилання на GitHub")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекти"
        ordering = ['-created_at']

    def __str__(self):
        return self.title