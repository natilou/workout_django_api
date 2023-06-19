from api.models import Exercise, User
from django_filters import rest_framework as filters


class ExerciseFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category__name", lookup_expr="iexact")
    equipment = filters.CharFilter(field_name="equipment__name", lookup_expr="iexact")
    force = filters.CharFilter(field_name="force__name", lookup_expr="iexact")
    level = filters.CharFilter(field_name="level__name", lookup_expr="iexact")
    mechanic = filters.CharFilter(field_name="mechanic__name", lookup_expr="iexact")
    muscle = filters.CharFilter(
        field_name="muscle_per_exercise__muscle__name",
        label="Muscle name",
        lookup_expr="iexact",
    )
    primary_muscle = filters.CharFilter(
        method="filter_by_primary_muscle",
        label="Primary muscle",
    )
    secondary_muscle = filters.CharFilter(
        method="filter_by_secondary_muscle",
        label="Secondary muscle",
    )

    favorites = filters.BooleanFilter(
        method="filter_by_favorites",
        label="Favorites",
    )

    def filter_by_primary_muscle(self, queryset, name, value):
        return queryset.filter(
            muscle_per_exercise__muscle__name__iexact=value,
            muscle_per_exercise__is_primary_muscle=True,
        )

    def filter_by_secondary_muscle(self, queryset, name, value):
        return queryset.filter(
            muscle_per_exercise__muscle__name__iexact=value,
            muscle_per_exercise__is_primary_muscle=False,
        )

    def filter_by_favorites(self, queryset, name, value):
        if value:
            request_user = self.request.user
            user = User.objects.get(id=request_user.id)
            return queryset.filter(favorite_exercises__user=user)

    class Meta:
        model = Exercise
        fields = [
            "category",
            "equipment",
            "force",
            "level",
            "mechanic",
            "muscle",
            "primary_muscle",
            "secondary_muscle",
            "favorites",
        ]
