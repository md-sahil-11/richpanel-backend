from django.conf import settings
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from subscription.models import Plan, SubscriptionHistory
from .serializers import PlanSerializer, SubscriptionHistorySerializer
from user.models import User

import stripe
import djstripe
import json


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = PlanSerializer

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscribe(self, request, price_id=None):
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        data = json.loads(request.body)
        payment_method = data['payment_method_id']
        price_id = data['price_id']
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

        payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
        djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)
        
        if not SubscriptionHistory.objects.filter(user=request.user).exists():
            SubscriptionHistory.objects.filter(user=request.user).update(
                plan=Plan.objects.filter(price_id=price_id).first()
            )
        else:
            SubscriptionHistory.objects.create(
                user=request.user,
                plan=Plan.objects.filter(price_id=price_id).first()
            )

        try:
            customer = stripe.Customer.create(
                payment_method=payment_method,
                email=request.user.email,
                invoice_settings={
                    'default_payment_method': payment_method
                }
            )

            djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)
            request.user.customer = djstripe_customer

            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[
                    {
                        "price": price_id,
                    },
                ],
                expand=["latest_invoice.payment_intent"],
                payment_settings={
                    'payment_method_types': ['card'],
                },
            )

            djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

            request.user.subscription = djstripe_subscription
            request.user.save()

            return Response(subscription)
        except Exception as e:
            return Response({'error': (e.args[0])}, status =403)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def cancel(self, request, *args, **kwargs):
        sub_id = request.user.subscription.id
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        
        SubscriptionHistory.objects.filter(user=request.user).update(
            is_cancelled=True
        )

        try:
            stripe.Subscription.delete(sub_id)
        except Exception as e:
            return Response({'error': (e.args[0])}, status =403)

        return Response("done")


class SubscriptionHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubscriptionHistorySerializer

    def get_queryset(self):
        return SubscriptionHistory.objects.filter(
            user=self.request.user
        )



