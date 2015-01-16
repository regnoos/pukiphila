from rest_framework import serializers
from rest_framework.reverse import reverse

from soonger.base.api.mixins import DefaultsMixin

from .models import User


class UserSerializer(DefaultsMixin, serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'birthday', 'gender', 'country', 'is_active', 'full_name', 'bio', 'photo',
                  'date_joined', 'is_staff', 'followers', 'verificated', 'website', 'profilehits', 'links',)

    def get_links(self, obj):
        request = self.context['request']
        username = obj.get_username()
        return {
            'self': reverse('user-detail', kwargs={User.USERNAME_FIELD: username}, request=request),

        }
