import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def text_response(request):
    """
    Return a HttpResponse with a simple text message.
    Check that the default content type of the response must be "text/html".
    """
    return HttpResponse("Hello World")



def looks_like_json_response(request):
    """
    Return a HttpResponse with a text message containing something that looks
    like a JSON document, but it's just "text/html".
    
    """
    return HttpResponse('{"apple":"pie"}')
    pass


def simple_json_response(request):
    """
    Return an actual JSON response by setting the `content_type` of the HttpResponse
    object manually.
    """
    return HttpResponse('{"apple":"pie"}',content_type="application/json")
    pass


def json_response(request):
    """
    Return the same JSON document, but now using a JsonResponse instead.
    """
    return JsonResponse({"apple":"pie"},safe=False)


def json_list_response(request):
    """
    Return a JsonReponse that contains a list of JSON documents
    instead of a single one.
    Note that you will need to pass an extra `safe=False` parameter to
    the JsonResponse object it order to avoid built-in validation.
    https://docs.djangoproject.com/en/2.0/ref/request-response/#jsonresponse-objects
    """
    return JsonResponse([{"apple":"pie"},{"peach":"cobbler"}],safe=False)

    
    pass


def json_error_response(request):
    """
    Return a JsonResponse with an error message and 400 (Bad Request) status code.
    """
    response =  JsonResponse({"message": "this is an error"},safe=False)
    response.status_code = 400
    return response
    pass


@csrf_exempt
def only_post_request(request):
    """
    Perform a request method check. If it's a POST request, return a message saying
    everything is OK, and the status code `200`. If it's a different request
    method, return a `400` response with an error message.
    """
    if request.method == 'POST':
        return JsonResponse({"message":"OK"})
    else:
        response = JsonResponse({"message":"ERROR"})
        response.status_code = 400
        return response



@csrf_exempt
def post_payload(request):
    """
    Write a view that only accepts POST requests, and processes the JSON
    payload available in `request.body` attribute.
    """
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        keys = data.keys()
        keyvalues = ""
        for key in keys :
            keyvalues += key
        return HttpResponse(keyvalues)
        
    else:
        response = JsonResponse({"message":"ERROR"})
        response.status_code = 400
        return response          


def custom_headers(request):
    """
    Return a JsonResponse and add a custom header to it.
    """
    response = JsonResponse({"hello":"world"})
    response['myheader'] = "has value"
    return response



def url_int_argument(request, first_arg):
    """
    Write a view that receives one integer parameter in the URL, and displays it
    in the response text.
    """
    return HttpResponse(str(first_arg))



def url_str_argument(request, first_arg):
    """
    Write a view that receives one string parameter in the URL, and displays it
    in the response text.
    """
    return HttpResponse(str(first_arg))



def url_multi_arguments(request, first_arg, second_arg):
    """
    Write a view that receives two parameters in the URL, and display them
    in the response text.
    """
    return HttpResponse(str(first_arg)+str(second_arg))



def get_params(request):
    """
    Write a view that receives GET arguments and display them in the
    response text.
    """
    args = request.GET.keys()
    result = ""
    for key in args:
        result += str(key)
    return HttpResponse (result)

