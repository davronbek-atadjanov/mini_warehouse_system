from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Material, ProductMaterial, Warehouse
from .serializers import ProductSerializer, MaterialSerializer, ProductMaterialSerializer, WarehouseSerializer
import json

class WarehouseAPIView(APIView):
    def post(self, request, format=None):
        products_data = request.data.get('products', None)
        if not products_data:
            return Response(
                {
                    "error": "No products data provided"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        data = []
        warehouse_remainders = {}

        for product_info in products_data:
            product_name = product_info.get('product_name')
            product_qty = product_info.get('quantity')
            if not product_name or not product_qty:
                return Response(
                    {
                        "error": "Product name and quantity are required"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                product = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                return Response(
                    {
                        "error": f"Product with name {product_name} does not exist"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            product_materials = ProductMaterial.objects.filter(product=product)
            materials_data = []
            for product_material in product_materials:
                material_data = Warehouse.objects.filter(material=product_material.material).first()
                warehouses = Warehouse.objects.filter(material=product_material.material).order_by("id")

                total_qty = product_material.quantity * product_qty
                for warehouse in warehouses:
                    warehouse_remainder = warehouse_remainders.get(
                        warehouse.id, warehouse.remainder
                    )
                    if warehouse_remainder == 0:
                        continue
                    if total_qty <= 0:
                        break
                    if warehouse_remainder >= total_qty:
                        warehouse_remainders[warehouse.id] = (warehouse_remainder - total_qty)
                        warehouse_data = WarehouseSerializer(warehouse).data
                        warehouse_data['warehouse_id'] = warehouse.id
                        warehouse_data['material_name'] = material_data.material.name
                        warehouse_data["qty"] = total_qty
                        warehouse_data['price'] = warehouse.price
                        total_qty = 0
                    else:
                        total_qty -= warehouse_remainder
                        warehouse_remainders[warehouse.id] = 0
                        warehouse_data = WarehouseSerializer(warehouse).data
                        warehouse_data['warehouse_id'] = warehouse.id
                        warehouse_data['material_name'] = material_data.material.name
                        warehouse_data["qty"] = warehouse_remainder
                        warehouse_data['price'] = warehouse.price

                    materials_data.append(warehouse_data)
                if total_qty > 0:
                    materials_data.append(
                        {
                            "warehouse_id": None,
                            "material_name": material_data.material.name,
                            "qty": total_qty,
                            "price": None,
                        }
                    )
            ordered_product_data = {
                "product_name": product.name,
                "product_qty":  product_qty,
                "product_materials": materials_data,
            }
            data.append(ordered_product_data)
        return Response({"result": data})
