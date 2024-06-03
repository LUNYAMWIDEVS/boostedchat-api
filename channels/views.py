from rest_framework.permissions import IsAuthenticated  # Import permission class
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import helpers_circular
from channels.models import ChannelManager

from .serializers import *
from .models import *
from setup.utils import setuputils
import json

class ChannelsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        return Response(helpers.channelsList())
        
        
class ChannelUserNameViewSet(viewsets.ModelViewSet):
    permission_classes = setuputils.get_permissions() #[IsAuthenticated]
    def get_serializer_class(self):
        serializerClass = ChannelUserNameSerializer # default value
        serializerClass = ChannelUserNameSerializer if self.action == "create" else serializerClass
        serializerClass = ChannelUserNameFilterSerializer if self.action == "list" else serializerClass
        serializerClass = ChannelUserNamePatchSerializer if self.action == "update" else serializerClass
        serializerClass = ChannelUserNameDeleteSerializer if self.action == "destroy" else serializerClass
        
        return serializerClass
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            LocalChannelManager = ChannelManager(serializer.validated_data['channel'])
            if LocalChannelManager is None:
                return Response({'message': 'Channel not supported'}, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            try:
                result = LocalChannelManager.save_channel_username(validated_data)
                result = ChannelUserNamesReadSerializer(result, many=False).data
                return Response({'message': 'Channel username created successfully', 'data': result}, status=status.HTTP_201_CREATED)
                # response_data = {
                #     'message': 'Channel username created successfully',
                #     'data': result,
                # }

                # # Serialize the response data to JSON format
                # json_data = json.dumps(response_data)

                # # Create the Response object with JSON content type in headers
                # return Response(json_data, status=status.HTTP_201_CREATED, content_type='application/json')

            except Exception as e:
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        serializer = self.get_serializer(data=request.query_params)
        if serializer.is_valid():
            LocalChannelManager = ChannelManager(serializer.validated_data['channel'])
            data = LocalChannelManager.read_channel_usernames(serializer.validated_data)
            serializer = ChannelUserNamesReadSerializer(data, many=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            LocalChannelManager = ChannelManager(serializer.validated_data['channel'])
            result = LocalChannelManager.update_channel_username(serializer.validated_data)
            # return Response({'error': 'Record updated'}, status=status.HTTP_200_OK)
            result = ChannelUserNamesReadSerializer(result, many=True).data
            return Response({'message': 'Channel username updated successfully', 'data': result}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # endpoint to delete a channel username
    def destroy(self, request, pk=None):
        serializer = self.get_serializer(data=request.query_params)
        if serializer.is_valid():
            LocalChannelManager = ChannelManager(serializer.validated_data['channel'])
            filters = {"id": serializer.validated_data['id']}
            result = LocalChannelManager.delete_channel_username(filters)
            return Response({'message': 'Channel username deleted successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

