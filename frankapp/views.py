import json
from django.shortcuts import render
from django.http import HttpResponse
from frankapp.models import *

# Create your views here.
def index(request):
    return render(request, 'frankapp/index.html')

def searchpeople(request):
    android = False
    
    if 'android' in request.GET:
        if 'true' in request.GET['android']:
            android = True;
            
    if 'types' in request.GET:
        types = request.GET['types']
        name = request.GET.get('name')
        if 'actor' in types:
            results = ActorsRoles.objects.filter(actor__name=name)
        else if 'crew' in types:
            results = CrewResponsibilities.objects.filter(crew__name=name)
        else if 'role' in types:
            results = ActorsRoles.objects.filter(role__name=name)
            
        for result in results:
            print result.actor.name + ": " + result.role.name

    if android == False:
        return render(request, 'frankapp/people.html', {'results': results})
    else:
        print "should return json"
        return HttpResponse(json.dumps(resultsToDict(results)), content_type="application/json")
    
def searchevents(request):
    results_list = []
    if 'types' in request.GET:
        types = request.GET['types']
        if 'actor' in types:
            actor = types['actor']
        if 'crew' in types:
            crew = types['crew']
        if 'role' in types:
            role = types['role']
    return render(request, 'frankapp/events.html', {'results_list': results})

def resultsToDict(results):
    response_data = {}
    i = 1
    for result in results:
        if (result.actor.name not in response_data):
            response_data[result.actor.name] = result.role.name
        else:
            response_data[result.actor.name + '_' + str(i)] = result.role.name
            i = i + 1
    return response_data
