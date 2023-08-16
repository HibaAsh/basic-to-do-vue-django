from rest_framework import serializers
from .models import Task
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    # created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    # finished_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    # full_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = Task
        fields = ["id", "title", "description", "completed", "created_at", "finished_at", "full_time"] 

    
    # def update(self, instance, validated_data):
    #     print("validated data:", validated_data)
    #     instance.title = validated_data["title"]
    #     instance.description = validated_data["description"]

    #     print('validated_data["completed"]: ', validated_data["completed"])
    #     print('instance.completed: ', instance.completed)

    #     if (validated_data["completed"]) and (validated_data["completed"] != instance.completed):
    #         print("Condition is met !!")
    #         instance.finished_at = timezone.now()
    #         instance.full_time = instance.finished_at - instance.created_at
    #     else:
    #         instance.finished_at = None
    #         instance.full_time = None

    #     instance.completed = validated_data["completed"]

        
    #     instance.save()

    #     return instance