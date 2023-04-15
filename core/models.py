from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, null=True)
    gender = models.BooleanField(null=True)
    date = models.DateField(null=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateField(null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []


class Supplier(models.Model):
    supplier_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(User, related_name="create%(app_label)s_%(class)s_related", on_delete=models.PROTECT)
    update_date = models.DateTimeField(null=True)
    update_by = models.ForeignKey(User, related_name="update%(app_label)s_%(class)s_related", on_delete=models.PROTECT)
    
    def __str__(self):
        return self.supplier_name

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(User, related_name="create%(app_label)s_%(class)s_related", on_delete=models.PROTECT)
    update_date = models.DateTimeField(null=True)
    update_by = models.ForeignKey(User, related_name='update%(app_label)s_%(class)s_related', on_delete=models.PROTECT)

    def __str__(self):
        return self.category_name 
    
class Role(models.Model):
    role_name = models.CharField(max_length=50, null=True)

class User_role(models.Model):
    role = models.ForeignKey(Role, related_name="role%(app_label)s_%(class)s_related", on_delete=models.PROTECT)
    user = models.ForeignKey(User, related_name="user%(app_label)s_%(class)s_related", on_delete=models.PROTECT)

class Branch(models.Model):
    branch_name = models.CharField(max_length=50, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(User, related_name="create%(app_label)s_%(class)s_related", on_delete=models.PROTECT)
    update_date = models.DateTimeField(null=True)
    update_by = models.ForeignKey(User, related_name="update%(app_label)s_%(class)s_related", on_delete=models.PROTECT)

class Product(models.Model):
    def upload_to(instance, filename):
        return 'Image/product_{0}/{1}'.format(instance.id, filename)
    
    branch = models.ForeignKey(Branch, related_name="branch%(app_label)s_%(class)s_related", on_delete=models.PROTECT)
    category = models.ForeignKey(Category, related_name="category%(app_label)s_%(class)s_related", on_delete=models.PROTECT)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField(null=True)
    price = models.FloatField()
    sale = models.FloatField(null=True)
    rate = models.FloatField(null=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to=upload_to, null=True)
    content = models.CharField(max_length=255)
    status = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(User, related_name="create%(app_label)s_%(class)s_related", on_delete=models.PROTECT)
    update_date = models.DateTimeField(auto_now_add=True)
    update_by = models.ForeignKey(User, related_name="update%(app_label)s_%(class)s_related", on_delete=models.PROTECT)

    def __str__(self):
        return self.product_name

class Product_Detail(models.Model):
    product = models.ForeignKey(Product, related_name="product%(app_label)s_%(class)s_related", on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=10)


class Ticket_import(models.Model):
    supplier = models.ForeignKey(Supplier, related_name="supplier%(app_label)s_%(class)s_related", on_delete=models.PROTECT)
    code = models.CharField(max_length=20)
    create_date = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(User, related_name="create%(app_label)s_%(class)s_related", on_delete=models.PROTECT)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.code

class Ticket_Import_Detail(models.Model):
    ticket_import = models.ForeignKey(Ticket_import, related_name="ticketimport%(app_label)s_%(class)s_related", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="product%(app_label)s_%(class)s_related", on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    
class Orders(models.Model):
    order_code = models.CharField(max_length=100)
    customer_name = models.ForeignKey(User, related_name="customername%(app_label)s_%(class)s_related", on_delete=models.PROTECT)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255)
    total_price = models.FloatField()
    status = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True)

class Orders_Item(models.Model):
    order = models.ForeignKey(Orders, related_name="order%(app_label)s_%(class)s_related", on_delete=models.PROTECT)
    product = models.ForeignKey(Product, related_name="product%(app_label)s_%(class)s_related", on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.FloatField()
    
class Size(models.Model):
    size_name = models.CharField(max_length=255)

class Color(models.Model):
    color_name = models.CharField(max_length=255)