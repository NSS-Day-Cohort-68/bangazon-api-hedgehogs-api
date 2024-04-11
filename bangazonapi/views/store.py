from rest_framework.viewsets import ViewSet


class Stores(ViewSet):
    def create(self, request):
        """
        @api {POST} /stores POST new store
        @apiName CreateStore
        @apiGroup Store

        Args:
            request (_type_): _description_
        """
