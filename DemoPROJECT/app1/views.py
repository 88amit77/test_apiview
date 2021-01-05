from rest_framework import viewsets
from .models import Data
from rest_framework import filters
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import NotFound as NotFoundError
###for auth
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated



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


###class based view
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


###function based view for view all data at once

class CustomPaginator(PageNumberPagination):
    page_size = 3 # Number of objects to return in one page

    def generate_response(self, query_set, serializer_obj, request):
        try:
            page_data = self.paginate_queryset(query_set, request)
        except NotFoundError:
            return Response({"error": "No results found for the requested page"}, status=status.HTTP_400_BAD_REQUEST)

        serialized_page = serializer_obj(page_data, many=True)
        return self.get_paginated_response(serialized_page.data)

class DataAPIView(APIView):
    ##working
    # def get(self, request):
    #     data = Data.objects.all()
    #
    #     # the many param informs the serializer that it will be serializing more than a single data.
    #     serializer = DataSerializers0(data, many=True)
    #     return Response({"data": serializer.data})
    ###view all with pagination
    def get(self, request, format=None):
        data_all = Data.objects.all()
        paginator = CustomPaginator()
        response = paginator.generate_response(data_all, DataSerializers0, request)

        return response



###function based view for post update and delete and for view single data as per request
class DataAPIViewDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Data.objects.get(pk=pk)
        except Data.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data1 = self.get_object(pk)
        serializer = DataSerializers1(data1)
        return Response({"data": serializer.data})

    def post(self, request):
        data1 = request.data.get('data')

        # Create an new data from the above data
        serializer = DataSerializers1(data=data1)
        if serializer.is_valid(raise_exception=True):
            data_saved = serializer.save()
        return Response({"success": "Data'{}' created successfully".format(data_saved.name)})

    def put(self, request, pk, format=None):
        data1 = self.get_object(pk)
        serializer = DataSerializers1(data1, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        data1 = self.get_object(pk)
        data1.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

##auth testing
# class ExampleView(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, format=None):
#         content = {
#             'user': unicode(request.user),  # `django.contrib.auth.User` instance.
#             'auth': unicode(request.auth),  # None
#         }
#         return Response(content)
###decorator based
# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
# def example_view(request, format=None):
#     content = {
#         'user': unicode(request.user),  # `django.contrib.auth.User` instance.
#         'auth': unicode(request.auth),  # None
#     }
#     return Response(content)


class AuthViewTest(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'message': 'Hello, Amit welcome to DRF AUTH !'}
        return Response(content)