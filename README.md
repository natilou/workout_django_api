# **WorkoutEmpire API** [![github-action](https://github.com/natilou/workout_django_api/actions/workflows/ci.yml/badge.svg)](https://github.com/natilou/workout_django_api/actions/workflows/ci.yml) [![codecov](https://codecov.io/gh/natilou/workout_django_api/branch/main/graph/badge.svg?token=DMCJYFDTJE)](https://codecov.io/gh/natilou/workout_django_api)

Welcome to the **WorkoutEmpire API**! This repository serves as the backend for the comprehensive WorkoutEmpire platform, which is currently under development. I'm working to provide users with a vast array of different exercises and workout routines. With this API, users will track their exercises, record time and weights used, monitor their progress in areas such as strength, flexibility, and cardio, and build their fitness empire using the tools and knowledge provided. 

## Present features
- **Workout Routines**: Users can create workout routines based on their preferred exercise types, muscle groups, equipment availability, fitness levels, categories, mechanics, and forces.
- **Exercise Filtering**: Users are able to filter exercises based on specific criteria such as muscle group, equipment, fitness level, category, mechanics, and forces. This allows users to find exercises that meet their specific needs and preferences.
- **User Authentication**: Users are able to register, login, and logout from the API.

## Planned Features
The WorkoutEmpire API aims to provide the following features:
- **Exercise Tracking**: Users will be able to log their exercises, including details such as exercise type, duration, sets, reps, and weights used.
- **Progress Monitoring**: Users will be able to track their progress in various fitness aspects, such as strength, flexibility, and cardio. The API will provide tools to record and analyze this data, allowing users to monitor their development over time.
- **Personalization**: The API will allow users to personalize their fitness journey. It will provide recommendations based on user preferences, helping them create personalized training programs.

## Dependencies
The WorkoutEmpire API has the following dependencies:

    Django (v4.2.2)
    Django Rest Framework (v3.14.0)
    Django Filter (v23.2)
    psycopg2-binary (v2.9.6)
    djangorestframework-simplejwt (v5.2.2)
    sentry-sdk (v1.25.0)

Development Dependencies

    isort (v5.12.0)
    flake8 (v6.0.0)
    ipdb (v0.13.13)
    black (v23.3.0)
    django-debug-toolbar (v4.1.0)
    pytest (v7.3.1)
    pytest-django (v4.5.2)
    pytest-cov (v4.1.0)
    freezegun (v1.2.2)
    
## API Documentation
The API documentation is currently in progress and will be made available soon. I'm working on providing comprehensive documentation for the API endpoints, request formats, and response structures. Stay tuned for updates!
    
## Special thanks
I would like to express my sincere gratitude to [yuhonas/free-exercise-db](https://github.com/yuhonas/free-exercise-db) for providing the Free Exercise Database. This open-source repository has been instrumental in the development of WorkoutEmpire, allowing me to leverage a comprehensive collection of exercises for the platform.
I highly recommend exploring [yuhonas/free-exercise-db](https://github.com/yuhonas/free-exercise-db) for anyone in need of an extensive and freely accessible exercise database.