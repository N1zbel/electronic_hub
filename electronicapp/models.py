from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=255, verbose_name='Поставщик')
    email = models.EmailField(verbose_name='Email')
    country = models.CharField(max_length=255, verbose_name='Страна')
    city = models.CharField(max_length=255, verbose_name='Город')
    street = models.CharField(max_length=255, verbose_name='Улица')
    house_number = models.CharField(max_length=10, verbose_name='Номер дома')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    @property
    def hierarchy_level(self):
        return 0  # Завод всегда находится на 0 уровне


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    model = models.CharField(max_length=255, null=True, blank=True, verbose_name='Модель продукта')
    release_date = models.DateField(null=True, blank=True, verbose_name='Дата релиза')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Поставщик')
    network_node = models.ForeignKey('NetworkNode', on_delete=models.CASCADE)


class NetworkNode(models.Model):
    FACTORY = 0
    RETAIL_NETWORK = 1
    INDIVIDUAL_ENTREPRENEUR = 2

    LEVEL_CHOICES = [
        (FACTORY, 'Factory'),
        (RETAIL_NETWORK, 'Retail Network'),
        (INDIVIDUAL_ENTREPRENEUR, 'Individual Entrepreneur'),
    ]

    name = models.CharField(max_length=255, verbose_name='Название Сети')
    contacts_email = models.EmailField(verbose_name='Контактный Емейл')
    contacts_country = models.CharField(max_length=255, verbose_name='Страна')
    contacts_city = models.CharField(max_length=255, verbose_name='Город')
    contacts_street = models.CharField(max_length=255, verbose_name='Улица')
    contacts_house_number = models.CharField(max_length=10, verbose_name='Номер дома')
    company_type = models.IntegerField(choices=LEVEL_CHOICES, verbose_name='Тип компании')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Поставщик')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    @property
    def hierarchy_level(self):
        if self.company_type == self.FACTORY:
            return 0
        if not self.supplier:
            return max(self.RETAIL_NETWORK, self.INDIVIDUAL_ENTREPRENEUR)
        return self.supplier.hierarchy_level + 1
