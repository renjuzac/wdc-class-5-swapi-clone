import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.models import Planet, People
from api.fixtures import SINGLE_PEOPLE_OBJECT, PEOPLE_OBJECTS
from api.serializers import serialize_people_as_json


def single_people(request):
    return JsonResponse(SINGLE_PEOPLE_OBJECT)


def list_people(request):
    return JsonResponse(PEOPLE_OBJECTS, safe=False)


@csrf_exempt
def people_list_view(request):
    """
    People `list` actions:

    Based on the request method, perform the following actions:

        * GET: Return the list of all `People` objects in the database.

        * POST: Create a new `People` object using the submitted JSON payload.

    Make sure you add at least these validations:

        * If the view receives another HTTP method out of the ones listed
          above, return a `400` response.

        * If submited payload is nos JSON valid, return a `400` response.
    """
    if request.method == 'GET':
        result = {}
        result["count"] = People.objects.count()
        result["results"] = []
        the_people = People.objects.values()
        for people in the_people:
            result["results"].append(people)
        
        return JsonResponse(result,safe=False)
    elif request.method == 'POST':
        text = (request.body.decode('utf-8'))
        try :
            data = json.loads(text)
            homeworld = Planet.objects.filter(name__icontains=data["homeworld"]).get()
            People.objects.create(name=data["name"],height=data["height"],
            mass = data["mass"],hair_color = data["hair_color"] ,homeworld =homeworld)
            return HttpResponse("Created user "+data["name"])
        except TypeError:
            return JsonResponse({'msg': 'Provide a valid JSON payload', 'success': False},status=400)
    else:
        return JsonResponse({'msg': 'Invalid HTTP method', 'success': False},status=400)


@csrf_exempt
def people_detail_view(request, people_id):
    """
    People `detail` actions:

    Based on the request method, perform the following actions:

        * GET: Returns the `People` object with given `people_id`.

        * PUT/PATCH: Updates the `People` object either partially (PATCH)
          or completely (PUT) using the submitted JSON payload.

        * DELETE: Deletes `People` object with given `people_id`.

    Make sure you add at least these validations:

        * If the view receives another HTTP method out of the ones listed
          above, return a `400` response.

        * If submited payload is nos JSON valid, return a `400` response.
    """
    if request.method == 'GET':
        result = People.objects.filter(id__exact=people_id).values()[0]
        return JsonResponse(result,safe=False)
    elif request.method == 'PUT' or request.method =='PATCH':
        try:
            text = request.body.decode('utf-8')
            data = json.loads(text)
            result = People.objects.filter(id__exact=people_id).get()
            for key,values in data.items():
                if key == "homeworld":
                    values = Planet.objects.filter(name__icontains=data["homeworld"]).get()
                    if not values:
                        return JsonResponse({'msg': 'Could not find planet with id: 9999', 'success': False},status=404)
                
                setattr(result,key,values)
            result.save()
            result = People.objects.filter(id__exact=people_id).values()[0]
            return JsonResponse(result, status=200)
        except TypeError:
            return HttpResponse("Exception Not valid JSON",status=400)
        except:
            return JsonResponse({'msg': 'Provided payload is not valid', 'success': False},status=400)
    elif request.method == "DELETE":
        result = People.objects.filter(id__exact=people_id).get()
        result.delete()
        return JsonResponse({'success': True},status=200)
    else:
        return JsonResponse({'msg': 'Invalid HTTP method', 'success': False},status=400)
        
    
