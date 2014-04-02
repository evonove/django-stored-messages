from rest_framework import serializers


class InboxSerializer(serializers.Serializer):
    id = serializers.CharField()
    message = serializers.CharField()
    level = serializers.IntegerField()
    date = serializers.DateTimeField()
