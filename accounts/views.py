from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from .forms import UserRegistrationForm, UserLoginForm

# API Views
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserProfileSerializer(user).data}, status=201)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user': UserProfileSerializer(user).data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully.'})

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_api(request):
    if request.method == 'GET':
        return Response(UserProfileSerializer(request.user).data)
    serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

# Template Views
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Daily Servant, {user.first_name}! 🎉')
            if user.role == 'servant':
                return redirect('servant_register_profile')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}! 👋')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm(request)
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'accounts/profile.html', {'user': request.user})
