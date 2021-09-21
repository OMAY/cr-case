from django.urls import path, include
from apps.crm.views import UserDetailView, logout_view, UserUpdateView, HomeView, CompanyDetailView, CompanyUpdateView, \
    CompanyCreateView, ProjectDetailView, ProjectCreateView, ProjectUpdateView, ContactMessageDetailView, \
    ContactMessageCreateView, ContactMessageUpdateView, CompanyMessagesListView, ProjectMessagesListView, \
    CompanyProjectsListView, SearchResultsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search_results/', SearchResultsView.as_view(), name='search_results'),
    path('company_message_list/<int:pk>/', CompanyMessagesListView.as_view(), name='company_message_list'),
    path('project_message_list/<int:pk>/', ProjectMessagesListView.as_view(), name='project_message_list'),
    path('contact_message_create/', ContactMessageCreateView.as_view(), name='contact_message_create'),
    path('contact_message_detail/<int:pk>/', ContactMessageDetailView.as_view(), name='contact_message_detail'),

    path('contact_message_update/<int:pk>/', ContactMessageUpdateView.as_view(), name='contact_message_update'),
    path('project_create/', ProjectCreateView.as_view(), name='project_create'),
    path('project_detail/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('project_update/<int:pk>/', ProjectUpdateView.as_view(), name='project_update'),
    path('company_create/', CompanyCreateView.as_view(), name='company_create'),
    path('company_detail/<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
    path('company_update/<int:pk>/', CompanyUpdateView.as_view(), name='company_update'),
    path('company_project_list/<int:pk>/', CompanyProjectsListView.as_view(), name='company_project_list'),
    path('user_update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user_detail/', UserDetailView.as_view(), name='user_detail'),


    # path('accounts/profile/', home, name=''),

]
