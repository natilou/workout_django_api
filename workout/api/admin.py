from api.models import Exercise, FavoriteExercise, Workout, WorkoutExercise
from django.contrib import admin

admin.site.register(Workout, admin.ModelAdmin)
admin.site.register(WorkoutExercise, admin.ModelAdmin)
admin.site.register(Exercise, admin.ModelAdmin)
admin.site.register(FavoriteExercise, admin.ModelAdmin)
