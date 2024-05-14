from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models.domain import Domain
from users.models.identity import Identity
from users.models.user import User
from users.services import IdentityService
from users.views.admin.domains import DomainValidator


class IdentityCreateSerializer(serializers.ModelSerializer):
    email_address = serializers.EmailField(write_only=True)
    initial_password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    domain = serializers.CharField(validators=[DomainValidator], write_only=True)

    def validate_email_address(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This user is already registered")
        return value

    def validate_initial_password(self, value):
        if value:
            validate_password(value)
        return value

    def validate_domain(self, value):
        if not value:
            return None

        if Domain.objects.filter(domain=value).exists():
            raise serializers.ValidationError("Domain name is already registered")

        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email_address"],
            password=validated_data["initial_password"],
        )
        domain = Domain.objects.create(
            domain=validated_data["domain"],
            service_domain=None,
            public=False,
            default=False,
            local=True,
        )
        domain.users.add(user)
        username = validated_data["username"]
        return IdentityService.create(
            user=user,
            username=username,
            domain=domain,
            name=username,
            discoverable=True,
        )

    class Meta:
        model = Identity
        fields = (
            "id",
            "actor_uri",
            "email_address",
            "initial_password",
            "username",
            "domain",
        )
        read_only_fields = ("id", "actor_uri")
