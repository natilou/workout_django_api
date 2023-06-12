from api.models import Workout, WorkoutExercise, Exercise
from django.contrib import admin

admin.site.register(Workout, admin.ModelAdmin)
admin.site.register(WorkoutExercise, admin.ModelAdmin)
admin.site.register(Exercise, admin.ModelAdmin)
