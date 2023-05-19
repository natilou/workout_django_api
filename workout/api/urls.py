from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    EquipmentViewSet,
    ExerciseViewSet,
    ForceViewSet,
    LevelViewSet,
    MechanicViewSet,
    MuscleViewSet,
    ProfileDetailViewSet,
    UsersViewSet,
)

router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"equipments", EquipmentViewSet)
router.register(r"levels", LevelViewSet)
router.register(r"mechanics", MechanicViewSet)
router.register(r"muscles", MuscleViewSet)
router.register(r"exercises", ExerciseViewSet)
router.register(r"forces", ForceViewSet)
router.register(r"users", UsersViewSet, basename="users")
router.register(r"profile", ProfileDetailViewSet, basename="profile")

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
