from care.emr.api.viewsets.base import EMRBaseViewSet, EMRListMixin
from care.security.authorization import AuthorizationController
from pydantic import BaseModel
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from care_notifications.models.web_push_subscription import WebPushSubscription
from care_notifications.resources.web_push_subscription.spec import (
    WebPushSubscriptionListSpec,
)
from care_notifications.settings import plugin_settings


class PushSubscriptionKeys(BaseModel):
    p256dh: str
    auth: str


class WebPushSubscribeRequest(BaseModel):
    endpoint: str
    keys: PushSubscriptionKeys


class WebPushUnsubscribeRequest(BaseModel):
    endpoint: str


class WebPushSubscriptionViewSet(EMRListMixin, EMRBaseViewSet):
    database_model = WebPushSubscription
    pydantic_model = WebPushSubscriptionListSpec
    pydantic_read_model = WebPushSubscriptionListSpec

    def get_queryset(self):
        queryset = super().get_queryset()
        if AuthorizationController.call("can_list_all_notifications", self.request.user):
            return queryset
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        payload = WebPushSubscribeRequest.model_validate(request.data)

        subscription, _ = WebPushSubscription.objects.update_or_create(
            endpoint=payload.endpoint,
            defaults={
                "user": request.user,
                "p256dh": payload.keys.p256dh,
                "auth": payload.keys.auth,
            },
        )
        return Response(
            WebPushSubscriptionListSpec.serialize(subscription).to_json(),
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["POST"])
    def unsubscribe(self, request, *args, **kwargs):
        payload = WebPushUnsubscribeRequest.model_validate(request.data)
        deleted, _ = self.get_queryset().filter(endpoint=payload.endpoint).delete()
        return Response({"deleted": deleted})

    @action(detail=False, methods=["GET"], url_path="vapid_public_key")
    def vapid_public_key(self, request, *args, **kwargs):
        return Response({"public_key": plugin_settings.WEBPUSH_VAPID_PUBLIC_KEY})
