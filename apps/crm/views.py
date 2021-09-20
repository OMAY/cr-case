from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, ListView, CreateView
from django.db.models import Q
from apps.crm.forms import MyUserModelForm, UserLoginForm, CompanyModelForm, ProjectModelForm, \
    ContactMessageModelForm
from apps.crm.mixins import StaffAndLoginRequiredMixin, RedirectToPreviousMixin
from apps.crm.models import MyUser, Company, Project, ContactMessage


class ContactMessageDetailView(StaffAndLoginRequiredMixin, RedirectToPreviousMixin, DetailView):
    model = ContactMessage
    template_name = 'contact_message_detail.html'
    context_object_name = 'contact_message'


class ContactMessageCreateView(StaffAndLoginRequiredMixin, RedirectToPreviousMixin, CreateView):
    model = ContactMessage
    template_name = 'contact_message_create.html'
    form_class = ContactMessageModelForm

    def form_valid(self, form):
        form.instance.manager = self.request.user
        form.instance.company = form.instance.project.company
        return super().form_valid(form)


class ContactMessageUpdateView(StaffAndLoginRequiredMixin, RedirectToPreviousMixin, UpdateView):
    model = ContactMessage
    template_name = 'contact_message_update.html'
    form_class = ContactMessageModelForm


class ProjectDetailView(DetailView, ListView):
    paginate_by = 5
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'
    object_list = ContactMessage.objects.all()


class ProjectMessagesListView(StaffAndLoginRequiredMixin, ListView):
    paginate_by = 5
    template_name = 'project_message_list.html'

    def get_queryset(self):
        return ContactMessage.objects.filter(project=self.kwargs['pk'])


class ProjectCreateView(StaffAndLoginRequiredMixin, RedirectToPreviousMixin, CreateView):
    model = Project
    template_name = 'project_create.html'
    form_class = ProjectModelForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(StaffAndLoginRequiredMixin, RedirectToPreviousMixin, UpdateView):
    model = Project
    template_name = 'project_update.html'
    form_class = ProjectModelForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class CompanyDetailView(DetailView, ListView):
    paginate_by = 5
    model = Company
    template_name = 'company_detail.html'
    context_object_name = 'company'
    object_list = Project.objects.all()


class CompanyMessagesListView(StaffAndLoginRequiredMixin, ListView):
    paginate_by = 5
    template_name = 'company_message_list.html'

    def get_queryset(self):
        context = ContactMessage.objects.filter(company=self.kwargs['pk'])
        return context


class CompanyProjectsListView(ListView):
    paginate_by = 5
    template_name = 'company_project_list.html'

    def get_queryset(self):
        context = Project.objects.filter(company=self.kwargs['pk'])
        return context


class CompanyCreateView(StaffAndLoginRequiredMixin, RedirectToPreviousMixin, CreateView):
    model = Company
    template_name = 'company_create.html'
    form_class = CompanyModelForm

    # success_url = reverse_lazy('crm:user_detail')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CompanyUpdateView(StaffAndLoginRequiredMixin, RedirectToPreviousMixin, UpdateView):
    model = Company
    template_name = 'company_update.html'
    form_class = CompanyModelForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


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


class HomeView(ListView):
    paginate_by = 5
    model = Company
    template_name = 'home.html'
    queryset = Company.objects.all()

    def get_ordering(self):
        ordering = self.request.GET.get('orderby')
        return ordering


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


class SearchResultsView(ListView):
    model = ContactMessage
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = ContactMessage.objects.filter(Q(type_of_message=query))
        return object_list
