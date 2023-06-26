from django.contrib import admin

from bloomapp.models import Cart, Category, Contact, Order, OrderFlag, OrderItem, Product, UserOrderedItem, UserProfile, Wishlist

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','name')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display=('id','user','phone_number','address')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('id','name','category','description','price','image')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=('id','name','email','message')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')
    list_filter = ('user', 'product')
    search_fields = ('user__username', 'product__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status')
    list_filter = ('user', 'status')
    search_fields = ('user__username',)

    actions = ['confirm_orders', 'cancel_orders']

    def confirm_orders(self, request, queryset):
        queryset.update(status='C', is_confirmed=True)

    confirm_orders.short_description = 'Confirm selected orders'

    def cancel_orders(self, request, queryset):
        queryset.update(status='X', is_cancelled=True)

    cancel_orders.short_description = 'Cancel selected orders'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')
    list_filter = ('order', 'product')
    search_fields = ('order__user__username', 'product__name')

class UserOrderdItemInline(admin.TabularInline):
    model = UserOrderedItem
    extra = 0

admin.site.register(OrderFlag)


@admin.register(UserOrderedItem)
class UserOrderedItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'ordered_item')
    list_filter = ('user',)
    search_fields = ('user__username', 'ordered_item__product__name')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    list_filter = ('user',)
    search_fields = ('user__username', 'product__name')