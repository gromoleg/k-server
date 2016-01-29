from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from response.templates import invalid_data
from .models import Faculty, Group


@csrf_exempt
def faculties(request):
    return Faculty.get_all()


@csrf_exempt
def groups(request):
    faculty = request.GET.get('faculty', None)
    if faculty is None:
        raise Http404
    try:
        faculty = int(faculty)
    except:
        return invalid_data
    return Group.get_groups_by_faculty(faculty)
