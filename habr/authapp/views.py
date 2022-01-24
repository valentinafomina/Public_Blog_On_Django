from django.contrib import auth
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from authapp.models import User
from authapp.forms import UserRegisterForm, UserProfileForm, UserLoginForm


# CRUD - Create Read Update Delete
class UserListView(ListView):
    model = User
    template_name = 'adthapp/admin-users-read.html'

    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    model = User
    template_name = 'authapp/admin-users-create.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('admin_staff:admin_users_read')

    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'authapp/admin-users-update-delete.html'
    success_url = reverse_lazy('admin_users_read')
    form_class = UserProfileForm

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Редактирование пользователя'
        return context


class UserDeleteView(DeleteView):
    model = User
    template_name = 'authapp/admin-users-update-delete.html'
    success_url = reverse_lazy('admin_users_read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'title': 'GeekShop - Авторизация', 'form': form}
    return render(request, 'authapp/login.html', context)
