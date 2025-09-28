
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Property
from django.http import JsonResponse
from .utils import get_redis_cache_metrics
from .utils import get_all_properties

@cache_page(60 * 15)  # Cache response for 15 minutes (900 seconds)
def property_list(request):
    properties = Property.objects.all()
    return render(request, "properties/property_list.html", {"properties": properties})


def property_list(request):
    properties = get_all_properties()
    return render(request, "properties/property_list.html", {"properties": properties})

def cache_metrics(request):
    metrics = get_redis_cache_metrics()
    return JsonResponse(metrics)
