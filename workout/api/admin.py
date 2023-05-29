from api.models import Workout, WorkoutExercise
from django.contrib import admin

admin.site.register(Workout, admin.ModelAdmin)
admin.site.register(WorkoutExercise, admin.ModelAdmin)
