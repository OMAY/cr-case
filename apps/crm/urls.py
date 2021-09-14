from django.urls import path
from apps.crm.views import home_page

urlpatterns = [
    path('', home_page)

]