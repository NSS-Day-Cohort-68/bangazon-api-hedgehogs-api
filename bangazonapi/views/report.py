from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.shortcuts import render
from bangazonapi.models import Order
from rest_framework.decorators import action


class Reports(ViewSet):
    @action(detail=False, methods=["get"])
    def orders(self, request):
        orderstatus = self.request.query_params.get("status", None)

        if orderstatus == "complete":
            completed_orders = Order.objects.filter(payment_type__isnull=False)
            context = {
                "title": "Completed Orders",
                "heading": "Orders that include a payment type that is not null",
                "content": completed_orders,
            }
            return render(request, "reports.html", context)
        if orderstatus == "incomplete":
            pass
        else:
            return Response("", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["get"])
    def products(self, request):
        pass
