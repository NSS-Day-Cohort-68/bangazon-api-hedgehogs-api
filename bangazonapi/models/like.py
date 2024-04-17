from django.db import models
from .customer import Customer
from .product import Product


class Like(models.Model):
    """Model representing likes on products"""

    customer = models.ForeignKey(
        Customer, related_name="likes", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, related_name="likes", on_delete=models.CASCADE)
