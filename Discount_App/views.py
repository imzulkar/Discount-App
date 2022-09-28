from django.db.models import Q
from django.shortcuts import render
from datetime import date, datetime
from rest_framework import generics, permissions as rest_permission, status

from Discount_App import serializers as ser, models as app_model
# Create your views here.
from rest_framework.response import Response


# ========== Discount section ==========
class DiscountView(generics.ListCreateAPIView):
    """
    Discount view
    > view data list (get)
    > Create request (post)
    > filter data using query peram
    > Valid discount list
    """
    permission_classes = [rest_permission.AllowAny]
    serializer_class = ser.DiscountSerializer

    def check_disocunt_validity(self):
        """
        to disable invalid discount if date or time expired
        this function should run using cron job

        """
        valid_discount = app_model.DiscountModel.objects.filter(is_valid=True)
        for check_valid in valid_discount:
            if check_valid.discount_category == 'date':
                if check_valid.end_date > datetime.today().date():
                    check_valid.is_valid = False
                    check_valid.save()
            else:
                if check_valid.end_time > datetime.today().time():
                    check_valid.is_valid = False
                    check_valid.save()

    def get_queryset(self):
        try:
            search = self.request.query_params.get('search')
            if search == 'valid':
                queryset = app_model.DiscountModel.objects.filter(is_valid=True)
            else:
                queryset = app_model.DiscountModel.objects.filter(Q(product_name__icontains=search) |
                                                                  Q(discount_category__icontains=search) |
                                                                  Q(discount_type__icontains=search))
        except:
            queryset = app_model.DiscountModel.objects.all()

        return queryset

    def create(self, request, *args, **kwargs):
        # method override
        set_status = True
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        discount_cat = serializer.validated_data.get('discount_category')
        # Checking category
        if discount_cat == 'date':
            start_date = serializer.validated_data.get('start_date')
            end_date = serializer.validated_data.get('end_date')
            if not (ser.DiscountSerializer.date_validate(self, start_date, end_date)):
                set_status = False
                return Response("Date must not be in the past.", status=status.HTTP_400_BAD_REQUEST)
        else:
            # if category time then check time is not null
            start_time = serializer.validated_data.get('start_time')
            end_time = serializer.validated_data.get('end_time')
            if not ser.DiscountSerializer.validate_time(self, start_time, end_time):
                set_status = False
                return Response("Time cant be null", status=status.HTTP_400_BAD_REQUEST)

        if set_status:
            # Check type value
            discount_type = serializer.validated_data.get('discount_type')
            discount_amount = serializer.validated_data.get('discount_amount')

            if ser.DiscountSerializer.validate_discount_percentage(self, discount_type, discount_amount):
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # if type percentage and value larger than 100 show error .
            return Response("Percentage cannot be larger than 100", status=status.HTTP_400_BAD_REQUEST)
        return Response("Error", status=status.HTTP_400_BAD_REQUEST)

    # def list(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(self.get_queryset(), many=True)
    #     response = serializer.data
    #     return Response(response, status=status.HTTP_200_OK)


class DiscountUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    Discount update view
    > discount update (put/patch)
    > discount delete (delete)
    > discount details (get)
    """
    permission_classes = [rest_permission.AllowAny]
    serializer_class = ser.DiscountSerializer
    queryset = app_model.DiscountModel.objects.all()
    lookup_field = 'id'


# ========== Category section ==========
class CategoryView(generics.ListCreateAPIView):
    """
        Category view
        > view data list (get)
        > Create request (post)
        > filter data using query peram
        """
    permission_classes = [rest_permission.AllowAny]
    serializer_class = ser.CategorySerializer

    def get_queryset(self):
        try:
            search = self.request.query_params.get('category')
            queryset = app_model.CategoryModel.objects.filter(category_name__icontains=search)
        except:
            queryset = app_model.CategoryModel.objects.all()

        return queryset


class CategoryUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    Category update view
    > Category update (put/patch)
    > Category delete (delete)
    > Category details (get)
    """
    permission_classes = [rest_permission.AllowAny]
    serializer_class = ser.CategorySerializer
    queryset = app_model.CategoryModel.objects.all()
    lookup_field = 'id'


# ========== Product section ==========
class ProductView(generics.ListCreateAPIView):
    """
        Discount view
        > view data list (get)
        > Create request (post)
        > filter data using query peram
    """
    permission_classes = [rest_permission.AllowAny]
    serializer_class = ser.ProductSerializer

    def get_queryset(self):
        try:
            search = self.request.query_params.get('product')
            queryset = app_model.ProductModel.objects.filter(product_name__icontains=search)
        except:
            queryset = app_model.ProductModel.objects.all()

        return queryset


class ProductUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
        Product update view
        > Product update (put/patch)
        > Product delete (delete)
        > Product details (get)
        """
    permission_classes = [rest_permission.AllowAny]
    serializer_class = ser.ProductSerializer
    queryset = app_model.ProductModel.objects.all()
    lookup_field = 'id'


# Add discount for all product
class AddDiscountForAllProductView(generics.CreateAPIView):
    permission_classes = [rest_permission.AllowAny]
    serializer_class = ser.AddDiscountForAllProductSerializer
    queryset = app_model.DiscountModel.objects.all()
    # lookup_field = 'id'
    def create(self, request, *args, **kwargs):
        products = app_model.ProductModel.objects.all()
        discount = app_model.DiscountModel.objects.get(discount_name=request.data.get('disocunt'))
        # print(request.data)
        for product in products:
            product.disocunt = discount
            product.save()

        return Response('Discount appied for all Products', status=status.HTTP_200_OK)



