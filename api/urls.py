from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonorViewSet,BloodInventoryViewSet,BloodRequestViewSet

router = DefaultRouter()
router.register(r'donors', DonorViewSet, basename='donor')
router.register(r'blood-inventory', BloodInventoryViewSet, basename='blood-inventory')
router.register(r'blood-requests', BloodRequestViewSet, basename='blood-request')



urlpatterns = [
    path('', include(router.urls)),  # Include all the donor-related routes
    

]
