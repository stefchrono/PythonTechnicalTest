from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.filters import SearchFilter
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny

from .models import Bond
from .forms import CreateUserForm
from .serializers import BondSerializer, UserSerializer

import django_filters.rest_framework


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('bonds')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                token = Token.objects.get(user=user).key
                return redirect('login')
                
        context={'form':form}
        return render(request, 'register.html', context)
    

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('bonds')
    else:
        context = {}
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('bonds')

            else:
                messages.info(request, 'Username Or Password is incorrect')
  
        return render(request, 'login.html')


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class HelloWorld(generics.ListCreateAPIView):
    queryset = Bond.objects.all()
    permission_classes = (IsAuthenticated,) 
    serializer_class = BondSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['legal_name']
    
    # Add owner on save
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Filter queryset by owner
    def get_queryset(self):
        owner_queryset = self.queryset.filter(user=self.request.user)
        return owner_queryset
