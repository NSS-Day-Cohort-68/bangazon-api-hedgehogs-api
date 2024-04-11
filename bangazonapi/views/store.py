from rest_framework.viewsets import ViewSet


class Stores(ViewSet):
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
