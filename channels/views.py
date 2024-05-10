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
                result = ChannelUserNameResponseSerializer(result, many=False).data
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
            LocalChannelManager.update_channel_username(serializer.validated_data)
            print(serializer.validated_data["filters"])
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # ChannelUserNameModel = helpers_circular.getChannelUserNameModel(channel)
        # if ChannelUserNameModel is None:
        #     return Response({'message': 'Channel not supported'}, status=status.HTTP_400_BAD_REQUEST)
        
        # try:
        #     channel_username = ChannelUserNameModel.objects.get(pk=pk)
        # except ChannelUserNameModel.DoesNotExist:
        #     return Response({'error': 'Channel username not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # serializer = self.serializer_class(channel_username, data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({'message': 'Channel username updated successfully'})
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, pk=None):
    #     channel = request.query_params.get('channel')
    #     if not channel:
    #         return Response({'error': 'Channel parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
    #     ChannelUserNameModel = self.getChannelUserNameModel(channel)
    #     if ChannelUserNameModel is None:
    #         return Response({'message': 'Channel not supported'}, status=status.HTTP_400_BAD_REQUEST)
        
    #     try:
    #         channel_username = ChannelUserNameModel.objects.get(pk=pk)
    #     except ChannelUserNameModel.DoesNotExist:
    #         return Response({'error': 'Channel username not found'}, status=status.HTTP_404_NOT_FOUND)
        
    #     channel_username.delete()
    #     return Response({'message': 'Channel username deleted successfully'})

    # def retrieve(self, request, pk=None):
    #     channel = request.query_params.get('channel')
    #     if not channel:
    #         return Response({'error': 'Channel parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
    #     ChannelUserNameModel = self.getChannelUserNameModel(channel)
    #     if ChannelUserNameModel is None:
    #         return Response({'message': 'Channel not supported'}, status=status.HTTP_400_BAD_REQUEST)
        
    #     try:
    #         channel_username = ChannelUserNameModel.objects.get(pk=pk)
    #     except ChannelUserNameModel.DoesNotExist:
    #         return Response({'error': 'Channel username not found'}, status=status.HTTP_404_NOT_FOUND)
        
    #     serializer = self.serializer_class(channel_username)
    #     return Response(serializer.data)






    #     channel_username = ChannelUserName.objects.get(pk=pk)
    #     serializer = self.serializer_class(channel_username)
    #     return Response(serializer.data)

    # def update(self, request, pk=None):
    #     channel_username = ChannelUserName.objects.get(pk=pk)
    #     serializer = self.serializer_class(channel_username, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'message': 'Channel username updated successfully'})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, pk=None):
    #     channel_username = ChannelUserName.objects.get(pk=pk)
    #     channel_username.delete()
    #     return Response({'message': 'Channel username deleted successfully'})
"""
Create a viewset for each channel
"""
class InstagramViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        # return array of strings
        return Response(["instagram", "whatsapp", "linkedIn", "sandbox"])
    
    def create(self, request):
        serializer = ChannelUserNameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        # create or update
        return Response({"message": "success"})