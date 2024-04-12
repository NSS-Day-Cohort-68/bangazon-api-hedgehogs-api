from rest_framework.viewsets import ViewSet
from django.http import HttpResponseServerError
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Store, Customer
from rest_framework.exceptions import PermissionDenied


class StoreSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for stores"""

    class Meta:
        model = Store
        url = serializers.HyperlinkedIdentityField(view_name="store", lookup_field="id")
        fields = (
            "id",
            "url",
            "name",
            "description",
            "seller",
            "created_date",
        )


class Stores(ViewSet):
    def retrieve(self, request, pk=None):
        try:
            store = Store.objects.get(pk=pk)
            serializer = StoreSerializer(store, context={"request": request})
            return Response(serializer.data)

        except Store.DoesNotExist:
            return Response(
                {"message": "The requested store does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def list(self, request):
        store = Store.objects.all()
        serializer = StoreSerializer(store, context={"request": request}, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        @api {POST} /stores POST new store
        @apiName CreateStore
        @apiGroup Store

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611

        @apiParam {String} name Short form name of store
        @apiParam {String} description Long form description of store
            {
                "name": "Papa's General Store",
                "description": "tools and socks"
            }

        @apiSuccess (200) {Object} store Created store
        @apiSuccess (200) {id} store.id Store Id
        @apiSuccess (200) {String} store.name Short form name of store
        @apiSuccess (200) {String} store.description Long form description of store
        @apiSuccess (200) {Number} store.seller Customer id of the user creating the store
        @apiSuccess (200) {Date} store.created_date Date store was created
        @apiSuccessExample {json} Success
            {
                "id": 1,
                "url": "http://localhost:8000/stores/1",
                "name": "Papa's General Store",
                "description": "tools and socks",
                "created_date": "2020-10-23",
                "seller": "http://localhost:8000/customers/5"
            }
        """
        # Check if user currently has a store
        existing_store = Store.objects.filter(seller__user=request.auth.user).first()
        if existing_store:
            raise PermissionDenied("Aw nuts! You already have a store!")

        # If the user doesn't have a store, create a new store
        new_store = Store()
        new_store.name = request.data["name"]
        new_store.description = request.data["description"]
        customer = Customer.objects.get(user=request.auth.user)
        new_store.seller = customer
        new_store.save()

        serializer = StoreSerializer(new_store, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            store = Store.objects.get(pk=pk)
            store.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Store.DoesNotExist as ex:
            return Response(
                {"This store does not exist.": ex.args[0]},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
