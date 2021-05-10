from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from orion import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^orion/', include('orion.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^registermember',views.registerMember,  name='registerMember'),
    url(r'^login',views.login,  name='login'),
    url(r'^registerStore',views.registerStore,  name='registerStore'),
    url(r'^getMyStore',views.getMyStore,  name='getMyStore'),
    url(r'^addBrand',views.addBrand,  name='addBrand'),
    url(r'^getStoreBrands',views.getStoreBrands,  name='getStoreBrands'),
    url(r'^editStore',views.editStore,  name='editStore'),
    url(r'^editBrand',views.editBrand,  name='editBrand'),
    url(r'^deleteBrand',views.deleteBrand,  name='deleteBrand'),
    url(r'^getBrandProducts',views.getBrandProducts,  name='getBrandProducts'),
    url(r'^uploadProduct',views.uploadProduct,  name='uploadProduct'),
    url(r'^getProductPictures',views.getProductPictures,  name='getProductPictures'),
    url(r'^deleteProduct',views.deleteProduct,  name='deleteProduct'),
    url(r'^editProduct',views.editProduct,  name='editProduct'),
    url(r'^delProductPicture',views.delProductPicture,  name='delProductPicture'),

    url(r'^forgotpassword', views.forgotpassword, name='forgotpassword'),
    url(r'^resetpassword/$', views.resetpassword, name='resetpassword'),
    url(r'^rstpwd', views.rstpwd, name='rstpwd'),

    url(r'^updatemember', views.updateMember, name='updateMember'),
    url(r'^newpayment', views.new_payment_account, name='new_payment_account'),
    url(r'^getpaymentstatus', views.getPaymentStatus, name='getPaymentStatus'),
    url(r'^completepayment',views.complete_payment_account,  name='complete_payment_account'),

    url(r'^getstores', views.getStores, name='getStores'),
    url(r'^getadvertisements', views.getAdvertisements, name='getAdvertisements'),
    url(r'^getstoreproducts', views.getStoreProducts, name='getStoreProducts'),

    url(r'^getStoreRatings',views.getStoreRatings,  name='getStoreRatings'),
    url(r'^placeStoreFeedback',views.placeStoreFeedback,  name='placeStoreFeedback'),

    url(r'^likeProduct',views.likeProduct,  name='likeProduct'),
    url(r'^unLikeProduct',views.unLikeProduct,  name='unLikeProduct'),

    url(r'^getcstores',views.getCategoryStores,  name='getCategoryStores'),
    url(r'^placeProductFeedback',views.placeProductFeedback,  name='placeProductFeedback'),
    url(r'^getProductRatings',views.getProductRatings,  name='getProductRatings'),
    url(r'^productInfo',views.productInfo,  name='productInfo'),

    url(r'^getPhones',views.getPhones,  name='getPhones'),
    url(r'^getAddresses',views.getAddresses,  name='getAddresses'),
    url(r'^getCoupons',views.getCoupons,  name='getCoupons'),

    url(r'^savePhoneNumber',views.savePhoneNumber,  name='savePhoneNumber'),
    url(r'^saveAddress',views.saveAddress,  name='saveAddress'),
    url(r'^delAddress',views.delAddress,  name='delAddress'),
    url(r'^delPhone',views.delPhone,  name='delPhone'),

    url(r'^uploadOrder',views.uploadOrder,  name='uploadOrder'),
    url(r'^uploadfcmtoken',views.fcm_insert,  name='fcm_insert'),

    url(r'^getNotifications',views.getNotifications,  name='getNotifications'),
    url(r'^delNotification',views.delNotification,  name='delNotification'),

    url(r'^getUserOrders',views.getUserOrders,  name='getUserOrders'),
    url(r'^delOrder',views.delOrder,  name='delOrder'),
    url(r'^userOrderItems',views.userOrderItems,  name='userOrderItems'),

    url(r'^receivedOrderItems',views.receivedOrderItems,  name='receivedOrderItems'),
    url(r'^cancelOrderItem',views.cancelOrderItem,  name='cancelOrderItem'),
    url(r'^progressOrderItem',views.progressOrderItem,  name='progressOrderItem'),
    url(r'^orderById',views.orderById,  name='orderById'),

    url(r'^storeOrderItemsToPay',views.storeOrderItemsToPay,  name='storeOrderItemsToPay'),

    url(r'^paybycard',views.paybycard,  name='paybycard'),
    url(r'^payFor',views.payFor,  name='payFor'),
    url(r'^getPaid',views.getPaid,  name='getPaid'),
    url(r'^getPayments',views.getPayments,  name='getPayments'),
    url(r'^paidItems',views.paidItems,  name='paidItems'),
    url(r'^getCustomerPayments',views.getCustomerPayments,  name='getCustomerPayments'),
    url(r'^refundPayment',views.refundPayment,  name='refundPayment'),

    url(r'^setLocation',views.setLocation,  name='setLocation'),
    url(r'^setDriverAvailable',views.setDriverAvailable,  name='setDriverAvailable'),
    url(r'^getDrivers',views.getDrivers,  name='getDrivers'),
    url(r'^preparedOrderItems',views.preparedOrderItems,  name='preparedOrderItems'),
    url(r'^requestPreparedOrderToDriver',views.requestPreparedOrderToDriver,  name='requestPreparedOrderToDriver'),
    url(r'^getStoreOrders',views.getStoreOrders,  name='getStoreOrders'),
    url(r'^getVendorOrderItems',views.getVendorOrderItems,  name='getVendorOrderItems'),
    url(r'^processVendorOrder',views.processVendorOrder,  name='processVendorOrder'),
    url(r'^confirmDelivered',views.confirmDelivered,  name='confirmDelivered'),

]


urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns=format_suffix_patterns(urlpatterns)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





























