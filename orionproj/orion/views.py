import datetime
import difflib
import os
import string
import urllib
from itertools import islice

import io
import requests
import xlrd
import re

from django.core import mail
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.contrib import messages
# from _mysql_exceptions import DataError, IntegrityError
from django.template import RequestContext

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import EmailMultiAlternatives

from django.core.files.storage import FileSystemStorage
import json
from django.contrib import auth
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.cache import cache_control
from numpy import long

import pandas as pd
import numpy as np

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.fields import empty
from rest_framework.permissions import AllowAny
from xlrd import XLRDError
from time import gmtime, strftime
import time
from openpyxl.styles import PatternFill

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings
from django import forms
import sys
from django.core.cache import cache

import urllib.request
import urllib.parse
from random import randint
import random
import math

from pyfcm import FCMNotification

import stripe

from orion.models import Member, Store, Brand, Product, ProductPicture, Payment, Advertisement, Rating, ProductLike, Phone, Address, Coupon, UsedCoupon, Order, OrderItem, Notification, Paid, DriverLocation
from orion.models import PreparedOrder, PreparedOrderItem
from orion.serializers import MemberSerializer, StoreSerializer, BrandSerializer, ProductSerializer, ProductPictureSerializer, AdvertisementSerializer, RatingSerializer, ProductLikeSerializer
from orion.serializers import PhoneSerializer, AddressSerializer, CouponSerializer, UsedCouponSerializer, OrderSerializer, OrderItemSerializer, NotificationSerializer, PaidSerializer, DriverLocationSerializer
from orion.serializers import PreparedOrderSerializer, PreparedOrderItemSerializer


import pyrebase

config = {
    "apiKey": "AIzaSyCu1ayZb-yfB_YDYg7KhEzN0bKK_xiX3PE",
    "authDomain": "orion-1571871108783.firebaseapp.com",
    "databaseURL": "https://orion-1571871108783.firebaseio.com",
    "storageBucket": "orion-1571871108783.appspot.com"
}

firebase = pyrebase.initialize_app(config)


def index(request):
    return HttpResponse('<h2>Hello I am OR1ON backend!</h2>')

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def registerMember(request):

    if request.method == 'POST':

        name = request.POST.get('name', '')
        eml = request.POST.get('email', '')
        phone = request.POST.get('phone_number', '')
        password = request.POST.get('password', '')
        role = request.POST.get('role', '')

        users = Member.objects.filter(email=eml)
        count = users.count()
        if count == 0:
            member = Member()
            member.name = name
            member.email = eml
            member.phone_number = phone
            member.picture_url = settings.URL + '/static/orion/images/2428675.png'
            member.password = password
            member.role = role
            member.stores = '0'
            member.registered_time = str(int(round(time.time() * 1000)))
            member.save()

            fs = FileSystemStorage()

            i = 0
            for f in request.FILES.getlist('files'):
                # print("Product File Size: " + str(f.size))
                # if f.size > 1024 * 1024 * 2:
                #     continue
                i = i + 1
                filename = fs.save(f.name, f)
                uploaded_url = fs.url(filename)
                if i == 1:
                    member.picture_url = settings.URL + uploaded_url
                    member.save()

            serializer = MemberSerializer(member, many=False)

            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            users = Member.objects.filter(email=eml, role=role)
            count = users.count()
            if count == 0:
                resp_er = {'result_code': '1'}
                return HttpResponse(json.dumps(resp_er))
            else:
                resp_er = {'result_code': '2'}
                return HttpResponse(json.dumps(resp_er))

    elif request.method == 'GET':
        pass

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        role = request.POST.get('role', '')
        if password != '':
            members = Member.objects.filter(email=email, password=password, role=role)
        else:
            members = Member.objects.filter(email=email, role=role)
        resp = {}
        if members.count() > 0:
            member = members[0]
            serializer = MemberSerializer(member, many=False)
            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)
        else:
            members = Member.objects.filter(email=email, role=role)
            if members.count() > 0:
                resp = {'result_code': '2'}
            else: resp = {'result_code':'1'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def registerStore(request):

    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        name = request.POST.get('name', '')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')
        delivery_price = request.POST.get('delivery_price', '0')
        delivery_days = request.POST.get('delivery_days', '0')
        lat = request.POST.get('latitude', '')
        lng = request.POST.get('longitude', '')

        stores = Store.objects.filter(member_id=member_id)
        count = stores.count()
        if count == 0:
            store = Store()
            store.member_id = member_id
            store.name = name
            store.phone_number = phone_number
            store.address = address
            store.delivery_price = delivery_price
            store.delivery_days = delivery_days
            store.ratings = '0.0'
            store.reviews = '0'
            store.registered_time = str(int(round(time.time() * 1000)))
            store.latitude = lat
            store.longitude = lng
            store.save()

            fs = FileSystemStorage()

            f = request.FILES['file']

            filename = fs.save(f.name, f)
            uploaded_url = fs.url(filename)
            store.logo_url = settings.URL + uploaded_url
            store.save()

            member = Member.objects.get(id=member_id)
            member.stores = '1'
            member.save()

            serializer = StoreSerializer(store, many=False)

            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            resp_er = {'result_code': '1'}
            return HttpResponse(json.dumps(resp_er))

    elif request.method == 'GET':
        pass


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getMyStore(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        stores = Store.objects.filter(member_id=member_id)
        if stores.count() > 0:
            store = stores[0]
            serializer = StoreSerializer(store, many=False)
            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)
        else:
            resp = {'result_code': '1'}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def addBrand(request):

    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        store_id = request.POST.get('store_id', '1')
        name = request.POST.get('name', '')
        category = request.POST.get('category', '')

        brands = Brand.objects.filter(member_id=member_id, store_id=store_id, name=name, category=category)
        count = brands.count()
        if count == 0:
            brand = Brand()
            brand.member_id = member_id
            brand.store_id = store_id
            brand.name = name
            brand.category = category
            brand.registered_time = str(int(round(time.time() * 1000)))
            brand.save()

            fs = FileSystemStorage()

            f = request.FILES['file']

            filename = fs.save(f.name, f)
            uploaded_url = fs.url(filename)
            brand.logo_url = settings.URL + uploaded_url
            brand.save()

            serializer = BrandSerializer(brand, many=False)

            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            resp_er = {'result_code': '1'}
            return HttpResponse(json.dumps(resp_er))

    elif request.method == 'GET':
        pass


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getStoreBrands(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        store_id = request.POST.get('store_id', '1')
        brands = Brand.objects.filter(member_id=member_id, store_id=store_id).order_by('-id')

        serializer = BrandSerializer(brands, many=True)
        resp = {'result_code': '0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def editStore(request):

    if request.method == 'POST':
        store_id = request.POST.get('store_id', '1')
        name = request.POST.get('name', '')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')
        delivery_price = request.POST.get('delivery_price', '0')
        delivery_days = request.POST.get('delivery_days', '0')
        lat = request.POST.get('latitude', '')
        lng = request.POST.get('longitude', '')

        stores = Store.objects.filter(id=store_id)
        count = stores.count()
        if count > 0:
            store = stores[0]
            store.name = name
            store.phone_number = phone_number
            store.address = address
            store.delivery_price = delivery_price
            store.delivery_days = delivery_days
            store.latitude = lat
            store.longitude = lng
            store.save()

            fs = FileSystemStorage()

            i = 0
            for f in request.FILES.getlist('files'):
                # print("Product File Size: " + str(f.size))
                # if f.size > 1024 * 1024 * 2:
                #     continue
                i = i + 1
                filename = fs.save(f.name, f)
                uploaded_url = fs.url(filename)
                if i == 1:
                    store.logo_url = settings.URL + uploaded_url
                    store.save()

            serializer = StoreSerializer(store, many=False)

            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            resp_er = {'result_code': '1'}
            return HttpResponse(json.dumps(resp_er))

    elif request.method == 'GET':
        pass


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def editBrand(request):

    if request.method == 'POST':
        brand_id = request.POST.get('brand_id', '1')
        name = request.POST.get('name', '')
        category = request.POST.get('category', '')

        brands = Brand.objects.filter(id=brand_id)
        count = brands.count()
        if count > 0:
            brand = brands[0]
            brand.name = name
            brand.category = category
            brand.save()

            fs = FileSystemStorage()

            i = 0
            for f in request.FILES.getlist('files'):
                # print("Product File Size: " + str(f.size))
                # if f.size > 1024 * 1024 * 2:
                #     continue
                i = i + 1
                filename = fs.save(f.name, f)
                uploaded_url = fs.url(filename)
                if i == 1:
                    brand.logo_url = settings.URL + uploaded_url
                    brand.save()

            serializer = BrandSerializer(brand, many=False)

            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            resp_er = {'result_code': '1'}
            return HttpResponse(json.dumps(resp_er))

    elif request.method == 'GET':
        pass



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def deleteBrand(request):

    if request.method == 'POST':
        brand_id = request.POST.get('brand_id', '1')
        brands = Brand.objects.filter(id=brand_id)
        fs = FileSystemStorage()
        if brands.count() > 0:
            brand = brands[0]
            products = Product.objects.filter(brand_id=brand.pk)
            for product in products:
                pics = ProductPicture.objects.filter(product_id=product.pk)
                for pic in pics:
                    fname = pic.picture_url.replace(settings.URL + '/media/', '')
                    fs.delete(fname)
                    pic.delete()
                fname = product.picture_url.replace(settings.URL + '/media/', '')
                fs.delete(fname)
                product.delete()
            fname = brand.logo_url.replace(settings.URL + '/media/', '')
            fs.delete(fname)
            brand.delete()
            resp = {'result_code': '0'}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)
        else:
            resp = {'result_code': '1'}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getBrandProducts(request):
    if request.method == 'POST':
        brand_id = request.POST.get('brand_id', '1')
        products = Product.objects.filter(brand_id=brand_id).order_by('-id')
        serializer = ProductSerializer(products, many=True)
        resp = {'result_code': '0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def uploadProduct(request):

    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        store_id = request.POST.get('store_id', '1')
        brand_id = request.POST.get('brand_id', '1')
        name = request.POST.get('name', '')
        subcategory = request.POST.get('subcategory', '')
        gender = request.POST.get('gender', '')
        gender_key = request.POST.get('gender_key', '')
        price = request.POST.get('price', '')
        description = request.POST.get('description', '')
        delivery_price = request.POST.get('delivery_price', '0')
        delivery_days = request.POST.get('delivery_days', '0')

        brands = Brand.objects.filter(id=brand_id)
        brand = None
        if brands.count() > 0:
            brand = brands[0]

        products = Product.objects.filter(member_id=member_id, store_id=store_id, brand_id=brand_id, name=name, subcategory=subcategory, gender=gender, price=price, description=description)
        count = products.count()
        if count == 0:
            product = Product()
            product.member_id = member_id
            product.store_id = store_id
            product.brand_id = brand_id
            product.name = name
            if brand is not None:
                product.category = brand.category
            product.subcategory = subcategory
            product.gender = gender
            product.gender_key = gender_key
            product.price = price
            product.new_price = '0'
            product.unit = 'SGD'
            product.description = description
            product.delivery_price = delivery_price
            product.delivery_days = delivery_days
            product.likes = '0'
            product.ratings = '0'
            product.save()

            fs = FileSystemStorage()

            i = 0
            for f in request.FILES.getlist('files'):
                # print("Product File Size: " + str(f.size))
                # if f.size > 1024 * 1024 * 2:
                #     continue
                i = i + 1
                filename = fs.save(f.name, f)
                uploaded_url = fs.url(filename)
                if i == 1:
                    product.picture_url = settings.URL + uploaded_url
                    product.save()

                p = ProductPicture()
                p.product_id = product.pk
                p.picture_url = settings.URL + uploaded_url
                p.save()

            resp = {'result_code': '0'}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            resp_er = {'result_code': '1'}
            return HttpResponse(json.dumps(resp_er))

    elif request.method == 'GET':
        pass


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getProductPictures(request):

    if request.method == 'POST':
        product_id = request.POST.get('product_id', '1')
        pps = ProductPicture.objects.filter(product_id=product_id)
        serializer = ProductPictureSerializer(pps, many=True)

        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def deleteProduct(request):

    if request.method == 'POST':
        product_id = request.POST.get('product_id', '1')
        products = Product.objects.filter(id=product_id)
        fs = FileSystemStorage()
        if products.count() > 0:
            product = products[0]
            pics = ProductPicture.objects.filter(product_id=product.pk)
            for pic in pics:
                fname = pic.picture_url.replace(settings.URL + '/media/', '')
                fs.delete(fname)
                pic.delete()
            fname = product.picture_url.replace(settings.URL + '/media/', '')
            fs.delete(fname)
            product.delete()
            resp = {'result_code': '0'}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)
        else:
            resp = {'result_code': '1'}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def editProduct(request):

    if request.method == 'POST':
        product_id = request.POST.get('product_id', '1')
        name = request.POST.get('name', '')
        subcategory = request.POST.get('subcategory', '')
        gender = request.POST.get('gender', '')
        gender_key = request.POST.get('gender_key', '')
        price = request.POST.get('price', '')
        description = request.POST.get('description', '')
        delivery_price = request.POST.get('delivery_price', '0')
        delivery_days = request.POST.get('delivery_days', '0')

        products = Product.objects.filter(id=product_id)
        count = products.count()
        if count > 0:
            product = products[0]
            product.name = name
            product.subcategory = subcategory
            product.gender = gender
            product.gender_key = gender_key
            if float(price) != float(product.price):
                product.new_price = price
            product.unit = 'SGD'
            product.description = description
            product.delivery_price = delivery_price
            product.delivery_days = delivery_days

            product.save()

            fs = FileSystemStorage()

            i = 0
            for f in request.FILES.getlist('files'):
                # print("Product File Size: " + str(f.size))
                # if f.size > 1024 * 1024 * 2:
                #     continue
                i = i + 1
                filename = fs.save(f.name, f)
                uploaded_url = fs.url(filename)
                if i == 1:
                    product.picture_url = settings.URL + uploaded_url
                    product.save()

                p = ProductPicture()
                p.product_id = product.pk
                p.picture_url = settings.URL + uploaded_url
                p.save()

            serializer = ProductSerializer(product, many=False)
            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            resp_er = {'result_code': '1'}
            return HttpResponse(json.dumps(resp_er))

    elif request.method == 'GET':
        pass


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def delProductPicture(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id', '1')
        picture_url = request.POST.get('picture_url', '')
        pictures = ProductPicture.objects.filter(product_id=product_id)
        for pic in pictures:
            if pic.picture_url == picture_url:
                pic.delete()
        products = Product.objects.filter(id=product_id)
        if products.count() > 0:
            product = products[0]
            pictures = ProductPicture.objects.filter(product_id=product_id)
            if pictures.count() > 0:
                pic = pictures[0]
                product.picture_url = pic.picture_url
                product.save()
            else:
                product.picture_url = ''
                product.save()

            resp = {'result_code':'0'}
            return HttpResponse(json.dumps(resp))
        else:
            resp = {'result_code':'1'}
            return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')

        usrs = Member.objects.filter(email=email)
        if usrs.count() == 0:
            return HttpResponse(json.dumps({'result_code': '1'}))

        message = 'You are allowed to reset your password from your request.<br>For it, please click this link to reset your password.<br><br>https://OR10N.pythonanywhere.com/resetpassword?email=' + email

        html =  """\
                    <html>
                        <head></head>
                        <body>
                            <a href="https://OR10N.pythonanywhere.com/"><img src="https://OR10N.pythonanywhere.com/static/orion/images/logo.jpg" style="width:150px;height:150px;border-radius: 8%; margin-left:25px;"/></a>
                            <h2 style="margin-left:10px; color:#02839a;">Voxmed User's Security Update Information</h2>
                            <div style="font-size:16px; word-break: break-all; word-wrap: break-word;">
                                {mes}
                            </div>
                        </body>
                    </html>
                """
        html = html.format(mes=message)

        fromEmail = 'Feroz.said@gmail.com'
        toEmailList = []
        toEmailList.append(email)
        msg = EmailMultiAlternatives('We allowed you to reset your password', '', fromEmail, toEmailList)
        msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=False)

        return HttpResponse(json.dumps({'result_code': '0'}))


def resetpassword(request):
    email = request.GET['email']
    return render(request, 'orion/resetpwd.html', {'email':email})


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def rstpwd(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        repassword = request.POST.get('repassword', '')
        if len(password) < 8:
            return render(request, 'orion/result.html',
                          {'response': 'Please enter password of characters more than 8.'})
        if password != repassword:
            return render(request, 'orion/result.html',
                          {'response': 'Please enter the same password.'})
        members = Member.objects.filter(email=email)
        if members.count() > 0:
            member = members[0]
            member.password = password
            member.save()
            return render(request, 'orion/result.html',
                          {'response': 'Password has been reset successfully.'})
        else:
            return render(request, 'orion/result.html',
                          {'response': 'You haven\'t been registered.'})
    else: pass


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def updateMember(request):

    if request.method == 'POST':

        member_id = request.POST.get('member_id', '1')
        name = request.POST.get('name', '')
        eml = request.POST.get('email', '')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')
        country = request.POST.get('country', '')
        area = request.POST.get('area', '')
        street = request.POST.get('street', '')
        house = request.POST.get('house', '')
        latitude = request.POST.get('latitude', '0')
        longitude = request.POST.get('longitude', '0')

        users = Member.objects.filter(id=member_id)
        count = users.count()
        if count > 0:
            member = users[0]
            member.name = name
            member.email = eml
            member.phone_number = phone_number
            if address != '': member.address = address
            if country != '': member.country = country
            if area != '': member.area = area
            if street != '': member.street = street
            if house != '': member.house = house
            member.latitude = latitude
            member.longitude = longitude

            member.save()

            fs = FileSystemStorage()

            i = 0
            for f in request.FILES.getlist('files'):
                # print("Product File Size: " + str(f.size))
                # if f.size > 1024 * 1024 * 2:
                #     continue
                i = i + 1
                filename = fs.save(f.name, f)
                uploaded_url = fs.url(filename)
                if i == 1:
                    member.picture_url = settings.URL + uploaded_url
                    member.save()

            serializer = MemberSerializer(member, many=False)

            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            resp_er = {'result_code': '1'}
            return HttpResponse(json.dumps(resp_er))

    elif request.method == 'GET':
        pass

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def new_payment_account(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        member_id = request.POST.get('member_id', '1')
        member = Member.objects.get(id=member_id)

        payments = Payment.objects.filter(member_id=member_id)
        resp = {'result_code':'0', 'acc_id':''}
        if payments.count() == 0:
            payment = Payment()
            payment.member_id = member_id
            try:
                acc = stripe.Account.create(
                  type="custom",
                  country="SG",
                  email=member.email,
                #   requested_capabilities=['card_payments', 'transfers'],       ################## when country is US
                )

                payment.acc_id = acc['id']
                payment.status = 'pending'
                payment.save()

                resp = {'result_code':'0', 'acc_id': payment.acc_id}

            except stripe.error.InvalidRequestError as e:
                print('stripe error')
                resp = {'result_code':'1'}

        else:
            payment = payments[0]
            resp = {'result_code':'0', 'acc_id': payment.acc_id, 'status': payment.status}

        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getPaymentStatus(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        payments = Payment.objects.filter(member_id=member_id)
        resp = {'result_code': '1'}
        if payments.count() > 0:
            payment = payments[0]
            resp = {'result_code':'0', 'status':payment.status}
        return HttpResponse(json.dumps(resp))



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def complete_payment_account(request):
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        acc_number = request.POST.get('bank_number', '')
        country = request.POST.get('country', '')
        routing_number = request.POST.get('routing_number', '')
        day = request.POST.get('day', '')
        month = request.POST.get('month', '')
        year = request.POST.get('year', '')
        city = request.POST.get('city', '')
        address = request.POST.get('address', '')
        postal_code = request.POST.get('postal_code', '')
        state = request.POST.get('state', '')
        ssn_last_4 = request.POST.get('ssn_last4', '')
        created_on = int(round(time.time()))

        member = Member.objects.get(id=member_id)
        acc_id = ''
        payments = Payment.objects.filter(member_id=member_id)
        payment = None
        if payments.count() > 0:
            payment = payments[0]
            acc_id = payment.acc_id
        else:
            resp = {'result_code':'1'}
            return HttpResponse(json.dumps(resp))

        external_account = {
            'object': 'bank_account',
            'account_number': acc_number,
            'country': 'SG',                         ############ country
            'currency': 'sgd',
            'routing_number': routing_number,
            # 'last4': ssn_last_4
        }

        dob = {
            'day': day,
            'month': month,
            'year': year,
        }

        addr = {
            'city': city,
            # 'country': 'SG',
            'line1': address,
            'postal_code': postal_code,
            # 'state': state
        }

        first_name, last_name = getFirstLastName(member.name)

        legal = {
            'dob': dob,
            'address': addr,
            'first_name':first_name,
            'last_name':last_name,
            # 'email':member.email,
            # 'phone':member.phone_number,
            # 'ssn_last_4':ssn_last_4,
        }

        tos = {
            'date': created_on,
            'ip': '75.70.234.51'
        }

        account = stripe.Account.modify(
          acc_id,
          external_account=external_account,
          business_type='individual',
          individual=legal,
          tos_acceptance=tos,
        )

        if account is not None:
            payment.acc_id = account['id']
            payment.status = 'completed'
            payment.bank_number = acc_number
            payment.routing_number = routing_number
            payment.country = country
            payment.city = city
            payment.address = address
            payment.postal_code = postal_code
            payment.state = state
            payment.ssn_last4 = ssn_last_4
            payment.birth_date = day
            payment.birth_month = month
            payment.birth_year = year
            payment.registered_time = str(int(round(time.time() * 1000)))
            payment.save()
            resp = {'result_code':'0'}
            return HttpResponse(json.dumps(resp))
        else:
            resp = {'result_code':'1'}
            return HttpResponse(json.dumps(resp))

def getFirstLastName(nameStr):
    nameStr = nameStr.split()
    first_name = nameStr[0]
    try:
        last_name = nameStr[1]
    except:
        last_name = ''
    return first_name, last_name


def paybycard(request):
    price = request.GET['price']
    member_id = request.GET['member_id']
    vendor_id = request.GET['vendor_id']
    itemIds = request.GET['itemids']
    type = request.GET['type']
    return render(request, 'orion/checkout.html', {'price':price, 'member_id':member_id, 'vendor_id':vendor_id, 'itemids':itemIds, 'type':type})


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def payFor(request):
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    if request.method == "POST":
        token = request.POST.get('token', '')
        price = request.POST.get('price', '')
        member_id = request.POST.get('member_id', '1')
        vendor_id = request.POST.get('vendor_id', '1')

        itemids = request.POST.get('itemids', '')
        type = request.POST.get('type', '')

        members = Member.objects.filter(id=member_id)
        if members.count() == 0:
            return render(request, 'orion/result.html',
                                      {'response': 'The customer doesn\'t exist.'})
        member = Member.objects.get(id=member_id)
        vendors = Member.objects.filter(id=vendor_id)
        if vendors.count() == 0:
            return render(request, 'orion/result.html',
                                      {'response': 'The vendor doesn\'t exist.'})
        vendor = Member.objects.get(id=vendor_id)

        if type == 'pay':

            payments = Payment.objects.filter(member_id=vendor_id)
            payment = None
            if payments.count() > 0:
                payment = payments[0]
            else:
                return render(request, 'orion/result.html',
                                          {'response': 'The vendor\'s payment hasn\'t been verified.'})
            amount = int(float(price.replace('$', '').replace(',', '')))

            try:
                charge = stripe.Charge.create(
                    amount=amount,
                    currency="sgd",
                    source=token  # obtained with Stripe.js
                )
                if charge is not None:
                    amount1 = amount - int(float(amount*0.1))     ##### to vendor (90%), to admin (10%)
                    try:
                        transfer = stripe.Transfer.create(
                            amount=amount1,
                            currency="sgd",
                            destination=payment.acc_id
                        )

                        if transfer is not None:
                            itemidList = itemids.split(',')

                            paid = Paid()
                            paid.member_id = member_id
                            paid.vendor_id = vendor_id
                            paid.paid_amount = str(amount)
                            paid.paid_time = str(int(round(time.time() * 1000)))
                            paid.payment_status = type
                            paid.charge_id = charge['id']
                            paid.transfer_id = transfer['id']
                            paid.save()

                            storeId = '0'
                            orderId = '0'
                            orderID = ''

                            for itemid in itemidList:
                                items = OrderItem.objects.filter(id=int(itemid))
                                if items.count() > 0:
                                    item = items[0]
                                    if storeId == '0': storeId = item.store_id
                                    if orderId == '0': orderId = item.order_id
                                    if orderID == '':
                                        orders = Order.objects.filter(id=item.order_id)
                                        if orders.count() > 0:
                                            order = orders[0]
                                            orderID = order.orderID
                                    item.paid_amount = item.price
                                    item.paid_time = paid.paid_time
                                    item.payment_status = type
                                    item.paid_id = paid.pk
                                    item.save()
                            paid.store_id = storeId
                            paid.order_id = orderId
                            paid.orderID = orderID
                            paid.save()

                            store = Store.objects.get(id=paid.store_id)
                            itemInfo = 'Order ID: ' + orderID + '\n' + 'Store Name: ' + store.name + '\n' + 'Amount: ' + str(amount1) + 'SGD consulting the application fee 10%'
                            info = 'Hi ' + vendor.name + ', I paid you on this order:\n' + itemInfo + '\nThe payment processing will take some time.\nPlease check it kindly.'
                            toids = []
                            toids.append(vendor_id)
                            sendMessage(member_id, toids, info, 'pay')
                            registerNotification(vendor_id, info, member_id, member.name, member.email, member.phone_number, '')

                            sendFCMPushNotification(vendor_id, member_id, info)

                            return render(request, 'orion/result.html',
                                              {'response': 'Your payment is done successfully!'})

                        else:
                            return render(request, 'orion/result.html',
                                          {'response': 'Payment Transfer Error!'})


                    except stripe.error.InvalidRequestError as e:
                        print('error')
                        return render(request, 'orion/result.html',
                                          {'response': 'Payment Transfer Error!'})
                else:
                    return render(request, 'orion/result.html',
                                          {'response': 'Payment Charge Error!'})
            except stripe.error.InvalidRequestError as e:
                    return render(request, 'orion/result.html',
                                          {'response': 'Payment Charge Error!'})



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getPaid(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        vendor_id = request.POST.get('vendor_id', '1')
        store_id = request.POST.get('store_id', '1')
        order_id = request.POST.get('order_id', '1')

        paids = Paid.objects.filter(member_id=member_id, vendor_id=vendor_id, order_id=order_id, store_id=store_id)
        if paids.count() > 0:
            paid = paids[0]
            current = int(round(time.time() * 1000))
            paid_time = int(paid.paid_time)
            if current - paid_time < 60000:
                resp = {'result_code':'0'}
                return HttpResponse(json.dumps(resp))
            else:
                resp = {'result_code':'1'}
                return HttpResponse(json.dumps(resp))
        else:
            resp = {'result_code':'1'}
            return HttpResponse(json.dumps(resp))




@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getStores(request):
    if request.method == 'POST':
        stores = Store.objects.all().order_by('-id')
        serializer = StoreSerializer(stores, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getAdvertisements(request):
    if request.method == 'POST':
        ads = Advertisement.objects.all().order_by('-id')
        serializer = AdvertisementSerializer(ads, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getStoreProducts(request):
    if request.method == 'POST':
        store_id = request.POST.get('store_id', '1')
        member_id = request.POST.get('member_id', '1')
        products = Product.objects.filter(store_id=store_id).order_by('-id')
        for product in products:
            brands = Brand.objects.filter(id=product.brand_id)
            if brands.count() > 0:
                brand = brands[0]
                product.brand_name = brand.name
                product.brand_logo = brand.logo_url
            plikes = ProductLike.objects.filter(product_id=product.pk, member_id=member_id)
            if plikes.count() > 0:
                product.isLiked = 'yes'
            else: product.isLiked = 'no'
        serializer = ProductSerializer(products, many=True)
        resp = {'result_code': '0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getStoreRatings(request):

    if request.method == 'POST':
        store_id = request.POST.get('store_id', '1')
        ratings = Rating.objects.filter(store_id=store_id).order_by('-id')
        serializer = RatingSerializer(ratings, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def placeStoreFeedback(request):

    if request.method == 'POST':

        store_id = request.POST.get('store_id', '1')
        member_id = request.POST.get('member_id', '1')
        subject = request.POST.get('subject', '')
        rating = request.POST.get('rating', '1')
        description = request.POST.get('description', '')

        members = Member.objects.filter(id=member_id)
        member = None
        if members.count() > 0:
            member = members[0]
        isNew = False
        rts = Rating.objects.filter(member_id=member_id, store_id=store_id)
        if rts.count() == 0:
            rt = Rating()
            rt.member_id = member_id
            if member is not None: rt.member_name = member.name
            rt.member_photo = member.picture_url
            rt.store_id = store_id
            rt.product_id = '0'
            rt.subject = subject
            rt.rating = rating
            rt.description = description
            rt.date_time = str(int(round(time.time() * 1000)))
            rt.save()
            isNew = True
        else:
            rt = rts[0]
            rt.member_id = member_id
            if member is not None: rt.member_name = member.name
            rt.member_photo = member.picture_url
            rt.store_id = store_id
            rt.product_id = '0'
            rt.subject = subject
            rt.rating = rating
            rt.description = description
            rt.date_time = str(int(round(time.time() * 1000)))
            rt.save()

        rts = Rating.objects.filter(store_id=store_id)
        if rts.count() > 0:
            i = 0
            for rt in rts:
                if rt.rating == '':
                    rt.rating = '0'
                i = i + float(rt.rating)
            i = float(i/rts.count())
            rat = str(i)
            rat = rat[:3]
            store = Store.objects.get(id=store_id)
            store.ratings = rat
            if isNew: store.reviews = str(int(store.reviews) + 1)
            store.save()

        store = Store.objects.get(id=store_id)

        resp = {'result_code':'0', 'ratings':str(store.ratings), 'reviews':str(store.reviews)}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def likeProduct(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id', '1')
        member_id = request.POST.get('member_id', '1')
        plike = ProductLike()
        plike.product_id = product_id
        plike.member_id = member_id
        plike.liked_time = str(int(round(time.time() * 1000)))
        plike.save()
        plikes = ProductLike.objects.filter(product_id=product_id)
        product = Product.objects.get(id=product_id)
        product.likes = str(plikes.count())
        product.save()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def unLikeProduct(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id', '1')
        member_id = request.POST.get('member_id', '1')
        plikes = ProductLike.objects.filter(product_id=product_id, member_id=member_id)
        if plikes.count() > 0:
            plike = plikes[0]
            plike.delete()
        plikes = ProductLike.objects.filter(product_id=product_id)
        product = Product.objects.get(id=product_id)
        product.likes = str(plikes.count())
        product.save()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getCategoryStores(request):
    if request.method == 'POST':
        stores = Store.objects.all().order_by('-id')
        storeList = []
        for store in stores:
            categoryList = []
            subcategoryList = []
            genderList = []
            products = Product.objects.filter(store_id=store.pk)
            for product in products:
                if not product.category in categoryList:
                    categoryList.append(product.category)
                if not product.subcategory in subcategoryList:
                    subcategoryList.append(product.subcategory)
                if not product.gender in genderList:
                    genderList.append(product.gender)

            data = {
                'id':store.pk,
                'member_id':store.member_id,
                'name': store.name,
                'phone_number': store.phone_number,
                'address': store.address,
                'logo_url': store.logo_url,
                'registered_time': store.registered_time,
                'ratings': store.ratings,
                'reviews': store.reviews,
                'status': store.status,
                'genders': genderList,
                'categories': categoryList,
                'subcategories': subcategoryList
            }

            storeList.append(data)

        resp = {'result_code':'0', 'data':storeList}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def placeProductFeedback(request):

    if request.method == 'POST':

        product_id = request.POST.get('product_id', '1')
        member_id = request.POST.get('member_id', '1')
        rating = request.POST.get('rating', '1')
        description = request.POST.get('description', '')

        members = Member.objects.filter(id=member_id)
        member = None
        if members.count() > 0:
            member = members[0]
        rts = Rating.objects.filter(member_id=member_id, product_id=product_id)
        if rts.count() == 0:
            rt = Rating()
            rt.member_id = member_id
            if member is not None: rt.member_name = member.name
            rt.member_photo = member.picture_url
            rt.store_id = '0'
            rt.product_id = product_id
            rt.subject = ''
            rt.rating = rating
            rt.description = description
            rt.date_time = str(int(round(time.time() * 1000)))
            rt.save()
        else:
            rt = rts[0]
            rt.member_id = member_id
            if member is not None: rt.member_name = member.name
            rt.member_photo = member.picture_url
            rt.store_id = '0'
            rt.product_id = product_id
            rt.subject = ''
            rt.rating = rating
            rt.description = description
            rt.date_time = str(int(round(time.time() * 1000)))
            rt.save()

        rts = Rating.objects.filter(product_id=product_id)
        if rts.count() > 0:
            i = 0
            for rt in rts:
                if rt.rating == '':
                    rt.rating = '0'
                i = i + float(rt.rating)
            i = float(i/rts.count())
            rat = str(i)
            rat = rat[:3]
            product = Product.objects.get(id=product_id)
            product.ratings = rat
            product.save()

        product = Product.objects.get(id=product_id)

        resp = {'result_code':'0', 'ratings':str(product.ratings)}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getProductRatings(request):

    if request.method == 'POST':
        product_id = request.POST.get('product_id', '1')
        member_id = request.POST.get('member_id', '1')
        ratings = Rating.objects.filter(product_id=product_id, member_id=member_id)
        if ratings.count() > 0:
            rating = ratings[0]
            serializer = RatingSerializer(rating, many=False)
            ratings = Rating.objects.filter(product_id=product_id)
            resp = {'result_code':'0', 'data':serializer.data, 'allreviews': ratings.count() }
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)
        else:
            resp = {'result_code':'1'}
            return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def productInfo(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id', '1')
        products = Product.objects.filter(id=product_id)
        if products.count() > 0:
            product = products[0]
            brands = Brand.objects.filter(id=product.brand_id)
            if brands.count() > 0:
                brand = brands[0]
                product.brand_name = brand.name
                product.brand_logo = brand.logo_url
            store = Store.objects.get(id=product.store_id)
            serializer = ProductSerializer(product, many=False)
            serializer2 = StoreSerializer(store, many=False)
            resp = {'result_code':'0', 'product':serializer.data, 'store':serializer2.data}
            return HttpResponse(json.dumps(resp))
        else:
            resp = {'result_code':'1'}
            return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getPhones(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        phones = Phone.objects.filter(member_id=member_id).order_by('-id')
        serializer = PhoneSerializer(phones, many=True)
        resp = {'result_code': '0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getAddresses(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        addresses = Address.objects.filter(member_id=member_id).order_by('-id')
        serializer = AddressSerializer(addresses, many=True)
        resp = {'result_code': '0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getCoupons(request):
    if request.method == 'POST':

        member_id = request.POST.get('member_id','1')

        availableList = []
        expiredList = []
        usedList = []

        coupons = Coupon.objects.all().order_by('-id')
        for coupon in coupons:
            current = int(round(time.time() * 1000))
            if current > int(coupon.expire_time):
                expiredList.append(coupon)
            useds = UsedCoupon.objects.filter(coupon_id=coupon.pk, member_id=member_id)
            if useds.count() > 0:
                usedList.append(coupon)
            if coupon not in expiredList and coupon not in usedList:
                availableList.append(coupon)

        serializer_expired = CouponSerializer(expiredList, many=True)
        serializer_used = CouponSerializer(usedList, many=True)
        serializer_available = CouponSerializer(availableList, many=True)

        resp = {'result_code':'0', 'expireds':serializer_expired.data, 'useds':serializer_used.data, 'availables':serializer_available.data}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def savePhoneNumber(request):

    if request.method == 'POST':
        member_id = request.POST.get('member_id', '0')
        phone_number = request.POST.get('phone_number', '')

        phones = Phone.objects.filter(member_id=member_id, phone_number=phone_number)
        if phones.count() == 0:
            phone = Phone()
            phone.member_id = member_id
            phone.phone_number = phone_number
            phone.save()
            resp = {'result_code':'0'}
        else:
            resp = {'result_code':'1'}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def saveAddress(request):

    if request.method == 'POST':
        member_id = request.POST.get('member_id', '0')
        address = request.POST.get('address', '')
        area = request.POST.get('area', '')
        street = request.POST.get('street', '')
        house = request.POST.get('house', '')
        lat = request.POST.get('latitude', '')
        lng = request.POST.get('longitude', '')

        adrs = Address.objects.filter(member_id=member_id, address=address, area=area, street=street, house=house)
        if adrs.count() == 0:
            adr = Address()
            adr.member_id = member_id
            adr.address = address
            adr.area = area
            adr.street = street
            adr.house = house
            adr.latitude = lat
            adr.longitude = lng
            adr.save()
            resp = {'result_code':'0'}
        else:
            resp = {'result_code':'1'}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def delAddress(request):

    if request.method == 'POST':
        addr_id = request.POST.get('addr_id', '1')
        addr = Address.objects.get(id=addr_id)
        if addr is not None:
            addr.delete()
            resp = {'result_code':'0'}
        else:
            resp = {'result_code':'1'}
        return HttpResponse(json.dumps(resp))

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def delPhone(request):

    if request.method == 'POST':
        phone_id = request.POST.get('phone_id', '1')
        phone = Phone.objects.get(id=phone_id)
        if phone is not None:
            phone.delete()
            resp = {'result_code':'0'}
        else:
            resp = {'result_code':'1'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def uploadOrder(request):

    if request.method == 'POST':

        member_id = request.POST.get('member_id', '0')
        orderID = request.POST.get('orderID', '')
        price = request.POST.get('price', '0')
        unit = request.POST.get('unit', '')
        shipping = request.POST.get('shipping', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        address_line = request.POST.get('address_line', '')
        phone_number = request.POST.get('phone_number', '')
        coupon_id = request.POST.get('coupon_id', '0')
        discount = request.POST.get('discount', '0')
        lat = request.POST.get('latitude', '')
        lng = request.POST.get('longitude', '')

        orderItems = request.POST.get('orderItems', '')

        order = Order()
        order.member_id = member_id
        order.orderID = orderID
        order.price = price
        order.unit = unit
        order.shipping = shipping
        order.date_time = str(int(round(time.time() * 1000)))
        order.email = email
        order.address = address
        order.address_line = address_line
        order.phone_number = phone_number
        order.status = 'placed'
        order.discount = discount
        order.latitude = lat
        order.longitude = lng

        order.save()

        try:
            decoded = json.loads(orderItems)
            for orderItem_data in decoded['orderItems']:

                member_id = orderItem_data['member_id']
                vendor_id = orderItem_data['vendor_id']
                store_id = orderItem_data['store_id']
                store_name = orderItem_data['store_name']
                product_id = orderItem_data['product_id']
                product_name = orderItem_data['product_name']
                category = orderItem_data['category']
                subcategory = orderItem_data['subcategory']
                gender = orderItem_data['gender']
                gender_key = orderItem_data['gender_key']
                price = orderItem_data['price']
                unit = orderItem_data['unit']
                quantity = orderItem_data['quantity']
                date_time = order.date_time
                picture_url = orderItem_data['picture_url']
                delivery_days = orderItem_data['delivery_days']
                delivery_price = orderItem_data['delivery_price']

                item = OrderItem()
                item.order_id = order.pk
                item.member_id = member_id
                item.vendor_id = vendor_id
                item.store_id = store_id
                item.store_name = store_name
                item.product_id = product_id
                item.product_name = product_name
                item.category = category
                item.subcategory = subcategory
                item.gender = gender
                item.gender_key = gender_key
                item.price = price
                item.unit = unit
                item.quantity = quantity
                item.date_time = date_time
                item.picture_url = picture_url
                item.delivery_days = delivery_days
                item.delivery_price = delivery_price
                item.status = 'placed'
                item.discount = order.discount
                item.status_time = date_time
                item.paid_amount = '0'
                item.paid_time = ''
                item.payment_status = ''
                item.paid_id = '0'
                item.address = order.address
                item.address_line = order.address_line
                item.latitude = order.latitude
                item.longitude = order.longitude

                item.save()

                itemInfo = 'Order ID: ' + orderID + '\n' + 'Order Date: ' + time.strftime('%d/%m/%Y %H:%M', time.gmtime(int(item.date_time) / 1000.0)) + '\n'
                itemInfo = itemInfo + 'Order Status: Order Placed' + '\n' + 'Item Name: ' + item.product_name + '\n' + 'Item Category: ' + item.category + ',' + item.subcategory + '\n'
                itemInfo = itemInfo + 'Item Price: ' + item.price + ' SGD' + '\n' + 'Quantity: ' + item.quantity + '\n' + 'Store: ' + item.store_name

                member = Member.objects.get(id=member_id)
                info = 'Hi, I placed a new order on ORION.\n' + itemInfo + '\nPlease check to process it kindly.'
                toids = []
                toids.append(vendor_id)
                sendMessage(member_id, toids, info, 'order')
                registerNotification(vendor_id, info, member_id, member.name, member.email, member.phone_number, '')

                sendFCMPushNotification(vendor_id, member_id, info)

            if int(coupon_id) > 0:
                ucoupon = UsedCoupon()
                ucoupon.member_id = member_id
                ucoupon.coupon_id = coupon_id
                ucoupon.discount = discount
                coupon = Coupon.objects.get(id=coupon_id)
                ucoupon.expire_time = coupon.expire_time
                ucoupon.status = 'used'
                ucoupon.save()

            resp = {'result_code': '0', 'orderID':order.orderID, 'date_time':order.date_time}
            return HttpResponse(json.dumps(resp))

        except:
            resp = {'result_code': '1'}
            return HttpResponse(json.dumps(resp))


def sendMessage(fromid, toids, message, opt):
    fromMembers = Member.objects.filter(id=fromid)
    if fromMembers.count() > 0:
        fromMember = fromMembers[0]

        db = firebase.database()

        from_name = fromMember.name
        if opt == 'admin': from_name = 'ORION Admin'

        data = {
            "msg": message,
            "date":str(int(round(time.time() * 1000))),
            "fromid": str(fromMember.pk),
            "fromname": from_name
        }

        for toid in toids:
            toMembers = Member.objects.filter(id=toid)
            if toMembers.count() > 0:
                toMember = toMembers[0]
                db.child(opt).child(str(toMember.pk)).push(data)




def registerNotification(receiverid, message, senderid, sendername, senderemail, senderphone, image):
    senders = Member.objects.filter(id=senderid)
    if senders.count() > 0:
        sender = senders[0]
        noti = Notification()
        noti.receiver_id = receiverid
        noti.message = message
        noti.sender_id = sender.pk
        noti.sender_name = sender.name
        noti.sender_email = sender.email
        noti.sender_phone = sender.phone_number
        noti.date_time = str(int(round(time.time() * 1000)))
        noti.image_message = image
        noti.save()

    resp = {'result_code':'0'}
    return HttpResponse(json.dumps(resp))


#inserting the token into database, after receiving it from Volley
@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def fcm_insert(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', 1)
        token = request.POST.get('fcm_token', '')
        member = Member.objects.get(id=member_id)
        member.fcm_token = token
        member.save()
        resp = {'result_code':'0', 'fcm_token':token}
        return JsonResponse(resp)

def sendFCMPushNotification(member_id, sender_id, notiText):
    date_time = str(time.strftime('%d/%m/%Y %H:%M'))
    members = Member.objects.filter(id=member_id)
    if members.count() > 0:
        member = members[0]
        message_title = 'ORION'
        if int(sender_id) > 0:
            senders = Member.objects.filter(id=sender_id)
            if senders.count() > 0:
                sender = senders[0]
                message_title = sender.name
        path_to_fcm = "https://fcm.googleapis.com"
        server_key = settings.FCM_LEGACY_SERVER_KEY
        reg_id = member.fcm_token #quick and dirty way to get that ONE fcmId from table
        if reg_id != '':
            message_body = notiText
            result = FCMNotification(api_key=server_key).notify_single_device(registration_id=reg_id, message_title=message_title, message_body=message_body, sound = 'ping.aiff', badge = 1)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getNotifications(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id', '1')
        notifications = Notification.objects.filter(receiver_id=receiver_id).order_by('-id')
        serializer = NotificationSerializer(notifications, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def delNotification(request):
    if request.method == 'POST':
        noti_id = request.POST.get('notification_id', '1')
        noti = Notification.objects.get(id=noti_id)
        noti.delete()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getUserOrders(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        orderList = []
        orders = Order.objects.filter(member_id=member_id).order_by('-id')
        for order in orders:
            orderList.append(order)

        resp = {'result_code':'0', 'data':orderData(orderList)}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def delOrder(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id', '1')
        order = Order.objects.get(id=order_id)
        if order is not None:
            items = OrderItem.objects.filter(order_id=order.pk)
            for item in items:
                item.delete()
            order.delete()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def userOrderItems(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        itemsList = []
        items = OrderItem.objects.filter(member_id=member_id).order_by('-id')
        for item in items:
            orders = Order.objects.filter(id=item.order_id)
            order = None
            if orders.count() > 0:
                order = orders[0]
            if order is not None:
                item.orderID = order.orderID
                vendors = Member.objects.filter(id=item.vendor_id)
                vendor = None
                if vendors.count() > 0:
                    vendor = vendors[0]
                    item.contact = vendor.phone_number
                    itemsList.append(item)
        serializer = OrderItemSerializer(itemsList, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp))


def orderData(orders):
    orderList = []
    for order in orders:
        member_name = ''
        if int(order.member_id) > 0:
            members = Member.objects.filter(id=order.member_id)
            if members.count() > 0:
                member = members[0]
                member_name = member.name
        items = OrderItem.objects.filter(order_id=order.pk)
        for item in items:
            vendors = Member.objects.filter(id=item.vendor_id)
            if vendors.count() > 0:
                vendor = vendors[0]
                item.contact = vendor.phone_number
        serializer = OrderItemSerializer(items, many=True)

        data = {
            'id':order.pk,
            'member_id':order.member_id,
            'orderID':order.orderID,
            'price':order.price,
            'unit':order.unit,
            'shipping':order.shipping,
            'date_time':order.date_time,
            'email':order.email,
            'address':order.address,
            'address_line':order.address_line,
            'latitude':order.latitude,
            'longitude':order.longitude,
            'phone_number':order.phone_number,
            'status':order.status,
            'discount':order.discount,
            'items':serializer.data,
            'member_name':member_name,
        }

        orderList.append(data)
    return orderList



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def receivedOrderItems(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        itemsList = []
        items = OrderItem.objects.filter(vendor_id=member_id).order_by('-id')
        for item in items:
            if item.status2 != 'canceled':
                orders = Order.objects.filter(id=item.order_id)
                if orders.count() > 0:
                    order = orders[0]
                    item.orderID = order.orderID
                    item.contact = order.phone_number
                    itemsList.append(item)
        serializer = OrderItemSerializer(itemsList, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def cancelOrderItem(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id', '1')
        item = OrderItem.objects.get(id=item_id)
        if item is not None:
            item.status2 = 'canceled'
            item.save()
        resp = {'result_code':'0'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def progressOrderItem(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        item_id = request.POST.get('item_id', '1')
        next = request.POST.get('next', '')
        item = OrderItem.objects.get(id=item_id)
        if item is not None:
            item.status = next
            item.status_time = str(int(round(time.time() * 1000)))
            item.save()

            member = Member.objects.get(id=member_id)

            orders = Order.objects.filter(id=item.order_id)
            if orders.count() > 0:
                order = orders[0]
                status = item.status
                if item.status == 'confirmed':status = 'Order Confirmed'
                elif item.status == 'prepared':status = 'Order Prepared'
                elif item.status == 'ready':status = 'Order Ready'
                elif item.status == 'delivered':status = 'Order Delivered'
                itemInfo = 'Order ID: ' + order.orderID + '\n' + 'Order Date: ' + time.strftime('%d/%m/%Y %H:%M', time.gmtime(int(item.date_time) / 1000.0)) + '\n' + 'Order Status: ' + status + '\n'
                itemInfo = itemInfo + 'Item Name: ' + item.product_name + '\n' + 'Item Category: ' + item.category + ' ' + item.subcategory + '\n' + 'Item Price: ' + item.price + ' SGD' + '\n'
                itemInfo = itemInfo + 'Quantity: ' + item.quantity + '\n' + 'Store: ' + item.store_name
                info = 'Hi, I upgraded your order on ORION.\n' + itemInfo + '\nPlease check.'

                toids = []
                toids.append(item.member_id)
                sendMessage(member_id, toids, info, 'order_upgrade')
                registerNotification(item.member_id, info, member_id, member.name, member.email, member.phone_number, '')

                sendFCMPushNotification(item.member_id, member_id, info)


                itemsList = []
                items = OrderItem.objects.filter(vendor_id=member_id).order_by('-id')
                for item in items:
                    if item.status2 != 'canceled':
                        orders = Order.objects.filter(id=item.order_id)
                        if orders.count() > 0:
                            order = orders[0]
                            item.orderID = order.orderID
                            item.contact = order.phone_number
                            itemsList.append(item)
                serializer = OrderItemSerializer(itemsList, many=True)

                resp = {'result_code':'0', 'next':next, 'data':serializer.data}
                return HttpResponse(json.dumps(resp))
            else:
                resp = {'result_code':'1'}
                return HttpResponse(json.dumps(resp))
        else:
            resp = {'result_code':'1'}
            return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def orderById(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id', '1')
        order = Order.objects.get(id=order_id)

        items = OrderItem.objects.filter(order_id=order.pk)
        for item in items:
            vendors = Member.objects.filter(id=item.vendor_id)
            if vendors.count() > 0:
                vendor = vendors[0]
                item.contact = vendor.phone_number
        serializer = OrderItemSerializer(items, many=True)

        data = {
            'id':order.pk,
            'member_id':order.member_id,
            'orderID':order.orderID,
            'price':order.price,
            'unit':order.unit,
            'shipping':order.shipping,
            'date_time':order.date_time,
            'email':order.email,
            'address':order.address,
            'address_line':order.address_line,
            'latitude':order.latitude,
            'longitude':order.longitude,
            'phone_number':order.phone_number,
            'status':order.status,
            'discount':order.discount,
            'items':serializer.data,
        }

        resp = {'result_code':'0', 'data':data}
        return HttpResponse(json.dumps(resp))



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def storeOrderItemsToPay(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        order_id = request.POST.get('order_id', '1')
        store_id = request.POST.get('store_id', '1')
        itemsList = []
        items = OrderItem.objects.filter(member_id=member_id, order_id=order_id, store_id=store_id).order_by('-id')
        for item in items:
            orders = Order.objects.filter(id=item.order_id)
            order = None
            if orders.count() > 0:
                order = orders[0]
            if order is not None:
                item.orderID = order.orderID
                vendors = Member.objects.filter(id=item.vendor_id)
                vendor = None
                if vendors.count() > 0:
                    vendor = vendors[0]
                    item.contact = vendor.phone_number
                    if item.payment_status != 'pay':
                        itemsList.append(item)
        serializer = OrderItemSerializer(itemsList, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getPayments(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        paids = Paid.objects.filter(member_id=member_id).order_by('-id')
        for paid in paids:
            stores = Store.objects.filter(id=paid.store_id)
            if stores.count() > 0:
                store = stores[0]
                paid.store_name = store.name
            items = OrderItem.objects.filter(paid_id=paid.pk)
            paid.items = str(items.count())
        serializer = PaidSerializer(paids, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def paidItems(request):
    if request.method == 'POST':
        paid_id = request.POST.get('paid_id', '1')
        role = request.POST.get('role', '')
        itemsList = []
        items = OrderItem.objects.filter(paid_id=paid_id).order_by('-id')
        for item in items:
            orders = Order.objects.filter(id=item.order_id)
            order = None
            if orders.count() > 0:
                order = orders[0]
            if order is not None:
                item.orderID = order.orderID
                if role == 'customer':
                    vendors = Member.objects.filter(id=item.vendor_id)
                    vendor = None
                    if vendors.count() > 0:
                        vendor = vendors[0]
                        item.contact = vendor.phone_number
                elif role == 'vendor':
                    members = Member.objects.filter(id=item.member_id)
                    member = None
                    if members.count() > 0:
                        member = members[0]
                        item.contact = member.phone_number
                itemsList.append(item)
        serializer = OrderItemSerializer(itemsList, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp))



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getCustomerPayments(request):
    if request.method == 'POST':
        vendor_id = request.POST.get('vendor_id', '1')
        paids = Paid.objects.filter(vendor_id=vendor_id).order_by('-id')
        for paid in paids:
            stores = Store.objects.filter(id=paid.store_id)
            if stores.count() > 0:
                store = stores[0]
                paid.store_name = store.name
            items = OrderItem.objects.filter(paid_id=paid.pk)
            paid.items = str(items.count())
        serializer = PaidSerializer(paids, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def refundPayment(request):
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    if request.method == 'POST':
        paid_id = request.POST.get('paid', '1')
        paids = Paid.objects.filter(id=paid_id)
        if paids.count() > 0:
            paid = paids[0]
            if paid.transfer_id != '':
                reversal = stripe.Transfer.create_reversal(paid.transfer_id)
                if reversal is not None:
                    refund = stripe.Refund.create(charge=paid.charge_id)
                    if refund is not None:
                        paid.payment_status = 'refund'
                        paid.save()
                        items = OrderItem.objects.filter(paid_id=paid.pk)
                        for item in items:
                            item.payment_status = 'refund'
                            item.save()

                        member = Member.objects.get(id=paid.member_id)
                        vendor = Member.objects.get(id=paid.vendor_id)
                        store = Store.objects.get(id=paid.store_id)
                        itemInfo = 'Order ID: ' + paid.orderID + '\n' + 'Store Name: ' + store.name + '\n' + 'Amount: ' + str(round(float(paid.paid_amount)/100, 2)) + 'SGD including the application fee 10%'
                        info = 'Hi ' + member.name + ', I refunded you the payment on this order:\n' + itemInfo + '\nThe refund processing will take some time.\nPlease check it kindly.'
                        toids = []
                        toids.append(member.pk)
                        sendMessage(paid.vendor_id, toids, info, 'refund')
                        registerNotification(member.pk, info, paid.vendor_id, vendor.name, vendor.email, vendor.phone_number, '')

                        sendFCMPushNotification(member.pk, vendor.pk, info)

                        resp = {'result_code':'0'}
                        return HttpResponse(json.dumps(resp))

            else:
                resp = {'result_code':'1'}
                return HttpResponse(json.dumps(resp))
        else:
            resp = {'result_code':'1'}
            return HttpResponse(json.dumps(resp))



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def setLocation(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        lat = request.POST.get('latitude', '')
        lng = request.POST.get('longitude', '')
        address = request.POST.get('address', '')
        area = request.POST.get('area', '')
        country = request.POST.get('country', '')

        member = Member.objects.get(id=member_id)

        dlocs = DriverLocation.objects.filter(member_id=member_id)
        dloc = None
        if dlocs.count() == 0:
            dloc = DriverLocation()
            dloc.member_id = member_id
            dloc.name = member.name
        else: dloc = dlocs[0]

        if dloc is not None:
            if lat != '': dloc.latitude = lat
            if lng != '': dloc.longitude = lng
            if address != '': dloc.address = address
            if country != '': dloc.country = country
            if area != '': dloc.area = area
            dloc.save()

            shareRealTimeLocation(member.pk, lat, lng)

            resp = {'result_code':'0', 'lat': str(dloc.latitude), 'lng': str(dloc.longitude)}

        return HttpResponse(json.dumps(resp))



def shareRealTimeLocation(member_id, lat, lng):
    members = Member.objects.filter(id=member_id)
    if members.count() > 0:
        member = members[0]

        db = firebase.database()

        data = {
            "time":str(int(round(time.time() * 1000))),
            "member_id": str(member.pk),
            "lat": lat,
            "lng": lng
        }

        db.child("driverloc").child(str(member.pk)).remove()
        db.child("driverloc").child(str(member.pk)).push(data)



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def setDriverAvailable(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        sts = request.POST.get('status', '')
        resp = {'result_code':'1'}
        members = Member.objects.filter(id=member_id)
        if members.count() > 0:
            member = members[0]
            member.status = sts
            member.save()

            resp = {'result_code':'0'}

        return HttpResponse(json.dumps(resp))



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getDrivers(request):
    if request.method == 'POST':
        drivers = Member.objects.filter(role='driver')
        for driver in drivers:
            if driver.address == '' or driver.latitude == '':
                driverLocations = DriverLocation.objects.filter(member_id=driver.pk)
                if driverLocations.count() > 0:
                    driverLocation = driverLocations[0]
                    driver.address = driverLocation.address
                    driver.latitude = driverLocation.latitude
                    driver.longitude = driverLocation.longitude
        serializer = MemberSerializer(drivers, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp))



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def preparedOrderItems(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        itemsList = []
        items = OrderItem.objects.filter(vendor_id=member_id).order_by('-id')
        for item in items:
            if item.status2 != 'canceled':
                orders = Order.objects.filter(id=item.order_id)
                if orders.count() > 0:
                    order = orders[0]
                    item.orderID = order.orderID
                    item.contact = order.phone_number
                    if item.status == 'prepared': itemsList.append(item)
        serializer = OrderItemSerializer(itemsList, many=True)
        resp = {'result_code':'0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp))



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def requestPreparedOrderToDriver(request):

    if request.method == 'POST':
        member_id = request.POST.get('member_id', '0')
        driver_id = request.POST.get('driver_id', '0')

        itemsStr = request.POST.get('itemsStr', '')

        preparedOrders = PreparedOrder.objects.filter(member_id=member_id, driver_id=driver_id, items_str=itemsStr, status='')
        if preparedOrders.count() > 0:
            resp = {'result_code': '2'}
            return HttpResponse(json.dumps(resp))
        else:
            preparedOrders = PreparedOrder.objects.filter(member_id=member_id, driver_id=driver_id, items_str=itemsStr, status='rejected')
            if preparedOrders.count() > 0:
                resp = {'result_code': '3'}
                return HttpResponse(json.dumps(resp))

        member = Member.objects.get(id=member_id)
        driver = Member.objects.get(id=driver_id)

        stores = Store.objects.filter(member_id=member.pk)
        if stores.count() > 0:
            store = stores[0]

        preparedOrder = PreparedOrder()
        preparedOrder.member_id = member_id
        preparedOrder.driver_id = driver_id
        preparedOrder.items_str = itemsStr
        preparedOrder.date_time = str(int(round(time.time() * 1000)))
        preparedOrder.status = ''
        preparedOrder.save()

        try:
            decoded = json.loads(itemsStr)
            for item_data in decoded['itemIds']:

                item_id = item_data['item_id']

                pitem = PreparedOrderItem()
                pitem.porder_id = preparedOrder.pk
                pitem.item_id = item_id
                pitem.save()

            info = 'Hi ' + driver.name + ', I sent you my prepared order for delivery. Please check them and accept.' + '\nStore: ' + store.name + '\nAddress: ' + store.address + '\nDelivery: ' + store.delivery_days + ' days' + '\nVendor: ' + member.name
            toids = []
            toids.append(driver_id)
            sendMessage(member_id, toids, info, 'request_driver')
            registerNotification(driver_id, info, member_id, member.name, member.email, member.phone_number, '')
            sendFCMPushNotification(driver_id, member_id, info)

            resp = {'result_code':'0'}
            return HttpResponse(json.dumps(resp))

        except:
            resp = {'result_code': '1'}
            return HttpResponse(json.dumps(resp))





@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getStoreOrders(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        preparedOrders = PreparedOrder.objects.filter(driver_id=member_id).order_by('-id')
        preparedOrderList = []
        for porder in preparedOrders:
            if porder.status != 'rejected':
                vendor_id = porder.member_id
                stores = Store.objects.filter(member_id=vendor_id)

                if stores.count() > 0:
                    store = stores[0]
                    serializer = StoreSerializer(store, many=False)
                    items = PreparedOrderItem.objects.filter(porder_id=porder.pk)
                    data = {
                        'id':porder.pk,
                        'date_time':porder.date_time,
                        'status':porder.status,
                        'items_count':str(items.count()),
                        'store':serializer.data
                    }

                    preparedOrderList.append(data)

        resp = {'result_code':'0', 'data':preparedOrderList}

        return HttpResponse(json.dumps(resp))



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def getVendorOrderItems(request):
    if request.method == 'POST':

        porder_id = request.POST.get('porder_id', '1')

        porders = PreparedOrder.objects.filter(id=porder_id)
        if porders.count() > 0:
            porder = porders[0]
            pitems = PreparedOrderItem.objects.filter(porder_id=porder.pk).order_by('-id')
            orderItemList = []
            for pitem in pitems:
                orderItems = OrderItem.objects.filter(id=pitem.item_id)
                if orderItems.count() > 0:
                    item = orderItems[0]
                    if item.status2 != 'canceled':
                        orders = Order.objects.filter(id=item.order_id)
                        if orders.count() > 0:
                            order = orders[0]
                            item.orderID = order.orderID
                            item.contact = order.phone_number
                            orderItemList.append(item)
            serializer = OrderItemSerializer(orderItemList, many=True)
            resp = {'result_code':'0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp))

        else:
            resp = {'result_code':'1'}
            return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def processVendorOrder(request):

    if request.method == 'POST':
        porder_id = request.POST.get('porder_id', '0')
        option = request.POST.get('option', '')

        itemsStr = request.POST.get('itemsStr', '')

        preparedOrders = PreparedOrder.objects.filter(id=porder_id)
        if preparedOrders.count() > 0:
            porder = preparedOrders[0]
            porder.status = option
            porder.save()

            if option == 'accepted':

                member = Member.objects.get(id=porder.member_id)
                driver = Member.objects.get(id=porder.driver_id)

                stores = Store.objects.filter(member_id=member.pk)
                if stores.count() > 0:
                    store = stores[0]

                try:
                    decoded = json.loads(itemsStr)
                    for item_data in decoded['itemIds']:

                        item_id = item_data['item_id']

                        orderItems = OrderItem.objects.filter(id=item_id)
                        if orderItems.count() > 0:
                            item = orderItems[0]
                            if item.status == 'prepared':
                                item.status = 'ready'

                            item.save()

                            orders = Order.objects.filter(id=item.order_id)
                            if orders.count() > 0:
                                order = orders[0]
                                status = 'Order Ready'
                                itemInfo = 'Order ID: ' + order.orderID + '\n' + 'Order Date: ' + time.strftime('%d/%m/%Y %H:%M', time.gmtime(int(item.date_time) / 1000.0)) + '\n' + 'Order Status: ' + status + '\n'
                                itemInfo = itemInfo + 'Item Name: ' + item.product_name + '\n' + 'Item Category: ' + item.category + ' ' + item.subcategory + '\n' + 'Item Price: ' + item.price + ' SGD' + '\n'
                                itemInfo = itemInfo + 'Quantity: ' + item.quantity + '\n' + 'Store: ' + item.store_name
                                info = 'Hi, I upgraded your order on ORION.\n' + itemInfo + '\nPlease check.'

                                toids = []
                                toids.append(item.member_id)
                                sendMessage(member.pk, toids, info, 'order_upgrade')
                                registerNotification(item.member_id, info, member.pk, member.name, member.email, member.phone_number, '')

                                sendFCMPushNotification(item.member_id, member.pk, info)


                    info = 'Hi ' + member.name + ', I am happy to notify you that I accepted your delivery order to be ready.\nI will process your order successfully soon.\nPlease track the items.' + driver.name
                    toids = []
                    toids.append(member.pk)
                    sendMessage(driver.pk, toids, info, 'driver_process')
                    registerNotification(member.pk, info, driver.pk, driver.name, driver.email, driver.phone_number, '')

                    sendFCMPushNotification(member.pk, driver.pk, info)

                    resp = {'result_code':'0'}
                    return HttpResponse(json.dumps(resp))

                except:
                    resp = {'result_code': '1'}
                    return HttpResponse(json.dumps(resp))

            elif option == 'rejected':
                info = 'Hi ' + member.name + ', I am unhappy to notify you that I rejected your delivery order unfortunately.\nI couldn\'t accept it due to my own issues. Please find another driver.\nI am much sorry.\n' + driver.name
                toids = []
                toids.append(member.pk)
                sendMessage(driver.pk, toids, info, 'driver_process')
                registerNotification(member.pk, info, driver.pk, driver.name, driver.email, driver.phone_number, '')

                sendFCMPushNotification(member.pk, driver.pk, info)

                resp = {'result_code':'0'}
                return HttpResponse(json.dumps(resp))
        else:
            resp = {'result_code': '1'}
            return HttpResponse(json.dumps(resp))




@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def confirmDelivered(request):
    if request.method == 'POST':
        porder_id = request.POST.get('porder_id', '0')
        item_id = request.POST.get('item_id', '1')
        items = OrderItem.objects.filter(id=item_id)
        if items.count() > 0:
            item = items[0]
            item.status = 'delivered'
            item.status_time = str(int(round(time.time() * 1000)))
            item.save()

            preparedOrders = PreparedOrder.objects.filter(id=porder_id)
            if preparedOrders.count() > 0:
                porder = preparedOrders[0]

                pitems = PreparedOrderItem.objects.filter(porder_id=porder.pk)
                deliveredList = []
                for pitem in pitems:
                    if pitem.item_id == item_id:
                        pitem.status = 'delivered'
                        pitem.save()
                    if pitem.status == 'delivered':
                        deliveredList.append(pitem)

                if len(deliveredList) == pitems.count():
                    porder.status = 'delivered'
                    porder.save()

                member = Member.objects.get(id=porder.member_id)
                driver = Member.objects.get(id=porder.driver_id)

                orders = Order.objects.filter(id=item.order_id)
                if orders.count() > 0:
                    order = orders[0]
                    status = 'Order Delivered'
                    itemInfo = 'Order ID: ' + order.orderID + '\n' + 'Order Date: ' + time.strftime('%d/%m/%Y %H:%M', time.gmtime(int(item.date_time) / 1000.0)) + '\n' + 'Order Status: ' + status + '\n'
                    itemInfo = itemInfo + 'Item Name: ' + item.product_name + '\n' + 'Item Category: ' + item.category + ' ' + item.subcategory + '\n' + 'Item Price: ' + item.price + ' SGD' + '\n'
                    itemInfo = itemInfo + 'Quantity: ' + item.quantity + '\n' + 'Store: ' + item.store_name
                    info = 'Hi, I upgraded your order on ORION.\n' + itemInfo + '\nPlease check.'

                    toids = []
                    toids.append(item.member_id)
                    sendMessage(member.pk, toids, info, 'order_upgrade')
                    registerNotification(item.member_id, info, member.pk, member.name, member.email, member.phone_number, '')

                    sendFCMPushNotification(item.member_id, member.pk, info)

                    customer = Member.objects.get(id=item.member_id)
                    info = 'Hi ' + member.name + ', I delivered your order item to this customer successfully.\n' + 'Customer: ' + customer.name + '\n' + 'Address: ' + item.address + '\n'
                    info = info + item.address_line + '\n'
                    info = info + itemInfo + '\nPlease check.'

                    toids = []
                    toids.append(member.pk)
                    sendMessage(driver.pk, toids, info, 'driver_process')
                    registerNotification(member.pk, info, driver.pk, driver.name, driver.email, driver.phone_number, '')

                    sendFCMPushNotification(member.pk, driver.pk, info)

                    resp = {'result_code':'0'}
                    return HttpResponse(json.dumps(resp))
                else:
                    resp = {'result_code':'1'}
                    return HttpResponse(json.dumps(resp))
            else:
                resp = {'result_code':'1'}
                return HttpResponse(json.dumps(resp))
        else:
            resp = {'result_code':'1'}
            return HttpResponse(json.dumps(resp))

























































































































