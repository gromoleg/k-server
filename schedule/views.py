from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from response.templates import invalid_data
from .models import Faculty, Group, Class
from json import loads


@csrf_exempt
def faculties(request):
    return Faculty.get_all()


@csrf_exempt
def groups(request):
    faculty = request.GET.get('faculty', None)
    if faculty is None:
        raise Http404
    try:
        faculty = Faculty.objects.get(id=int(faculty))
    except:
        return invalid_data
    return faculty.get_groups()


@csrf_exempt
def group(request, group_id):
    try:
        _group = Group.objects.get(id=int(group_id))
    except:
        return invalid_data

    if request.method == 'GET':
        return _group.get_schedule()

    elif request.method == 'POST':
        try:
            data = loads(request.POST.get('data', None))
        except:
            return invalid_data
        return _group.update_schedule(data)



@csrf_exempt
def group_class(request, group_id, class_id):
    try:
        _class = Class.objects.get(id=int(class_id), group_id=int(group_id))
    except:
        return invalid_data
    try:
        data = loads(request.POST['data'])
    except:
        return invalid_data
    return _class.modify(data)
