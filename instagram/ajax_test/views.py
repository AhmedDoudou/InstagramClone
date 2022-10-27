from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Friend

def index(request):
    return render(request, "test.html")
    
def GetProfile(request):
    profiles = Friend.objects.all()
    return JsonResponse({"profiles":list(profiles.values())})

def Create(request):
    if request.method=="POST":
        nick_name = request.POST["nick_name"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        friend = Friend(nick_name=nick_name,first_name=first_name,last_name=last_name)
        friend.save()
        return HttpResponse("Data Added Successflly")