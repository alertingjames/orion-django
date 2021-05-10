from rest_framework import serializers
from .models import Member, Store, Brand, Product, ProductPicture, Advertisement, Rating, ProductLike, Phone, Address, Coupon, UsedCoupon, Order, OrderItem, Notification, Paid, DriverLocation, PreparedOrder
from .models import PreparedOrderItem

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'name', 'email', 'password', 'phone_number', 'picture_url', 'address', 'country', 'area', 'street', 'house', 'latitude', 'longitude', 'role', 'registered_time', 'stores', 'status', 'fcm_token')

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'member_id', 'name', 'logo_url', 'phone_number', 'address', 'delivery_price', 'delivery_days', 'ratings', 'reviews', 'registered_time', 'status', 'latitude', 'longitude')

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'member_id', 'store_id', 'name', 'category', 'logo_url', 'registered_time', 'status')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'store_id', 'member_id', 'brand_id', 'name', 'picture_url', 'category', 'subcategory', 'gender', 'gender_key', 'price', 'new_price', 'unit', 'description', 'registered_time', 'status', 'likes', 'isLiked', 'ratings', 'delivery_price', 'delivery_days', 'brand_name', 'brand_logo')

class ProductPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPicture
        fields = ('id', 'product_id', 'picture_url')

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('id', 'store_id', 'store_name', 'picture_url')

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'store_id', 'product_id', 'member_id', 'member_name', 'member_photo', 'rating', 'date_time', 'subject', 'description')

class ProductLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLike
        fields = ('id', 'product_id', 'member_id', 'liked_time')


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('id', 'member_id', 'phone_number', 'status')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'member_id', 'address', 'area', 'street', 'house', 'status', 'latitude', 'longitude')

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ('id', 'discount', 'expire_time', 'status')

class UsedCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsedCoupon
        fields = ('id', 'member_id', 'coupon_id', 'discount', 'expire_time', 'option', 'status')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'member_id', 'orderID', 'price', 'unit', 'shipping', 'date_time', 'email', 'address', 'address_line', 'phone_number', 'status', 'discount', 'latitude', 'longitude')

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order_id', 'member_id', 'vendor_id', 'store_id', 'store_name', 'product_id', 'product_name', 'category', 'subcategory', 'gender', 'gender_key', 'price', 'unit', 'quantity', 'date_time', 'picture_url', 'delivery_days', 'delivery_price', 'status', 'orderID', 'contact', 'discount', 'status2', 'status_time', 'paid_amount', 'paid_time', 'payment_status', 'paid_id', 'address', 'address_line', 'latitude', 'longitude')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'receiver_id', 'message', 'sender_id', 'sender_name', 'sender_email', 'sender_phone', 'date_time', 'image_message')


class PaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paid
        fields = ('id', 'member_id', 'vendor_id', 'store_id', 'order_id', 'orderID', 'paid_amount', 'paid_time', 'payment_status', 'charge_id', 'transfer_id', 'items', 'store_name')


class DriverLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLocation
        fields = ('id', 'name', 'address', 'country', 'area', 'street', 'house', 'latitude', 'longitude', 'status')


class PreparedOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreparedOrder
        fields = ('id', 'member_id', 'driver_id', 'items_str', 'date_time', 'status')


class PreparedOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreparedOrderItem
        fields = ('id', 'porder_id', 'item_id', 'status')




























































