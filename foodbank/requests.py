from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from . import models
from . import AUTH

import csv
import json
from datetime import datetime

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
@csrf_exempt
def import_requests(req, **params):
    reader = csv.reader(req)
    first_line = True
    categories = []
    with csv.reader(req.body) as reader:
        for row in reader:
            if first_line:
                first_line = False
                for category_name in row[2:]:
                    category_o = models.Category.objects.filter(
                        name=category_name).first()
                    if category_o is None:
                        category_o = models.Category()
                        category_o.name = category_name
                        category.save()
                        categories.append(category)
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
def post_request(req, **param):
    r = models.Request()
    data = json.loads(req.body.decode('utf-8'))['result']['parameters']
    beneficiary = data['BeneficiaryName']
    category = data['FoodCategory']
    quantity = data['number']
    category_o = models.Category.objects.filter(name=category).first()
    if category_o is None:
        category_o = models.Category()
        category_o.name = category
        category_o.save()
    r.category = category_o
    beneficiary_o = models.Beneficiary.objects.filter(
        name__contains=beneficiary).first()
    if beneficiary_o is None:
        beneficiary_o = models.Beneficiary()
        beneficiary_o.name = beneficiary
        beneficiary_o.save()
    r.beneficiary = beneficiary_o
    r.quantity = quantity
    r.time = datetime.now()
    r.save()
    return JsonResponse({
        'status' : 'success'
    }, safe=False)

@csrf_exempt
def show_beneficiary_requests(req, **params):
    response = HttpResponse(content_type='text/csv')
    categories = []
    for category in models.Category.objects.all():
        categories.append(category.name)

    writer = csv.writer(response)
    writer.writerow([
        'Date Time',
        'Beneficiary'
    ] + categories)
    for beneficiary in models.Beneficiary.objects.all():
        b_data = dict()
        time = ''
        for request in beneficiary.request_set.all():
            if time < str(request.time):
                time = str(request.time)
            if request.category.name in b_data:
                b_data[request.category.name] += request.quantity
            else:
                b_data[request.category.name] = request.quantity
        writer.writerow(
            [ time, beneficiary.name ] +
            [
                b_data[category_name] if category_name in b_data else 0
                for category_name in categories
            ])
    return response
