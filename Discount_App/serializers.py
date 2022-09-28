# from django.utils.datetime_safe import datetime
from builtins import ValueError
from datetime import datetime,date
from rest_framework import serializers
# import Discount app model
from Discount_App import models as app_model

#========== Discount section ==========
class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = app_model.DiscountModel
        fields= '__all__'
        extra_kwargs ={
            'is_valid': {'read_only':True}
        }


    # below functions can be defined in view as well
    # and all this function can be implemented in serializer also

    def date_validate(self, date1, date2):
        """Date Validate fucntion"""
        current_date = datetime.today().date()
        if date1 >= current_date and date2 >= current_date:
            return True
        return False


    def validate_time(self, time1, time2):
        """Time Validate fucntion"""
        if time1 and time2:
            return True
        return False

    def validate_discount_percentage(self, type , value):
        """Discount percentage validate"""
        if type == 'percentage':
            return (value < 100)
        return True




    # validating before post request

    # def create(self, validated_data):
    #     discount_cat = validated_data['discount_category']
    #     if discount_cat == 'date':
    #         start_date = validated_data['start_date']
    #         end_date = validated_data['end_date']
    #         if start_date and end_date and self.date_validate(start_date,end_date):
    #             return app_model.DiscountModel.objects.create(**validated_data)
    #         return ValueError


#========== Category section ==========
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = app_model.CategoryModel
        fields = '__all__'

        
class ProductSerializer(serializers.ModelSerializer):
    disocunt_detail = DiscountSerializer(read_only=True, source='disocunt')
    category_detail = CategorySerializer(read_only=True, source='category')
    class Meta:
        model = app_model.ProductModel
        fields = '__all__'
        extra_fields =  ['disocunt_detail','category_detail']
        # depth = 1

    def to_representation(self, instance):
        data = super(ProductSerializer, self).to_representation(instance)
        data.pop('disocunt')
        data.pop('category')
        return data


# update discount for all
class AddDiscountForAllProductSerializer(serializers.ModelSerializer):
    disocunt = serializers.SlugRelatedField(queryset=app_model.DiscountModel.objects.all(), slug_field='discount_name')
    class Meta:
        model = app_model.DiscountModel
        fields = ['disocunt']
        # extra_fields = ['disocunt']