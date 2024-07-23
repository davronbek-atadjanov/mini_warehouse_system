from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .serializers import ProductSerializer, WarehouseSerializer
from .models import Product, Warehouse, ProductMaterial

class WarehouseListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        data = []
        warehouse_remainders = {}
        for product in queryset:
            product_materials = ProductMaterial.objects.filter(product=product)
            materials_data = []
            for product_material in product_materials:
                material_data = Warehouse.objects.filter(material=product_material.material).first()
                warehouses = Warehouse.objects.filter(material=product_material.material).order_by("id")

                total_qty = product_material.quantity * product.quantity
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
                "product_qty": product.quantity,
                "product_materials": materials_data,
            }
            data.append(ordered_product_data)
        return Response({"result": data})
