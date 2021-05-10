from django.db import models

# Create your models here.

class Member(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    picture_url = models.CharField(max_length=1000)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    role = models.CharField(max_length=30)
    registered_time = models.CharField(max_length=50)
    stores = models.CharField(max_length=11)
    status = models.CharField(max_length=20)
    fcm_token = models.CharField(max_length=2000)

class Store(models.Model):
    member_id = models.CharField(max_length=11)
    name = models.CharField(max_length=50)
    logo_url = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    delivery_price = models.CharField(max_length=11)
    delivery_days = models.CharField(max_length=11)
    ratings = models.CharField(max_length=11)
    reviews = models.CharField(max_length=11)
    registered_time = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)

class Brand(models.Model):
    member_id = models.CharField(max_length=11)
    store_id = models.CharField(max_length=11)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    logo_url = models.CharField(max_length=1000)
    registered_time = models.CharField(max_length=50)
    status = models.CharField(max_length=20)


class Product(models.Model):
    store_id = models.CharField(max_length=11)
    member_id = models.CharField(max_length=11)
    brand_id = models.CharField(max_length=11)
    name = models.CharField(max_length=50)
    picture_url = models.CharField(max_length=1000)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)
    gender_key = models.CharField(max_length=100)
    price = models.CharField(max_length=11)
    new_price = models.CharField(max_length=11)
    unit = models.CharField(max_length=20)
    description = models.CharField(max_length=2000)
    registered_time = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    likes = models.CharField(max_length=11)
    isLiked = models.CharField(max_length=20)
    ratings = models.CharField(max_length=11)
    delivery_price = models.CharField(max_length=11)
    delivery_days = models.CharField(max_length=11)
    brand_name = models.CharField(max_length=100)
    brand_logo = models.CharField(max_length=1000)


class ProductPicture(models.Model):
    product_id = models.CharField(max_length=11)
    picture_url = models.CharField(max_length=1000)


class Payment(models.Model):
    member_id = models.CharField(max_length=11)
    bank_number = models.CharField(max_length=30)
    routing_number = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=30)
    state = models.CharField(max_length=50)
    ssn_last4 = models.CharField(max_length=30)
    birth_date = models.CharField(max_length=11)
    birth_month = models.CharField(max_length=11)
    birth_year = models.CharField(max_length=11)
    registered_time = models.CharField(max_length=50)
    acc_id = models.CharField(max_length=500)
    status = models.CharField(max_length=20)


class Advertisement(models.Model):
    store_id = models.CharField(max_length=11)
    store_name = models.CharField(max_length=100)
    picture_url = models.CharField(max_length=1000)


class Rating(models.Model):
    store_id = models.CharField(max_length=11)
    product_id = models.CharField(max_length=11)
    member_id = models.CharField(max_length=11)
    member_name = models.CharField(max_length=50)
    member_photo = models.CharField(max_length=1000)
    rating = models.CharField(max_length=11)
    date_time = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    description = models.CharField(max_length=50)


class ProductLike(models.Model):
    product_id = models.CharField(max_length=11)
    member_id = models.CharField(max_length=11)
    liked_time = models.CharField(max_length=50)


class Phone(models.Model):
    member_id = models.CharField(max_length=11)
    phone_number = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

class Address(models.Model):
    member_id = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)

class Coupon(models.Model):
    discount = models.CharField(max_length=11)
    expire_time = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

class UsedCoupon(models.Model):
    member_id = models.CharField(max_length=11)
    coupon_id = models.CharField(max_length=11)
    discount = models.CharField(max_length=11)
    expire_time = models.CharField(max_length=100)
    option = models.CharField(max_length=50)
    status = models.CharField(max_length=20)


class Order(models.Model):
    member_id = models.CharField(max_length=11)
    orderID = models.CharField(max_length=20)
    price = models.CharField(max_length=11)
    unit = models.CharField(max_length=20)
    shipping = models.CharField(max_length=11)
    date_time = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    address_line = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    discount = models.CharField(max_length=11)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)

class OrderItem(models.Model):
    order_id = models.CharField(max_length=11)
    member_id = models.CharField(max_length=11)
    vendor_id = models.CharField(max_length=11)
    store_id = models.CharField(max_length=11)
    store_name = models.CharField(max_length=100)
    product_id = models.CharField(max_length=11)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    gender_key = models.CharField(max_length=100)
    price = models.CharField(max_length=11)
    unit = models.CharField(max_length=20)
    quantity = models.CharField(max_length=11)
    date_time = models.CharField(max_length=50)
    picture_url = models.CharField(max_length=1000)
    delivery_days = models.CharField(max_length=100)
    delivery_price = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    orderID = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    discount = models.CharField(max_length=11)
    status2 = models.CharField(max_length=50)
    status_time = models.CharField(max_length=50)
    paid_amount = models.CharField(max_length=11)
    paid_time = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    paid_id = models.CharField(max_length=11)
    address = models.CharField(max_length=200)
    address_line = models.CharField(max_length=300)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)


class Notification(models.Model):
    receiver_id = models.CharField(max_length=11)
    message = models.CharField(max_length=1000)
    sender_id = models.CharField(max_length=11)
    sender_name = models.CharField(max_length=50)
    sender_email = models.CharField(max_length=80)
    sender_phone = models.CharField(max_length=1000)
    date_time = models.CharField(max_length=100)
    image_message = models.CharField(max_length=1000)


class Paid(models.Model):
    member_id = models.CharField(max_length=11)
    vendor_id = models.CharField(max_length=11)
    store_id = models.CharField(max_length=11)
    order_id = models.CharField(max_length=11)
    orderID = models.CharField(max_length=30)
    paid_amount = models.CharField(max_length=11)
    paid_time = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=30)
    charge_id = models.CharField(max_length=300)
    transfer_id = models.CharField(max_length=300)
    items = models.CharField(max_length=11)
    store_name = models.CharField(max_length=100)



class DriverLocation(models.Model):
    member_id = models.CharField(max_length=11)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    status = models.CharField(max_length=100)


class PreparedOrder(models.Model):
    member_id = models.CharField(max_length=11)
    driver_id = models.CharField(max_length=11)
    items_str = models.CharField(max_length=2000)
    date_time = models.CharField(max_length=50)
    status = models.CharField(max_length=50)


class PreparedOrderItem(models.Model):
    porder_id = models.CharField(max_length=11)
    item_id = models.CharField(max_length=11)
    status = models.CharField(max_length=50)















































