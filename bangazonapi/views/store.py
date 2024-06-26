from rest_framework.viewsets import ViewSet
from django.http import HttpResponseServerError
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Store, Customer, Product, Favorite
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .product import ProductSerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Users

    Arguments:
        serializers
    """

    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(view_name="user", lookup_field="id")
        fields = ("id", "url", "username", "first_name", "last_name")


class SellerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for sellers"""

    user = UserSerializer(many=False)

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name="customer", lookup_field="id"
        )
        fields = ("id", "url", "user")
        depth = 1


class StoreSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for stores"""

    seller = SellerSerializer(many=False)
    products = ProductSerializer(many=True)

    class Meta:
        model = Store
        url = serializers.HyperlinkedIdentityField(view_name="store", lookup_field="id")
        fields = (
            "id",
            "url",
            "name",
            "description",
            "is_favorite",
            "products",
            "seller",
            "created_date",
            
        )
        depth = 1



class Stores(ViewSet):
    def retrieve(self, request, pk=None):
        """
        @api {GET} /stores/:id GET store matching primary key
        @apiName GetStore
        @apiGroup Store

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611

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
        try:
            customer = Customer.objects.get(user=request.auth.user)
            store = Store.objects.get(pk=pk)
            is_favorite = Favorite.objects.filter(customer=customer, seller=store.seller)
            if len(is_favorite):
                store.is_favorite = True
            else:
                store.is_favorite = False
            store.products = Product.objects.filter(customer=store.seller)
            serializer = StoreSerializer(store, context={"request": request})
            return Response(serializer.data)

        except Store.DoesNotExist:
            return Response(
                {"message": "The requested store does not exist. Kinda spooky..."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def list(self, request):
        """
        @api {GET} /stores GET all stores
        @apiName GetStores
        @apiGroup Store

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611

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
        all_stores = Store.objects.all()
        for store in all_stores:
            store.products = Product.objects.filter(customer=store.seller)
        serializer = StoreSerializer(
            all_stores, context={"request": request}, many=True
        )
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
        existing_store = Store.objects.filter(seller__user=request.auth.user)
        if existing_store:
            raise PermissionDenied("Aw nuts! You already have a store!")

        # If the user doesn't have a store, create a new store
        new_store = Store()
        new_store.name = request.data["name"]
        new_store.description = request.data["description"]
        customer = Customer.objects.get(user=request.auth.user)
        new_store.seller = customer
        new_store.products = Product.objects.filter(customer=new_store.seller)
        new_store.save()

        serializer = StoreSerializer(new_store, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """
        @api {DELETE} /stores/:id DELETE store matching id
        @apiName RemoveStore
        @apiGroup Store

        @apiParam {id} id Store Id to be deleted
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        try:
            store = Store.objects.get(pk=pk)
            store.delete()

            return Response(
                "Your store was successfully destroyed!",
                status=status.HTTP_204_NO_CONTENT,
            )

        except Store.DoesNotExist as ex:
            return Response(
                {"This store does not exist.": ex.args[0]},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as ex:
            return Response(
                {"An unexpected error occurred": ex.args[0]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        """
        @api {PUT} /stores/:id PUT edit store data
        @apiName EditStore
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

        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        try:
            store = Store.objects.get(pk=pk)
        except Store.DoesNotExist:
            return Response(
                {"message": "This store does not exist o.o"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if the user is the owner of the store
        if store.seller.user != request.auth.user:
            raise PermissionDenied("Smile! You're on camera! This is not your store!")

        # Update store data based on request data
        # If the key "name" exists in the request.data, its value is returned.
        # If not, it returns the default value, which is store.name.
        store.name = request.data.get("name", store.name)
        store.description = request.data.get("description", store.description)
        store.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
