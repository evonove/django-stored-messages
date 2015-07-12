from rest_framework import serializers


class InboxSerializer(serializers.Serializer):
    id = serializers.CharField()
    message = serializers.CharField()
    level = serializers.IntegerField()
    tags = serializers.CharField()
    date = serializers.DateTimeField(format=None)
    url = serializers.URLField(required=False)
