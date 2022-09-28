from django.contrib import admin
from Discount_App import models
# Register your models here.
admin.site.register(models.DiscountModel)
admin.site.register(models.CategoryModel)
admin.site.register(models.ProductModel)