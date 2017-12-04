from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import *
from django.contrib.auth import get_user_model
PASSWORD_MAX_LENGTH = 128
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.StringRelatedField(source = 'user_type.user_type',read_only = True)

    class Meta:
        model = User
        fields = ("email","id", "user_type","mobile","is_active","comments","rooftop_area","consumption","total_bill_with_taxes",
                  "total_unit_consumption","total_per_unit_cost","willing_price_per_unit","price_escalation_per_year","plant_size_per_RT_area",
                  "plant_size_per_consumption","feasible_in_house_plant","customer_profile","income","cibil_report","review")


class UserRegisterSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True)

        def create(self, validated_data):
            user = User.objects.create(
                username=validated_data['email'],
                email=validated_data['email'],
                mobile=validated_data['mobile'],
                user_type_id=1
            )
            user.set_password(validated_data['password'])
            user.save()
            return user

        class Meta:
            model = User
            fields = ("email", "password", "mobile")

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ('__all__')


class EPC_DetailsSerializer(serializers.ModelSerializer):
    user_type = serializers.StringRelatedField(source = 'user.user_type.user_type',read_only = True)
    email = serializers.StringRelatedField(source = 'user.email',read_only = True)
    username = serializers.StringRelatedField(source = 'user.username',read_only = True)
    mobile = serializers.StringRelatedField(source = 'user.mobile',read_only = True)

    class Meta:
        model = EPC_Details
        fields = ("user_type","email","username","mobile","registered_name", "module_manufacturer","inverter_manufacturer",
                  "wiring_cost_range","civil_work_range","labor","total_cost_range")


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_Details
        fields = ('__all__')


class ResetPasswordSerializer(serializers.Serializer):
    """
    Reset password serializer
    """
    current_password = serializers.CharField(
        help_text=('Current Password'),
        max_length=PASSWORD_MAX_LENGTH,
    )
    password1 = serializers.CharField(
        help_text=('New Password'),
        max_length=PASSWORD_MAX_LENGTH,
        min_length=8,
        error_messages={
            "min_length": "Password length should be minimum 8 characters.",
        },
    )
    password2 = serializers.CharField(
        help_text=('New Password (confirmation)'),
        max_length=PASSWORD_MAX_LENGTH
    )

    def validate_current_password(self, value):
        """
        current password check
        """
        if self.instance.has_usable_password() and not self.instance.check_password(value):
            raise serializers.ValidationError('Current password is not correct.')
        return value

    def validate(self, data):
        """
        password_confirmation check
        """
        password_confirmation = data["password2"]
        password = data['password1']

        if password_confirmation != password:
            raise serializers.ValidationError({'password2': 'Password confirmation mismatch.'})
        return data

    def update(self, instance, validated_data):
        """ change password """
        if instance is not None:
            instance.set_password(validated_data.get('password2'))
            instance.save()
            return instance
        return User(**attrs)


class ModifyUserPasswordSerializer(serializers.Serializer):
    """
    Modify user's password by admin serializer
    """
    user_password1 = serializers.CharField(
        help_text=('New Password'),
        max_length=PASSWORD_MAX_LENGTH,
        min_length=8,
        error_messages={
            "min_length": "Password length should be minimum 8 characters.",
        },
    )
    user_password2 = serializers.CharField(
        help_text=('New Password (confirmation)'),
        max_length=PASSWORD_MAX_LENGTH
    )

    def validate(self, data):
        """
        password_confirmation check
        """
        password = data['user_password1']
        password_confirmation = data["user_password2"]

        if password_confirmation != password:
            raise serializers.ValidationError({'user_password2': 'Password confirmation mismatch.'})

        return data

    def update(self, instance, validated_data):
        """ change password """
        print instance
        if instance is not None:
            user = User.objects.get(id=instance)
            user.set_password(validated_data.get('user_password2'))
            user.save()
            return instance

        return User(**attrs)
