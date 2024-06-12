from rest_framework import status, viewsets
from rest_framework.response import Response

from instagram.models import Account
from .serializers import LeadSerializer, LeadsSerializer
from .models import Lead, Leadv1

class LeadManager(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def list(self, request):

        leads = Lead.objects.all()
        instagram_accounts = []
        for lead in leads:
            instagram_accounts.append(Account.objects.filter(id=lead.instagram.id).values())

        response = {"status_code": status.HTTP_200_OK, "instagram": instagram_accounts}
        return Response(response, status=status.HTTP_200_OK)

class LeadsViewSet(viewsets.ModelViewSet):
    queryset = Leadv1.objects.all()
    serializer_class = LeadsSerializer

    # todo: implement filters later
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Custom create method
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)