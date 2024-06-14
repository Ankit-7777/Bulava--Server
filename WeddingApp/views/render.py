from django.shortcuts import render

def index(request):
    return render(request, 'dashboard/index.html')

def birthday(request):
    return render(request, 'events/event_card_birthday.html')

def inaugrations(request):
    return render(request, 'events/event_card_inauguration.html')

def wedding(request):
    return render(request, 'events/event_card_wedding.html')

def custom(request):
    return render(request, 'events/event_card_custom.html')