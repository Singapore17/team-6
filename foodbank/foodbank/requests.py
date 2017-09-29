from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from . import models
from . import AUTH

import csv

def basic_auth(func):
    @wraps(func)
    def _decorator(request, *args, **kwargs):
        from django.contrib.auth import authenticate, login
        if request.META.has_key('HTTP_AUTHORIZATION'):
            method, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            if method.lower() == 'basic':
                auth = auth.strip.decode('base64')
                username, password = auth.split(':')
                if username == AUTH.username and password == AUTH.password:
                    return func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden('<h1>Forbidden</h1>')
        res = HttpResponse()
        res.status_code = 401
        res['WWW-Authenticate'] = 'Basic'
        return res

    return _decorator


# suppose request body is csv
def import_requests(req, **params):
    first_line = True
    with csv.reader(req.body) as reader:
        for row in reader:
            if first_line:
                first_line = False
                continue
            r = models.Request()
            beneficiary = models.Beneficiary.objects.filter(
                name__contains=row[0]).first()
            if beneficiary is None:
                beneficiary = models.Beneficiary()
                beneficiary.name = row[0]
                beneficiary.save()
            r.beneficiary = name
            r.quantity = row[0]


@csrf_exempt
@basic_auth
def post_request(req, **param):
    r = models.Request()


