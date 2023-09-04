from django_filters import rest_framework as filters
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import (
    BlacklistedToken,
    OutstandingToken,
    RefreshToken,
)

from .filters import ExerciseFilter
from .models import (
    Category,
    Equipment,
    Exercise,
    ExerciseLog,
    FavoriteExercise,
    Force,
    Level,
    Mechanic,
    Muscle,
    User,
    Workout,
    WorkoutSession,
)
from .permissions import UserPermission
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
    WorkoutSerializer,
    WorkoutSessionSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Category to be viewed or edited.
    """

    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [UserPermission]


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Equipment to be viewed or edited.
    """

    queryset = Equipment.objects.all().order_by("name")
    serializer_class = EquipmentSerializer
    permission_classes = [UserPermission]


class LevelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Level to be viewed or edited.
    """

    queryset = Level.objects.all().order_by("name")
    serializer_class = LevelSerializer
    permission_classes = [UserPermission]


class MechanicViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Mechanic to be viewed or edited.
    """

    queryset = Mechanic.objects.all().order_by("name")
    serializer_class = MechanicSerializer
    permission_classes = [UserPermission]


class MuscleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Muscle to be viewed or edited.
    """

    queryset = Muscle.objects.all().order_by("name")
    serializer_class = MuscleGroupSerializer
    permission_classes = [UserPermission]


class ForceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Force to be viewed or edited.
    """

    queryset = Force.objects.all().order_by("name")
    serializer_class = ForceSerializer
    permission_classes = [UserPermission]


class ExerciseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Exercise to be viewed or edited.
    """

    queryset = Exercise.objects.all().order_by("name")
    serializer_class = ExerciseSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ExerciseFilter
    permission_classes = [UserPermission]

    @action(
        methods=["post", "delete"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        exercise = Exercise.objects.get(id=pk)
        request_user = request.user
        user = User.objects.get(id=request_user.id)
        favorite, created = FavoriteExercise.objects.get_or_create(
            user=user, exercise=exercise
        )
        if request.method == "POST" and created:
            return Response(status=status.HTTP_201_CREATED)
        if request.method == "DELETE" and not created:
            favorite.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def logs(self, request, pk=None):
        exercise = Exercise.objects.get(id=pk)
        request_user = request.user
        user = User.objects.get(id=request_user.id)
        sets_made = request.data["sets_made"]
        reps_made = request.data.getlist("reps_per_set_made")
        weight_used = request.data.getlist("weight_used")
        location = request.data.get("location", None)
        end_datetime = request.data["end_datetime"]
        start_datetime = request.data["start_datetime"]
        workout_session = WorkoutSession.objects.create(
            user=user,
            location=location,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )
        ExerciseLog.objects.create(
            exercise=exercise,
            sets_made=int(sets_made),
            reps_per_set_made=reps_made,
            weight_used=weight_used,
            workout_session=workout_session
        )
        return Response(status=status.HTTP_201_CREATED)


class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    lookup_field = "username"


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


class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    queryset = Workout.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


class WorkoutSessionViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSessionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = WorkoutSession.objects.all()
