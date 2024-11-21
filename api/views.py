from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Donor,BloodInventory,BloodRequest
from .serializers import DonorSerializer,BloodInventorySerializer,BloodRequestSerializer
from rest_framework.response import Response
from rest_framework import status


class DonorViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer


class BloodInventoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = BloodInventory.objects.all()
    serializer_class = BloodInventorySerializer 

    def perform_create(self, serializer):
        # Extract the blood type from the request data
        blood_type = serializer.validated_data.get('blood_type')
        
        # Check if a BloodInventory record already exists for this blood type
        existing_inventory = BloodInventory.objects.filter(blood_type=blood_type).first()
        
        if existing_inventory:
            # If exists, update the existing record with the new units
            existing_inventory.units += serializer.validated_data.get('units', 0)  # Add the new units
            existing_inventory.save()
            return Response({'message': 'Units added to existing blood group.'}, status=status.HTTP_200_OK)
        
        # If not exists, create a new record
        serializer.save()

        return Response({'message': 'New blood group created.'}, status=status.HTTP_201_CREATED)



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
        serializer.save(user=self.request.user) 

    def get_queryset(self):
        user = self.request.user
    
        if user.is_staff:
            return BloodRequest.objects.all()
        return BloodRequest.objects.filter(user=user)
    