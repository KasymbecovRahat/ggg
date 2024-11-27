from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    phonenumber = PhoneNumberField(null=True, blank=True)
    ROLES_STATUS = (
        ('Владелец', 'Владелец'),
        ('Клиент', 'Клиент'),
        ('Курьер', 'Курьер')
    )
    user_role = models.CharField(max_length=12, choices=ROLES_STATUS, default='Клиент')


class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.category_name


class Store(models.Model):
    store_name = models.CharField(max_length=20)
    store_description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store_image = models.ImageField(upload_to='store_photo')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_store')
    address = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.store_name}, {self.address}'


class ContactInfo(models.Model):
    contact_info = PhoneNumberField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='contacts')

    def __str__(self):
        return f'{self.store} {self.contact_info}'


class Product(models.Model):
    product_name = models.CharField(max_length=30)
    product_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product')
    product_photo = models.ImageField(upload_to='product_image/')
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')


    def __str__(self):
        return f'{self.product_name} {self.store}'


class ProductCombo(models.Model):
    combo_name = models.CharField(max_length=30)
    combo_description = models.TextField()
    combo_price = models.DecimalField(max_digits=10, decimal_places=2)
    combo_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_combo')
    combo_photo = models.ImageField(upload_to='combo_image/')

    def __str__(self):
        return f'{self.combo_name} {self.combo_store}'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart')
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class CarItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity


class Orders(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders_product')
    client_orders = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_orders')
    courier_orders = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courier_orders')
    ORDER_STATUS = (
        ('Ожидает  обработки', 'Ожидает  обработки'),
        ('В процессе доставки', 'В процессе доставки'),
        ('Доставлен', 'Доставлен'),
        ('Отменен', 'Отменен')
    )
    orders_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Ожидает  обработки')
    orders_created = models.DateTimeField(auto_now_add=True)
    delivery_address = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.product} {self.client_orders} {self.orders_status}'


class Courier(models.Model):
    users = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    COURIER_STATUS = (
        ('Доступен', 'Доступен'),
        ('Занят', 'Занят')
    )
    status_courier = models.CharField(max_length=12, choices=COURIER_STATUS)
    current_orders = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='courier')

    def __str__(self):
        return f'{self.users}'


class StoreReview(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='review_store')
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='Рейтинг')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client} {self.rating} {self.comment}'


class CourierReview(models.Model):
    client_review = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_review')
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courier_review')
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='Рейтинг')

    def __str__(self):
        return f'{self.courier} {self.rating}'
