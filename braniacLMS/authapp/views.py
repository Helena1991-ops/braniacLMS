from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView, UpdateView
from authapp.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser
from authapp.forms import CustomUserCreationForm, CustomUserChangeForm

class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'
    extra_context = {
        'title': 'Вход пользователя'
    }


class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('mainapp:index')
    template_name = 'authapp/register.html'


# class RegisterView(TemplateView):
#     template_name = 'authapp/register.html'
#     extra_context = {
#         'title': 'Регистрация пользователя'
#     }
#
#     def post(self, request, *args, **kwargs):
#         try:
#             print(type(request.POST))
#             if all(
#                     (
#                         request.POST.get('username'),
#                         request.POST.get('email'),
#                         request.POST.get('first_name'),
#                         request.POST.get('last_name'),
#                         request.POST.get('password1'),
#                         request.POST.get('password2'),
#                         request.POST.get('password1') == request.POST.get('password2'),
#
#                     )
#             ):
#                 new_user=models.User.objects.create(
#                     username=request.POST.get('username'),
#                     first_name=request.POST.get('first_name'),
#                     last_name=request.POST.get('last_name'),
#                     email=request.POST.get('email'),
#                     age=request.POST.get('age') if request.POST.get('age') else 0,
#                     avatar=request.FILES.get('avatar'),
#                 )
#                 new_user.set_password(request.POST.get('password1'))
#                 new_user.save()
#                 messages.add_message(request, messages.INFO, 'Регистрация прошла успешно')
#                 return HttpResponseRedirect(reverse('authapp:login'))
#
#             else:
#                 messages.add_message(request, messages.WARNING, 'Что-то пошло не так :(')
#                 return HttpResponseRedirect(reverse('authapp:register'))
#
#         except Exception as exp:
#             messages.add_message(request, messages.WARNING, mark_safe(f"Что-то пошло не так :( {exp}"))
#             return HttpResponseRedirect(reverse('authapp:register'))



class CustomLogoutView(LogoutView):
    pass


class EditView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'authapp/edit.html'


    def get_object(self, queryset=None):
        return self.request.user


    def get_success_url(self):
        return reverse_lazy('authapp:edit')


# class EditView(TemplateView):
#     template_name = 'authapp/edit.html'
#
#     extra_context = {
#         'title': 'Редактирование пользователя'
#     }
#
#     def post(self, request, *args, **kwargs):
#
#         if request.POST.get('username'):
#             request.user.username = request.POST.get('username')
#
#         if request.POST.get('first_name'):
#             request.user.first_name = request.POST.get('first_name')
#
#         if request.POST.get('last_name'):
#             request.user.last_name = request.POST.get('last_name')
#
#         if request.POST.get('age'):
#             request.user.age = request.POST.get('age')
#
#         if request.POST.get('email'):
#             request.user.email = request.POST.get('email')
#
#         request.user.save()
#         return HttpResponseRedirect(reverse('authapp:edit'))