from django.contrib import admin
from .models import Material, Product, ProductMaterial, Warehouse

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'code']
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['material', 'remainder', 'price']

class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ['product', 'material', 'quantity']


class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Material, MaterialAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductMaterial, ProductMaterialAdmin)
admin.site.register(Warehouse,WarehouseAdmin)

