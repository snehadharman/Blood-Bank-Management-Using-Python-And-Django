from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Donor,BloodInventory,BloodRequest
from .serializers import DonorSerializer,BloodInventorySerializer,BloodRequestSerializer




class DonorViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer


class BloodInventoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = BloodInventory.objects.all()
    serializer_class = BloodInventorySerializer
    permission_classes = [permissions.IsAdminUser] 



class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to allow only admin users or the owner of the request to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Admin users can access any object
        if request.user.is_staff:
            return True
        # Regular users can only access their own requests
        return obj.user == request.user

class BloodRequestViewSet(viewsets.ModelViewSet):
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Set the user to the currently logged-in user

    def get_queryset(self):
        user = self.request.user
        # Admins can view all requests; regular users can only view their own
        if user.is_staff:
            return BloodRequest.objects.all()
        return BloodRequest.objects.filter(user=user)
    

