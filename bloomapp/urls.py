from . import views
from django.urls import path

urlpatterns = [
      path('',views.home,name='home'),
      path('signup',views.signup,name='signup'),
      path('signin_page/',views.signin_page,name='signin_page'),
      path('about_us/',views.about_us,name='about_us'),
      path('product_search/', views.product_search, name='product_search'),
      path('usercreate/',views.usercreate,name='usercreate'),
      path('signin/',views.signin,name='signin'),
      path('admin_home_page/',views.admin_home_page,name='admin_home_page'),
      path('logout/',views.logout,name="logout"),
      path('category_page/',views.category_page,name='category_page'),
      path('categories/<str:category_name>/',views.categories, name='categories'),
      path('fashion_categories_view/<str:category_names>/',views. fashion_categories_view, name='fashion_categories_view'),
      path('electronics_categories_view/<str:category_names>/',views. electronics_categories_view, name='electronics_categories_view'),
      path('appliances_categories_view/<str:category_names>/',views. appliances_categories_view, name='appliances_categories_view'),
      path('productpage/',views.productpage,name='productpage'),
      path('p_editpage/<int:pk>',views.p_editpage,name='p_editpage'),
      path('p_edit_form/<int:pk>',views.p_edit_form,name='p_edit_form'),
      path('p_delete_form/<int:pk>',views.p_delete_form,name='p_delete_form'),
      path('ad_userform/<int:pk>',views.ad_userform,name='ad_userform'),
      path('UserDetails/',views.UserDetails,name='UserDetails'),
      path('ad_useredit/<int:pk>',views.ad_useredit,name='ad_useredit'),
      path('ad_userdelete/<int:pk>',views.ad_userdelete,name='ad_userdelete'),
      path('contact_view/',views.contact_view,name='contact_view'),
      path('ad_contact/',views.ad_contact,name='ad_contact'),
      path('allproducts/', views.allproducts, name='allproducts'),
      path('product_detail/<int:pk>/', views.product_detail, name='product_detail'),
      path('cart/', views.cart, name='cart'),
      path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
      path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
      path('update-cart/<int:pk>/', views.update_cart, name='update_cart'),
      path('place-order/', views.place_order, name='place_order'),
      path('place-order_page/', views.place_order_page, name='place_order_page'),
      path('order_success/', views.order_success, name='order_success'),
      path('ordered_items/', views.ordered_items, name='ordered_items'),
      path('update_order_status/<int:ordered_item_id>/',views.update_order_status, name='update_order_status'),
      # path('remove_order_flag/', views.remove_order_flag, name='remove_order_flag'),
      path('user_ordered_items/', views.user_ordered_items, name='user_ordered_items'),
      path('confirm_order/<int:order_id>/', views.confirm_order, name='confirm_order'),
      path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
      path('wishlist/', views.wishlist, name='wishlist'),
      path('add_to_wishlist/<int:pk>/', views.add_to_wishlist, name='add_to_wishlist'),
      path('remove_from_wishlist/<int:pk>/', views.remove_from_wishlist, name='remove_from_wishlist'),

]