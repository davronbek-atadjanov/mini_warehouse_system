from rest_framework import serializers
from .models import Product, Material, ProductMaterial, Warehouse

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['price']

class ProductMaterialSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(many=True, read_only=True)
    class Meta:
        model = ProductMaterial
        fields = ['material', 'quantity', 'warehouse']

class ProductSerializer(serializers.ModelSerializer):
    product_materials = ProductMaterialSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['product_materials']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['name']