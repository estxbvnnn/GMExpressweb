from django.core.management.base import BaseCommand
from catalogo.models import CATALOGOS
from productos.models import CategoriaProducto, Producto
from servicios.models import TipoServicio, Servicio

DEFAULT_PRECIO = 0
DEFAULT_STOCK = 0
DEFAULT_UNIDAD = "unidad"
DEFAULT_ESTADO_SERVICIO = "activo"


class Command(BaseCommand):
    help = "Importa el catálogo estático (categorías, productos y servicios) a la base de datos."

    def handle(self, *args, **options):
        created = {"categorias": 0, "productos": 0, "tipos": 0, "servicios": 0}
        updated = {"categorias": 0, "productos": 0, "tipos": 0, "servicios": 0}

        for cat in CATALOGOS:
            cat_obj, cat_created = CategoriaProducto.objects.update_or_create(
                nombre=cat["nombre"],
                defaults={"descripcion": cat.get("descripcion", "")},
            )
            created["categorias"] += int(cat_created)
            updated["categorias"] += int(not cat_created)

            tipo_obj, tipo_created = TipoServicio.objects.update_or_create(
                nombre=cat["nombre"],
                defaults={"descripcion": cat.get("descripcion", "")},
            )
            created["tipos"] += int(tipo_created)
            updated["tipos"] += int(not tipo_created)

            for prod in cat.get("productos", []):
                desc = prod.get("breve", "")
                if prod.get("ingredientes"):
                    desc += f"\nIngredientes: {prod['ingredientes']}"
                if prod.get("entrega"):
                    desc += f"\nEntrega: {prod['entrega']}"

                prod_obj, prod_created = Producto.objects.update_or_create(
                    nombre=prod["nombre"],
                    categoria=cat_obj,
                    defaults={
                        "precio": DEFAULT_PRECIO,
                        "descripcion": desc,
                        "stock": DEFAULT_STOCK,
                        "unidad_medida": DEFAULT_UNIDAD,
                    },
                )
                created["productos"] += int(prod_created)
                updated["productos"] += int(not prod_created)

                srv_obj, srv_created = Servicio.objects.update_or_create(
                    nombre=prod["nombre"],
                    tipo=tipo_obj,
                    defaults={
                        "precio": DEFAULT_PRECIO,
                        "descripcion": desc,
                        "estado": DEFAULT_ESTADO_SERVICIO,
                    },
                )
                created["servicios"] += int(srv_created)
                updated["servicios"] += int(not srv_created)

        self.stdout.write(self.style.SUCCESS("Importación finalizada"))
        self.stdout.write(
            f"Categorías: {created['categorias']} creadas, {updated['categorias']} actualizadas\n"
            f"Productos: {created['productos']} creados, {updated['productos']} actualizados\n"
            f"Tipos servicio: {created['tipos']} creados, {updated['tipos']} actualizados\n"
            f"Servicios: {created['servicios']} creados, {updated['servicios']} actualizados"
        )
