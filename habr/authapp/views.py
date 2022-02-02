from pyexpat import model
from django.contrib import auth
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import User
from .forms import UserRegisterForm, UserProfileForm, UserLoginForm


# CRUD - Create Read Update Delete
class UserDetailView(DetailView):
    model = User
    template_name = 'authapp/users-detail.html'

    def dispatch(self, request, *args, **kwargs):
        return super(UserDetailView, self).dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    model = User
    template_name = 'authapp/users-create.html'
    form_class = UserRegisterForm

    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        next = ''
        if self.request.GET:
            next = self.request.GET['next']
        if next != '':
            context['next'] = next
        return context

    def get_success_url(self):
        next_url = self.request.GET['next']
        if next_url:
            return next_url
        return reverse_lazy('main:articles')


class UserUpdateView(UpdateView):
    model = User
    template_name = 'authapp/users-update-delete.html'
    form_class = UserProfileForm
    success_url = '/auth/profile/2/'

    def get_context_data(self, **kwargs):
        content = super(UserUpdateView, self).get_context_data(**kwargs)
        content['title'] = 'Редактирование пользователя'
        content['user'] = User.objects.get(username = self.request.user)
        return content


class UserDeleteView(DeleteView):
    model = User
    template_name = 'authapp/users-update-delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(reverse('auth:login'))


def login(request):
    title = 'Вход'
    next = ''

    if request.GET:
        next = request.GET['next']

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                print(request)
                print(next)
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse('main:articles'))
    else:
        form = UserLoginForm()
    content = {'title': title, 'form': form}
    if next != '':
        content['next'] = next
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('auth:login'))
