from rest_framework import serializers
from results.models import *

class ResultSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['course','semester','passout_year','result_json']
class ResultSerializer(serializers.ModelSerializer):
    course_abbreviation = serializers.SerializerMethodField()

    def get_course_abbreviation(self, obj):
        return obj.course.abbreviation

    class Meta:
        model = Result
        fields = ['course_abbreviation', 'semester', 'passout_year', 'result_json']
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','name','abbreviation']