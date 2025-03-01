
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

from farm_app.catalog.models import VegetableAndFruit, DairyProduct, Nut, AnimalProduct

from farm_app.accounts.validators import validate_ten_digits

UserModel = 'accounts.FarmerUser'


class Order(models.Model):
    ORDERED = 'Ordered'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'

    STATUS_CHOICES = (
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered')
    )

    user = models.ForeignKey(UserModel, related_name='orders', blank=True, null=True,
                             on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, validators=[validate_ten_digits], help_text="Enter a valid 10-digit phone number.")

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    paid_amount = models.IntegerField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)

    def update_status(self):
        three_days_ago = timezone.now() - timezone.timedelta(days=3)
        seven_days_ago = timezone.now() - timezone.timedelta(days=7)
        if self.created_at < three_days_ago and self.status == 'Ordered':
            self.status = Order.SHIPPED
            self.save()
        if self.created_at < seven_days_ago and self.status == 'Shipped':
            self.status = Order.DELIVERED
            self.save()

    def send_order_emails(self):
        seller_orders = {}
        for item in self.items.all():
            seller = None
            if item.fruit:
                seller = item.fruit.user
            elif item.dairy:
                seller = item.dairy.user
            elif item.meat:
                seller = item.meat.user
            elif item.nut:
                seller = item.nut.user

            if seller:
                if seller.email not in seller_orders:
                    seller_orders[seller.email] = []
                seller_orders[seller.email].append(f"{item.get_name()} - {item.quantity} pcs")

        # Send email to each seller
        for seller_email, products in seller_orders.items():
            subject = "New Order Notification - FarmApp"
            message = f"Dear Seller,\n\nYou have a new order for the following products:\n\n"
            message += "\n".join(products)
            message += "\n\nPlease prepare these products for shipping.\n\nFarmApp Team"

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [seller_email])

        # Send confirmation email to buyer
        buyer_subject = "Order Confirmation - FarmApp"
        buyer_message = f"Dear {self.first_name},\n\nThank you for your order! Here are your order details:\n\n"
        for item in self.items.all():
            buyer_message += f"- {item.get_name()} - {item.quantity} pcs\n"

        buyer_message += "\nYour order will be processed soon.\n\nFarmApp Team"
        send_mail(buyer_subject, buyer_message, settings.DEFAULT_FROM_EMAIL, [self.email])

    def save(self, *args, **kwargs):
        """Override save to send emails when a new order is placed."""
        is_new = self.pk is None  # Check if this is a new order
        super().save(*args, **kwargs)
        if is_new:
            self.send_order_emails()






    class Meta:
        ordering = ('-created_at',)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    fruit = models.ForeignKey(VegetableAndFruit, related_name='VegetableAndFruit', on_delete=models.CASCADE, null=True,
                              blank=True)
    dairy = models.ForeignKey(DairyProduct, related_name='DairyProduct', on_delete=models.CASCADE, null=True,
                              blank=True)
    meat = models.ForeignKey(AnimalProduct, related_name='AnimalProduct', on_delete=models.CASCADE, null=True,
                             blank=True)
    nut = models.ForeignKey(Nut, related_name='Nut', on_delete=models.CASCADE, null=True, blank=True)

    price = models.FloatField()
    quantity = models.IntegerField(default=1)



    def get_name(self):
        if self.fruit:
            return f'{self.fruit.name}'
        elif self.dairy:
            return f'{self.dairy.name} {self.dairy.percent}%'
        if self.meat:
            return f'{self.meat.name} {self.meat.type}'
        if self.nut:
            return f'{self.nut.type} {self.nut.name}'

