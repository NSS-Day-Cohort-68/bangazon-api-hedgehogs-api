"""Customer order model"""

from django.db import models
from .customer import Customer
from .payment import Payment


class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.DO_NOTHING,
    )
    payment_type = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, null=True)
    created_date = models.DateField(
        default="0000-00-00",
    )

    @property
    def total_price(self):
        """total_price property of an order

        Returns:
            int -- Sum of the prices of all items in the order.
        """
        line_items = self.lineitems.all()
        total = sum(item.product.price for item in line_items)
        return total
