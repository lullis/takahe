from rest_framework import generics

from users.models.identity import Identity

from . import serializers


class IdentityCreateView(generics.CreateAPIView):
    serializer_class = serializers.IdentityCreateSerializer
    model = Identity
