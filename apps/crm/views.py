from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, HttpResponse


def home_page(request):
    # return HttpResponse("Hello-Hellllloooowwww!")
    return render(request, "home.html")
