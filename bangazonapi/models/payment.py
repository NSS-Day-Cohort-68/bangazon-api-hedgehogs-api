from django.db import models
from .customer import Customer
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE


class Payment(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE
    merchant_name = models.CharField(
        max_length=25,
    )
    account_number = models.CharField(max_length=25)
    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, related_name="payment_types"
    )
    expiration_date = models.DateField(
        default="0000-00-00",
    )
    create_date = models.DateField(
        auto_now_add=True,
    )

    @property
    def obscured_num(self):
        # Replaces all but the last 3 digits with asterisks
        if self.account_number is not None:
            obscured_digits = "*" * (len(self.account_number) - 3)
            visible_digits = self.account_number[-3:]
            return obscured_digits + visible_digits
        else:
            return None
