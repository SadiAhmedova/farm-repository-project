
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


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
    items = models.ManyToManyField(OrderItem, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    paid_amount = models.IntegerField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)

    @property
    def total_price(self):
        return sum(item.price * item.quantity for item in self.items.all())

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
        sellers = set(item.seller for item in self.items.all())

        for seller in sellers:
            seller_email = seller.email
            seller_items = self.items.filter(seller=seller)

            html_message = render_to_string('order_notification.html', {
                'order': self,
                'seller': seller,
                'items': seller_items,
            })

            email = EmailMessage(
                subject="New Order Notification - FarmApp",
                body=html_message,
                from_email=settings.EMAIL_HOST_USER,
                to=[seller_email],
            )
            email.content_subtype = "html"
            email.send()

        buyer_email = self.user.email
        buyer_message = render_to_string('order_confirmation.html', {'order': self})

        email = EmailMessage(
            subject="Order Confirmation - FarmApp",
            body=buyer_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[buyer_email],
        )
        email.content_subtype = "html"
        email.send()


    def save(self, *args, **kwargs):
        is_new = self.pk is None
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

