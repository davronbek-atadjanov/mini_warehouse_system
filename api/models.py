from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=150)
    quantity = models.IntegerField(default=0)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Material(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_materials")
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField()


class Warehouse(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    remainder = models.FloatField()
    price = models.FloatField()

