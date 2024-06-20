# views.py

from django.shortcuts import render
from django.http import JsonResponse
from WeddingApp.models import BannerImage
import random

def index(request):
    return render(request, 'dashboard/index.html')

def get_random_banner_image(request):
    try:
        random_banner = BannerImage.objects.order_by('?').first()
        if random_banner:
            return JsonResponse({'image_url': random_banner.image.url})
        else:
            return JsonResponse({'image_url': '/static/images/event-07.jpg'})
    except Exception as e:
        return JsonResponse({'error': str(e)})


def birthday(request):
    return render(request, 'events/event_card_birthday.html')

def inaugrations(request):
    return render(request, 'events/event_card_inauguration.html')

def wedding(request):
    return render(request, 'events/event_card_wedding.html')

def custom(request):
    return render(request, 'events/event_card_custom.html')