from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer 

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()  
            user.password = make_password(serializer.validated_data['password'])  
            user.save()
            
            return redirect("login_page")
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST.get('username')  
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
            print("User found in DB: ", user)
        except User.DoesNotExist:
            user = None
            print("User does not exist in DB.")
        
        if user is not None:
            user = authenticate(request, username=username, password=password)
            print("Here is the authenticated user: ", user)
            if user is not None:
                login(request, user)
      
                refresh = RefreshToken.for_user(user)
                
                response = redirect('dashboard')
                response.set_cookie(key='access_token', value=str(refresh.access_token), httponly=True)
                response.set_cookie(key='refresh_token', value=str(refresh), httponly=True)
                
                return response
            else:
                print("Authentication failed.")
                return render(request, 'auth/login.html', {'error': 'Invalid credentials'})
        else:
            return render(request, 'auth/login.html', {'error': 'User does not exist'})


def logout_view(request):
    logout(request)
    return redirect('login_page')


def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_page')
        return view_func(request, *args, **kwargs)
    return wrapper


@custom_login_required
def dashboard(request):
    user = request.user
    return render(request, 'dashboard.html', {'user': user})


def login_page(request):
    return render(request, 'auth/login.html')


def register_page(request):
    return render(request, 'auth/register.html')

