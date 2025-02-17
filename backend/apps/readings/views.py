"""
These classes describe one way of entering into the web site.
"""

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import StoryPrototype, Student, Document
from .analysis import RereadingAnalysis
from .serializers import (
    StoryPrototypeSerializer, StudentPrototypeSerializer, AnalysisSerializer,
    DocumentSerializer, StudentSerializer
)


@api_view(['GET'])
def reading_view(request, doc_id):
    """
    Send a document with its associated segments, questions, prompts, etc.
    to the frontend
    """
    # TODO(ra): implement me!


class ListDocument(generics.ListCreateAPIView):
    """View a list of documents or create a new one"""
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class DetailDocument(generics.RetrieveUpdateDestroyAPIView):
    """Get a single document or update/delete it"""
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class ListStudent(generics.ListCreateAPIView):
    """View a list of students or create a new one"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class DetailStudent(generics.RetrieveUpdateDestroyAPIView):
    """Get a single student's data or update/delete it"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


################################################################################
# Prototype views
# The API endpoints below were for the prototype from summer 2019
################################################################################
class ListStudentPrototype(generics.ListCreateAPIView):
    """ View a list of students of create a new one """
    queryset = Student.objects.all()
    serializer_class = StudentPrototypeSerializer


class DetailStudentPrototype(generics.RetrieveUpdateDestroyAPIView):
    """ Get a single Student or update/delete it """
    queryset = Student.objects.all()
    serializer_class = StudentPrototypeSerializer


class ListStoryPrototype(generics.ListCreateAPIView):
    """ Get a list of story objects """
    queryset = StoryPrototype.objects.all()
    serializer_class = StoryPrototypeSerializer


class DetailStoryPrototype(generics.RetrieveUpdateDestroyAPIView):
    """ Get a single story object, or update/delete it """
    queryset = StoryPrototype.objects.all()
    serializer_class = StoryPrototypeSerializer


@api_view(['GET'])
def analysis(request):
    """
    Init a RereadingAnalysis, and serialize it to send to the frontend.
    """
    analysis_obj = RereadingAnalysis()
    serializer = AnalysisSerializer(instance=analysis_obj)
    return Response(serializer.data)
