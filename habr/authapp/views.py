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
    success_url = reverse_lazy('auth:users_detail')

    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'authapp/users-update-delete.html'
    form_class = UserProfileForm

    def get_context_data(self, **kwargs):
        content = super(UserUpdateView, self).get_context_data(**kwargs)
        content['title'] = 'Редактирование пользователя'
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

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return redirect(get_redirect_url())
    else:
        form = UserLoginForm()
    content = {'title': title, 'form': form}
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
