from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from .models import Faculty


@csrf_exempt
def faculties(request):
    return Faculty.get_all()