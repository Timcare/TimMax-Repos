from django.urls import path
from . import views
from .views import ProfileView

urlpatterns = [
    path('',views.main,name="main"),
    path('home/',views.home,name='home'),
    path('list/',views.list,name='list'),
    path('listing/<str:id>/',views.listing_view,name='listings'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('listing/<str:id>/edit',views.edit_view,name="edit"),
    path('listing/<str:id>/like',views.like_listing_view,name="like_listing"),
    path('listing/<str:id>/inquiry',views.inquire_listing_using_email,name="inquire_listing"),
]
