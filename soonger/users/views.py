from rest_framework import viewsets

from soonger.base.api.mixins import DefaultsMixin

from .models import User
from .serializers import UserSerializer


class UserViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing users."""

    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer