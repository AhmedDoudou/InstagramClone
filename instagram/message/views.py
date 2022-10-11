from django.shortcuts import render

def NewMessage(request):
    return render(request,"chat.html")