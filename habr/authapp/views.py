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

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = 'Профиль'
        content['user_check'] = User.objects.get(username=self.request.user)
        if content['user_check'].id == self.get_object().id:
            content['edit_visible'] = 'True'
        else:
            content['edit_visible'] = 'False'
        return content


class UserCreateView(CreateView):
    model = User
    template_name = 'authapp/users-create.html'
    form_class = UserRegisterForm

    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['title'] = 'Регистрация'
        next = ''
        if self.request.GET:
            next = self.request.GET['next']
        if next != '':
            content['next'] = next
        return content

    def get_success_url(self):
        next_url = self.request.GET['next']
        if next_url:
            return next_url
        return reverse_lazy('main:articles')


class UserUpdateView(UpdateView):
    model = User
    template_name = 'authapp/users-update-delete.html'
    form_class = UserProfileForm

    def get_context_data(self, **kwargs):
        content = super(UserUpdateView, self).get_context_data(**kwargs)
        content['title'] = 'Редактирование пользователя'
        content['user'] = User.objects.get(username = self.request.user)
        return content

    def get_object(self, queryset=None):
        return User.objects.get(username=self.request.user)

    def get_success_url(self):
        profile_id = User.objects.get(username = self.request.user).id
        return reverse_lazy('auth:users_detail', kwargs={'pk': profile_id})


class UserDeleteView(DeleteView):
    model = User
    template_name = 'authapp/users-update-delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = 0
        self.object.save()
        return HttpResponseRedirect(reverse('auth:login'))

    def get_object(self, queryset=None):
        return User.objects.get(username=self.request.user)


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