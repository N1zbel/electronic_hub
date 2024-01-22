from django.contrib import admin

from electronicapp.models import Product, NetworkNode, Supplier


class ProductInline(admin.TabularInline):
    model = Product


class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'contacts_email', 'get_hierarchy_level']
    inlines = [ProductInline]

    def get_hierarchy_level(self, obj):
        return obj.hierarchy_level


admin.site.register(NetworkNode, NetworkNodeAdmin)
admin.site.register(Supplier)
admin.site.register(Product)
