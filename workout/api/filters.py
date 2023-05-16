from api.models import Exercise
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
        ]
