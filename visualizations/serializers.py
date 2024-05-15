from rest_framework import serializers
from results.models import *

class ResultSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['course','semester','passout_year','result_json']
class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['id','course','semester','passout_year']