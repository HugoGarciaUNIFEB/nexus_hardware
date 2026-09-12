from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Vitrine e Catálogo
    path('', views.home_view, name='home'),
    path('catalogo/', views.catalog_view, name='catalog'),
    path('produto/<slug:slug>/', views.product_detail_view, name='product_detail'),

    # Carrinho e Checkout
    path('carrinho/', views.cart_view, name='cart'),
    path('carrinho/adicionar/<int:product_id>/', views.cart_add_view, name='cart_add'),
    path('carrinho/atualizar/<int:item_id>/', views.cart_update_view, name='cart_update'),
    path('carrinho/remover/<int:item_id>/', views.cart_remove_view, name='cart_remove'),
    path('carrinho/cupom/', views.coupon_apply_view, name='coupon_apply'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('pedido/<str:order_number>/sucesso/', views.order_success_view, name='order_success'),

    # Autenticação e Conta
    path('cadastro/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('minha-conta/', views.account_view, name='account'),
]
