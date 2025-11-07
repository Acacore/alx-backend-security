from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit



# Create your views here.

def home(request):
    return render(request, "ip_tracking/home.html")


@csrf_exempt  # only if you're testing locally, not in production
@ratelimit(key='user_or_ip', rate='10/m', method='POST', block=True)
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)
    return HttpResponse("Send POST request to log in")



def limit_by_auth(view_func):
    def wrapper(request, *args, **kwargs):
        rate = '10/m' if request.user.is_authenticated else '5/m'
        decorator = ratelimit(key='user_or_ip', rate=rate, block=True)
        return decorator(view_func)(request, *args, **kwargs)
    return wrapper
