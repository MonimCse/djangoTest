from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Choice, Question, CustomerInfo


class CustomerInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerInfo
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
            class Meta:
                model = Question
                fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
            class Meta:
                model = Choice
                fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, required=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        self.fields["username"].error_messages["required"] = u"username is required"
        self.fields["username"].error_messages["blank"] = u"username cannot be blank"
        self.fields["email"].error_messages["required"] = u"email is required"
        self.fields["email"].error_messages["blank"] = u"email cannot be blank"
        self.fields["password"].error_messages[
            "min_length"
        ] = u"password must be at least 8 chars"
