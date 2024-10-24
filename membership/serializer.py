from rest_framework import serializers
from .models import Membership

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'