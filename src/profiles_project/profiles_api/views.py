from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from . import serializers
from . import models
from . import permissions

# Create your views here.


class HelloApiView(APIView):
    """Test APIView"""

    serailizer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Return a list of APIViews."""

        an_apiview = [
            'Uses HTTP methods as function (get, post, put, patch, delete)',
            'It is similar to a traditional Django view',
            'Gives you the most control over your logic',
            'Is mapped mannualy to URLs'
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name."""

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle an update method."""

        return Response({'method': 'Put'})

    def patch(self, request, pk=None):
        """Patch request, only update the fields provided in the request."""

        return Response({'method': 'Patch'})

    def delete(self, request, pk=None):
        """Delete an object"""

        return Response({'method': 'Delete'})


class HelloViewSet(viewsets.ViewSet):
    """Test API Viewset"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""

        a_viewset = [
            'Uses actions (list, create, update, update partial, destroy)',
            'Automatically map to URLs using Routers',
            'Provide more functionality with less code'
        ]

        return Response({'message': 'Hello', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello messsage"""

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handles getting an object by its ID"""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handles updating an object by its ID"""

        return Response({'http_method': 'Update'})

    def partial_update(self, request, pk=None):
        """Hanlde updating a part of the object"""

        return Response({'http_method': 'partial_update'})

    def destroy(self, request, pk=None):
        """handles deleting an object by its ID."""

        return Response({'http_method': 'destroy'})


class UserProfileViewset(viewsets.ModelViewSet):
    """Handles reading and updating profile"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    """Added permission to update the own user profile."""
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)
    """Added Search by name and email feature."""


class LoginViewSet(viewsets.ViewSet):
    """Check email and password and retun an auth token."""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """use the AuthToken APIView to validate and create a token."""

        return ObtainAuthToken().post(request)


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, updating and reading profile feed items."""

    authentication_classes = (TokenAuthentication,)

    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated,)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""

        serializer.save(user_profile=self.request.user)
