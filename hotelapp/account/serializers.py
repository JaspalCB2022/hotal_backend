from django.contrib.auth.password_validation import validate_password as valid_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(max_length=60, min_length=8, write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "avatar",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "is_active",
            "role",
            "created_at",
            "updated_at",
            "password",
        ]
        read_only_fields = [
            "is_active",
            "role",
            "created_at",
            "updated_at",
        ]

    def validate_password(self, value):
        valid_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            self.validate_password(password)
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        user = self.context["request"].user
        is_superadmin = user.is_superuser
        if not is_superadmin:
            validated_data.pop("email", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def validate_avatar(self, avatar):
        if avatar:
            if not avatar.name.lower().endswith((".png", ".jpg", ".jpeg")):
                raise serializers.ValidationError("Only image files are allowed.")
            max_size = 5 * 1024 * 1024
            if avatar.size > max_size:
                raise serializers.ValidationError(
                    "File size too large. Max size is 5MB."
                )
        return avatar

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) != 10:
            raise serializers.ValidationError(
                "Phone number must be exactly 10 digits long."
            )
        return value

    

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=60, min_length=6, write_only=True)
    confirm_password = serializers.CharField(
        max_length=60, min_length=6, write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "is_active",
            "role",
            "password",
            "confirm_password",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "is_active",
            "role",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        if validated_data.get("password") != validated_data.get("confirm_password"):
            raise serializers.ValidationError("Password don't match")
        validated_data.pop("confirm_password")
        user = get_user_model().objects.create_user(**validated_data)
        return user


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=60, min_length=8, write_only=True)
    confirm_password = serializers.CharField(
        max_length=60, min_length=6, write_only=True
    )

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)



class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        required=True,
        write_only=True,
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
    )
    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
    )

    def validate(self, data):
        current_password = data.get("current_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        user = self.context["request"].user

        errors = {}

        if len(new_password) < 8 or len(confirm_password) < 8:
            errors[
                "detail"
            ] = "New password and confirm password should be at least 8 characters."
            raise serializers.ValidationError(errors)

        if not user.check_password(current_password):
            errors["detail"] = "password is incorrect."
            raise serializers.ValidationError(errors)

        if new_password != confirm_password:
            errors["detail"] = "New password and confirm password do not match."
            raise serializers.ValidationError(errors)

        if not new_password.strip():
            errors["detail"] = "New password cannot be empty."
            raise serializers.ValidationError(errors)

        try:
            valid_password(new_password, user=user)

        except ValidationError as e:
            errors["detail"] = e.messages[0]
            raise serializers.ValidationError(errors)

        return data