from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import (
    BlacklistedToken,
    OutstandingToken,
    RefreshToken,
)

from .filters import ExerciseFilter
from .models import Category, Equipment, Exercise, Force, Level, Mechanic, Muscle
from .serializers import (
    CategorySerializer,
    ChangePasswordSerializer,
    EquipmentSerializer,
    ExerciseSerializer,
    ForceSerializer,
    LevelSerializer,
    MechanicSerializer,
    MuscleGroupSerializer,
    RegisterSerializer,
    UpdateUserSerializer,
    UserSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Category to be viewed or edited.
    """

    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Equipment to be viewed or edited.
    """

    queryset = Equipment.objects.all().order_by("name")
    serializer_class = EquipmentSerializer


class LevelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Level to be viewed or edited.
    """

    queryset = Level.objects.all().order_by("name")
    serializer_class = LevelSerializer


class MechanicViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Mechanic to be viewed or edited.
    """

    queryset = Mechanic.objects.all().order_by("name")
    serializer_class = MechanicSerializer


class MuscleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Muscle to be viewed or edited.
    """

    queryset = Muscle.objects.all().order_by("name")
    serializer_class = MuscleGroupSerializer


class ForceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Force to be viewed or edited.
    """

    queryset = Force.objects.all().order_by("name")
    serializer_class = ForceSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Exercise to be viewed or edited.
    """

    queryset = Exercise.objects.all().order_by("name")
    serializer_class = ExerciseSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ExerciseFilter


class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UpdateUserSerializer


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)
