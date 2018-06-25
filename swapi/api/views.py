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
        result = []
        the_people = People.objects.values()

        for people in the_people:
            people['homeworld'] = 'http://localhost:8000/planets/{}/'.format(people['homeworld_id'])
            del people['id']
            del people['homeworld_id']
            result.append(people)
        
        return JsonResponse(result,safe=False)
    elif request.method == 'POST':
        text = (request.body.decode('utf-8'))
        try :
            try:
                data = json.loads(text)
            except ValueError:
                return JsonResponse({'msg': 'Provide a valid JSON payload', 'success': False},status=400)
            if not isinstance(data['height'],int):
                raise ValueError
            homeworldset = Planet.objects.filter(id__exact=data["homeworld"])
            if homeworldset:
                homeworld = Planet.objects.filter(id__exact=data["homeworld"]).get()
            else :
                return JsonResponse({"success": False,"msg": "Could not find planet with id: 9999"},status = 404)

            People.objects.create(name=data["name"],height=data["height"],
            mass = data["mass"],hair_color = data["hair_color"] ,homeworld =homeworld)
            user  = People.objects.filter(name__exact=data["name"]).get()
            result = data
            result['homeworld'] = 'http://localhost:8000/planets/{}/'.format(data['homeworld'])
            result['created'] = user.created
            return JsonResponse(result,status=201)
        except ValueError:
            return JsonResponse({'msg': 'Provided payload is not valid', 'success': False},status=400)
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
        result['homeworld'] = 'http://localhost:8000/planets/{}/'.format(result['homeworld_id'])
        del result['id']
        del result['homeworld_id']
        return JsonResponse(result,safe=False)
    elif request.method == 'PUT' :
        try:
            text = request.body.decode('utf-8')
            data = json.loads(text)

            expected_keys = ["name","height","mass","homeworld","hair_color"]
            for key in expected_keys:
                if key not in data.keys():
                    return JsonResponse({'msg': 'Missing field in full update', 'success': False}, status=400)

            if not isinstance(data['height'],int):
                raise ValueError
            result = People.objects.filter(id__exact=people_id).get()
            for key,values in data.items():
                if key == "homeworld":
                    try:
                        values = Planet.objects.filter(id__exact=data["homeworld"]).get()
                    except:
                        message = 'Could not find planet with id: {}'.format(data["homeworld"])
                        return JsonResponse({'msg': message, 'success': False},status=404)
                setattr(result,key,values)
            result.save()
            result = People.objects.filter(id__exact=people_id).values()[0]
            return JsonResponse(result, status=200)
        except ValueError:
            return JsonResponse({'msg': 'Provided payload is not valid', 'success': False},status=400)
    elif request.method =='PATCH':

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
        
    
