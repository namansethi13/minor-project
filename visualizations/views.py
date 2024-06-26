from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ResultSerializer,ResultSerializerAll,CourseSerializer
from results.models import Result,Course


@api_view(['GET'])
def result(request):
    all_results = Result.objects.all()
    serializer = ResultSerializer(all_results, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def result_id(request,id):
    try:
        result = Result.objects.get(id=id)
    except Result.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ResultSerializerAll(result)
    return Response(serializer.data)

@api_view(['GET'])
def getcourse(request,id):
    try:
        course=Course.objects.get(id=id)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CourseSerializer(course)
    return Response(serializer.data)

        

