from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, JsonResponse, HttpResponse, request
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from apps.crm.forms import MyUserModelForm, UserLoginForm
from apps.crm.mixins import StaffAndLoginRequiredMixin
from apps.crm.models import MyUser


def home(request):
    return render(request, "home.html")


class UserDetailView(StaffAndLoginRequiredMixin, DetailView):
    queryset = MyUser.objects.all()
    template_name = 'user_detail.html'

    def get_object(self):
        return self.request.user


class UserUpdateView(StaffAndLoginRequiredMixin, UpdateView):
    model = MyUser
    template_name = "user_update.html"
    form_class = MyUserModelForm
    success_url = reverse_lazy('crm:user_detail')


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('crm:home')
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')

