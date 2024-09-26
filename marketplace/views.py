from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAgentOrReadOnly, IsAgent, IsAuthenticatedAndOwner
from .models import Property, PropertyImage, Flags
from .serializers import PropertySerializer, PropertyStatusSerializer, FlagSerializer

# Create your views here.
class PropertyAPIView(generics.GenericAPIView):
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type']
    search_fields = ['type']
    permission_classes = [IsAgentOrReadOnly]
    
    def get_queryset(self):
        queryset = Property.objects.all()
        property_type = self.request.query_params.get('type', None)
        
        if property_type is not None:
            queryset = queryset.filter(type=property_type)
        
        return queryset
    
    @swagger_auto_schema(operation_description="Get a list of property adverts")
    def get(self, request):
        properties = self.get_queryset()
        serializer = self.serializer_class(instance=properties, many=True)
        
        message = {
            "status": "success",
            "data": serializer.data,
        }
        return Response(message, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_description="Create a property advert")
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        user = request.user
        agent = user.agent_profile
        
        if serializer.is_valid():
            serializer.save(owner=agent)
            message = {
                "status": "success",
                "data": serializer.data,
            }
            return Response(message, status=status.HTTP_201_CREATED)
        message = {
            "status": "error",
            "error": serializer.errors,
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    
class SinglePropertyAPIView(generics.GenericAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAgentOrReadOnly]
    
    @swagger_auto_schema(operation_description="Retrieve a single property advert by id")
    def get(self, request, pk):
        property = get_object_or_404(Property, pk=pk)
        serializer = self.serializer_class(instance=property)
        message = {
            "status": "success",
            "data": serializer.data,
        }
        return Response(message, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_description="Update a single property advert by id")
    def put(self, request, pk):
        property = get_object_or_404(Property, pk=pk)
        data = request.data
        serializer = self.serializer_class(instance=property, data=data)
        
        if serializer.is_valid():
            serializer.save()
            message = {
                "status": "success",
                "data": serializer.data,
            }
            return Response(message, status=status.HTTP_201_CREATED)
        message = {
            "status": "error",
            "error": serializer.errors,
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(operation_description="Delete a property advert by id")
    def delete(self, request, pk):
        property = get_object_or_404(Property, pk=pk)
        property.delete()
        message = {
            "status": "success",
            "message": "Property deleted successfully!"
        }
        return Response(message, status=status.HTTP_204_NO_CONTENT)            
        
    
class PropertyStatusAPIView(generics.UpdateAPIView):
    serializer_class = PropertyStatusSerializer
    permission_classes = [IsAgent]
    queryset = Property.objects.all()
    
    @swagger_auto_schema(operation_description="Update the status of a property by id") 
    def patch(self, request, pk):
        property = self.get_object()
        data = request.data
        serializer = self.serializer_class(data=data, instance=property)
        
        if serializer.is_valid():
            serializer.save()
            message = {
                "status": "success",
                "data": serializer.data,
            }
            return Response(message, status=status.HTTP_200_OK)
        message = {
            "status": "error",
            "error": serializer.errors,
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
            

class FlagCreateView(generics.CreateAPIView):
    queryset = Flags.objects.all()
    permission_classes = [IsAuthenticatedAndOwner]
    serializer_class = FlagSerializer

    @swagger_auto_schema(operation_description="Flag a property advert")
    def post(self, request, *args, **kwargs):
        property_id = self.kwargs['pk']
        property_instance = Property.objects.get(pk=property_id)  # Fetch the property instance

        # Create the flag with property instance
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, property_id=property_instance)
            message = {
                "status": "success",
                "data": serializer.data,
            }
            return Response(message, status=status.HTTP_201_CREATED)
        message = {
            "status": "error",
            "error": serializer.errors,
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
        
class FlagListView(generics.ListAPIView):
    # List of all flags
    queryset = Flags.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FlagSerializer
    

class FlagPropertyList(generics.ListAPIView):
    # List of all flags made on a particular property
    serializer_class = FlagSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        flags = Flags.objects.all().filter(property_id=pk)
        serializer = self.serializer_class(instance=flags, many=True)
        message = {
            "status": "success",
            "data": serializer.data,
        }
        return Response(message, status=status.HTTP_200_OK)
        
    
class FlagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flags.objects.all()
    permission_classes = [IsAuthenticatedAndOwner]
    serializer_class = FlagSerializer
    
    def get_object(self):
        flag = super().get_object()
        
        # Ensure that the flag belongs to the user making the request
        if flag.created_by != self.request.user:
            raise PermissionDenied("You do not have permission to modify this flag.")
        return flag

    @swagger_auto_schema(operation_description="Update a flag by id")
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete a flag by id")
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)