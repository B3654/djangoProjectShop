from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                        args=[self.slug])


    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)  # slug : Алиас продукта(его URL).
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)  # Необязательное описание для продукта.
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.Field(blank=True)  # Это поле PositiveIntegerField для хранения остатков данного продукта.
    available = models.BooleanField(default=True)  # Это булево значение, указывающее, доступен ли продукт или нет. Позволяет включить/отключить продукт в каталоге.
    created = models.DateTimeField(auto_now_add=True)  # Это поле хранит дату когда был создан объект.
    updated = models.DateTimeField(auto_now=True)  # В этом поле хранится время последнего обновления объекта.

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                        args=[self.id, self.slug])

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name
