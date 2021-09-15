
from django.urls import path
from apps.crm.views import home, UserDetailView, logout_view, UserUpdateView

urlpatterns = [

    path('user_update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user_detail/', UserDetailView.as_view(), name='user_detail'),

    path('', home, name='home'),
    # path('accounts/profile/', home, name=''),


]


