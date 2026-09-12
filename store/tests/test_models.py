from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from store.models import Category, Product, Cart, CartItem, Coupon, Order, OrderItem


class ModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Placas de Vídeo",
            slug="placas-de-video",
            icon="developer_board"
        )
        self.product = Product.objects.create(
            category=self.category,
            name="RTX 4080 Super",
            slug="rtx-4080-super",
            brand="ASUS",
            description="Placa gráfica topo de linha",
            price=Decimal("8000.00"),
            pix_price=Decimal("6800.00"),
            stock=5,
            is_featured=True
        )
        self.user = User.objects.create_user(
            username="gamer1",
            email="gamer1@nexus.com",
            password="password123"
        )

    def test_category_slug_and_str(self):
        self.assertEqual(str(self.category), "Placas de Vídeo")
        cat2 = Category.objects.create(name="Processadores")
        self.assertEqual(cat2.slug, "processadores")

    def test_product_properties(self):
        self.assertEqual(str(self.product), "ASUS - RTX 4080 Super")
        self.assertTrue(self.product.sku.startswith("NX-"))
        self.assertEqual(self.product.discount_percent, 15)
        self.assertEqual(self.product.installment_price, Decimal("800.00"))

    def test_coupon_validity(self):
        coupon = Coupon.objects.create(
            code="TESTE10",
            discount_percent=10,
            active=True
        )
        self.assertTrue(coupon.is_valid())

        coupon.active = False
        coupon.save()
        self.assertFalse(coupon.is_valid())

    def test_cart_calculations(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        # 2x de 8000 = 16000 (a prazo), 2x 6800 = 13600 (PIX)
        self.assertEqual(cart.get_total_items(), 2)
        self.assertEqual(cart.get_subtotal(), Decimal("16000.00"))
        self.assertEqual(cart.get_pix_subtotal(), Decimal("13600.00"))

        # Aplicação de cupom de 10%
        coupon = Coupon.objects.create(code="DESC10", discount_percent=10)
        cart.coupon = coupon
        cart.save()

        # 10% de 13600 = 1360
        self.assertEqual(cart.get_discount_amount(), Decimal("1360.00"))
        self.assertEqual(cart.get_total(), Decimal("12240.00"))

    def test_order_creation_and_number(self):
        order = Order.objects.create(
            user=self.user,
            full_name="Gamer Teste",
            email="gamer1@nexus.com",
            phone="11999999999",
            cep="01000-000",
            address="Rua Teste",
            number="100",
            neighborhood="Centro",
            city="São Paulo",
            state="SP",
            subtotal=Decimal("6800.00"),
            shipping_fee=Decimal("24.90"),
            total_amount=Decimal("6824.90")
        )
        self.assertTrue(order.order_number.startswith("NX-"))
        self.assertEqual(order.status, "PENDING")
