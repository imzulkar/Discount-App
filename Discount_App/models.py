from django.db import models


# Create your models here.
#========== Discount section ==========
class DiscountModel(models.Model):
    """
    Discount model
    """

    # Discount choices tupel
    DISCOUNT_CATEGORY = (
        ('date', 'Date'),
        ('time', 'Time'),
    )

    DISCOUNT_TYPE = (
        ('flat', 'Flat'),
        ('percentage', 'Percentage'),
    )

    discount_name = models.CharField(max_length=255, blank=False, null=False)
    discount_category = models.CharField(max_length=20, choices=DISCOUNT_CATEGORY, default='date', blank=False)
    # For Category time
    start_time = models.TimeField(default=None, null=True)
    end_time = models.TimeField(default=None, null=True)
    # For Category Date
    start_date = models.DateField(default=None, null=True)
    end_date = models.DateField(default=None, null=True)
    # Discount Field
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE, default='flat', blank=False)
    discount_amount = models.IntegerField(blank=False, default=0)

    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.discount_name

#========== Category section ==========
class CategoryModel(models.Model):
    category_name = models.CharField(max_length=100, blank=False, null=False)
    def __str__(self):
        return self.category_name

#========== Product section ==========
class ProductModel(models.Model):
    product_name = models.CharField(max_length=100, blank=False, null=False)
    category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, null=True, related_name='product_category')
    disocunt = models.ForeignKey(DiscountModel, on_delete=models.SET_NULL, null=True, related_name='product_discount')

    def __str__(self):
        return self.product_name



