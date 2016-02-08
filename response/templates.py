from django.http import JsonResponse
from django.http import HttpResponse


def error_response(error, result):
    return JsonResponse({"status": 0, "result": result, "error": error})


def ok_response(result):
    return JsonResponse({"status": 1, "result": result, "error": 0})


def response(result, error=0):
    return JsonResponse({"status": bool(error), "result": result, "error": error})

status_ok = ok_response([])
invalid_data = error_response(51, result=[])
