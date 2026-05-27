from django.contrib import admin
from django.urls import path
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                "status": "success",
                "message": "User logged in successfully",
                "username": username
            })

        return JsonResponse({
            "status": "failed",
            "message": "Invalid username or password"
        }, status=401)

    return JsonResponse({"message": "Use POST request for login"})


@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({
        "status": "success",
        "message": "User logged out successfully"
    })


def dealers_by_state(request, state):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dealers by State</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 30px;
            }}
            h1 {{
                color: #222;
            }}
            .dealer {{
                background-color: white;
                padding: 15px;
                margin: 15px 0;
                border-radius: 8px;
                box-shadow: 0 0 8px #ccc;
            }}
        </style>
    </head>
    <body>
        <h1>Dealers filtered by State</h1>
        <p>Showing dealers located in <strong>{state}</strong></p>

        <div class="dealer">
            <h2>Auto World Dealer</h2>
            <p><strong>ID:</strong> 1</p>
            <p><strong>City:</strong> Kansas City</p>
            <p><strong>State:</strong> Kansas</p>
            <p><strong>Address:</strong> 123 Main Street</p>
        </div>

        <div class="dealer">
            <h2>Best Cars Dealer</h2>
            <p><strong>ID:</strong> 2</p>
            <p><strong>City:</strong> Topeka</p>
            <p><strong>State:</strong> Kansas</p>
            <p><strong>Address:</strong> 456 Oak Avenue</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", login_user),
    path("logout/", logout_user),
    path("dealers/state/<str:state>/", dealers_by_state),
]