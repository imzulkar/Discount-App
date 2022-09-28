from django.contrib import admin
from django.urls import path
from Discount_App import views as app_view

urlpatterns = [
    path('discount/', app_view.DiscountView.as_view(), name='create_discount'),
    # For create and list view of discount(post & get) and filter
    # for search use this url =>**** discount/?search=value ****
    # for valid discount use this url ==> **** discount/?search=valid ****

    path('discount/<int:id>/', app_view.DiscountUpdateView.as_view(), name='update_discount'),
    # for discount update/delete/details

    # ========Category section========
    path('category/', app_view.CategoryView.as_view(), name='categories'),
    # for create category and view list (post & get) and filter
    # for search use this url =>**** category/?category=value ****

    path('category/<int:id>/', app_view.CategoryUpdateView.as_view(), name='update_categories'),
    # for category update/delete/details

    # ========Product section========
    path('product/', app_view.ProductView.as_view(), name='products'),
    # for create product and view list (post & get) and filter
    # for search use this url =>**** product/?product=value ****

    path('product/<int:id>/', app_view.ProductUpdateView.as_view(), name='update_products'),
    # for product update/delete/details

    path('add-discount/', app_view.AddDiscountForAllProductView.as_view(), name='add_discount_for_all_product'),




]
