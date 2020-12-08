import django_filters.rest_framework

from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny

from .models import Bond
from .serializers import BondSerializer, UserSerializer


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
