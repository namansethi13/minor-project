from rest_framework import serializers
from .models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'course', 'subject', 'code', 'credit', 'is_not_university', 'semester', 'is_practical']