from rest_framework import viewsets
from .models import Data
from rest_framework import filters
from .serializers import DataSerializers
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework import status



DEFAULT_PAGE = 1


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


class Custom_Pagination_Fixed(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = 2
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.page.paginator.count,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)),
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'results': data
        })

class DataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Data.objects.all().order_by('-id')
    serializer_class = DataSerializers
    # filterset_fields = ('name', 'city')
    # filter_fields = ('name', 'city')
    search_fields = ['name', 'city','occupation','age']
    ordering_fields = ['id']
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    pagination_class = Custom_Pagination_Fixed

###testing function views decorator based like @ api views
@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Data.objects.all()
        serializer = DataSerializers(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DataSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Data.objects.get(pk=pk)
    except Data.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DataSerializers(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DataSerializers(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)