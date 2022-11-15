from django.http import JsonResponse
from .models import Book
from .serializers import BookSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


#### View sets ####
# class BookViewSets(viewsets.ViewSet):
#     def list(self, request):
#         book = Book.objects.all()
#         serializer = BookSerializer(book, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = BookSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk=None):
#         queryset = Book.objects.all()
#         book = get_object_or_404(queryset, pk=pk)
#         serializer = BookSerializer(book)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         book = Book.objects.get(pk=pk)
#         serializer = BookSerializer(book, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(status=status.HTTP_400_BAD_REQUEST)



#### Generic View sets ####
# class BookViewSets(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
#     serializer_class = BookSerializer
#     queryset = Book.objects.all()



#### Model ViewSets ####
class BookViewSets(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()




#### Generic api views ####
class GenericApiView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    lookup_field = 'id'
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, id =None):

        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)




#### class based api views ####
class BookApiView(APIView):
    def get(self, request):
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer= BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetails(APIView):
    def get_object(self, id):
        try:
            return Book.objects.get(pk = id)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        book = self.get_object(id)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    def put(self, request, id):
        book = self.get_object(id)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        book = self.get_object(id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




#### function based api views with api_view decorator ####
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def book_list(request):
    if request.method == 'GET':
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer= BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT', 'DELETE'])
def book_details(request, id):

    try:
        book = Book.objects.get(pk = id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)