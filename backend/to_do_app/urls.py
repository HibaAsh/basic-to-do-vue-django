from django.urls import path, include
from rest_framework import routers
from .views import TaskViewSet

task_router = routers.DefaultRouter()
task_router.register('', TaskViewSet, basename="TaskViewSet")

urlpatterns = [
    path('task/', include(task_router.urls)),
]