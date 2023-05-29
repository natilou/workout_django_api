from django.contrib import admin
from api.models import Workout, WorkoutExercise

admin.site.register(Workout, admin.ModelAdmin)
admin.site.register(WorkoutExercise, admin.ModelAdmin)