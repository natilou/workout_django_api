from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (
    CategoryViewSet,
    ChangePasswordView,
    EquipmentViewSet,
    ExerciseViewSet,
    ForceViewSet,
    LevelViewSet,
    LogoutAllView,
    LogoutView,
    MechanicViewSet,
    MuscleViewSet,
    RegisterView,
    UpdateProfileView,
    UsersViewSet,
    WorkoutViewSet,
    WorkoutSessionViewSet,
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
router.register(r"workouts", WorkoutViewSet, basename="workouts")
router.register(r"workout_sessions", WorkoutSessionViewSet, basename="workouts_sessions")

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="auth_register"),
    path(
        "change_password/<int:pk>/",
        ChangePasswordView.as_view(),
        name="auth_change_password",
    ),
    path(
        "update_profile/<int:pk>/",
        UpdateProfileView.as_view(),
        name="auth_update_profile",
    ),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
    path("logout_all/", LogoutAllView.as_view(), name="auth_logout_all"),
]
