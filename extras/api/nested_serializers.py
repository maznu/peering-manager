from rest_framework import serializers

from extras.models import IXAPI, JobResult, Webhook
from peering_manager.api import WritableNestedSerializer
from users.api.nested_serializers import NestedUserSerializer


class NestedIXAPISerializer(WritableNestedSerializer):
    class Meta:
        model = IXAPI
        fields = ["id", "display", "name", "url"]


class NestedJobResultSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="extras-api:jobresult-detail")
    user = NestedUserSerializer(read_only=True)

    class Meta:
        model = JobResult
        fields = ["url", "created", "completed", "user", "status"]


class NestedWebhookSerializer(WritableNestedSerializer):
    class Meta:
        model = Webhook
        fields = ["id", "name", "url"]
