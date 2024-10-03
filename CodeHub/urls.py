"""
URL configuration for CodeHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from store import views

#image importing

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    #registration

    path('registration/',views.SignUpView.as_view(),name='signup'),

    #login

    path('',views.SignInView.as_view(),name='signin'),

    #index

    path('index/',views.IndexView.as_view(),name='index'),

    #profile_eidt

    path('profile/<int:pk>/change/',views.UserProfileUpdateView.as_view(),name='profile-update'),

    #project_add

    path('project/add/',views.ProjectCreateView.as_view(),name='project_add'),

    #project-list

    path('works/all/',views.MyprojectListView.as_view(),name='myworks'),

    #project-delete

    path('work/<int:pk>/remove/',views.ProjectDeleteView.as_view(),name='work-delete'),

    #project-detail

    path('project/<int:pk>/',views.ProjectDetailView.as_view(),name='project-detail'),

    #Add to wishlist

    path('project/<int:pk>/wishlist/add/',views.AddToWishListView.as_view(),name='add-to-wishlist'),

    #Wish list items

    path('wishlist/summary/',views.MyCartListView.as_view(),name='my-cart'),

    #wishlist Delete

    path('wishlist/item/<int:pk>/remove/',views.WishListItemDeleteView.as_view(),name='cart-item-delete'),

    #cart / checkout

    path('checkout/',views.CheckOutView.as_view(),name='checkout'),

    #payment verification

    path('payment/verification/',views.PaymentVerificationView.as_view(),name='payment-verify'),

    #order_summary

    path('order/summary/',views.MyPurchaseView.as_view(),name='order-summary'),

    #review

    path('project/<int:pk>/review/add/',views.ReviewCreateView.as_view(),name='review-add')



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
