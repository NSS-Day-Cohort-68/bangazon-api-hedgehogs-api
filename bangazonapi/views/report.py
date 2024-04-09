from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.shortcuts import render
from bangazonapi.models import Order
from rest_framework.decorators import action
from bangazonapi.models import Product

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
            return render(request, "order_reports.html", context)
        if orderstatus == "incomplete":
            incomplete_orders = Order.objects.filter(payment_type__isnull=True)
            context = {
                "title": "Incomplete Orders",
                "heading": "Orders that include a payment type that is null",
                "content": incomplete_orders,
            }
            return render(request, "order_reports.html", context)
        else:
            return Response("", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["get"])
    def expensiveproducts(self, request):
        
        expensiveproducts = Product.objects.filter(price__gte=1000)
        context = {
            "title": "Expensive Products",
            "heading": "Products that are greater than or equal to $1000",
            "content": expensiveproducts,
        }
        return render(request, "products.html", context)
    
    @action(detail=False, methods=["get"])
    def inexpensiveproducts(self, request):
        
        inexpensiveproducts = Product.objects.filter(price__lte=999)
        context = {
            "title": "Inexpensive Products",
            "heading": "Products that are less than or equal to $1000",
            "content": inexpensiveproducts,
        }
        return render(request, "products.html", context)
