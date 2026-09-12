from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Category, Product, Cart, CartItem, Coupon, Order


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Placas de Vídeo",
            slug="placas-de-video",
            icon="developer_board"
        )
        self.product = Product.objects.create(
            category=self.category,
            name="RTX 4090 OC",
            slug="rtx-4090-oc",
            brand="NVIDIA",
            description="Placa extrema de 24GB",
            price=Decimal("15000.00"),
            pix_price=Decimal("12750.00"),
            stock=4,
            is_featured=True
        )
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@nexus.com",
            password="testpassword123",
            first_name="Test",
            last_name="User"
        )

    def test_home_view(self):
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "RTX 4090 OC")
        self.assertContains(response, "Nexus Hardware")

    def test_catalog_view_and_filters(self):
        response = self.client.get(reverse('store:catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "RTX 4090 OC")

        # Teste filtro por categoria
        response_cat = self.client.get(reverse('store:catalog') + f"?category={self.category.slug}")
        self.assertEqual(response_cat.status_code, 200)
        self.assertContains(response_cat, "RTX 4090 OC")

        # Teste busca textual
        response_search = self.client.get(reverse('store:catalog') + "?q=RTX")
        self.assertEqual(response_search.status_code, 200)
        self.assertContains(response_search, "RTX 4090 OC")

        # Teste busca sem resultados
        response_empty = self.client.get(reverse('store:catalog') + "?q=InexistenteXYZ")
        self.assertEqual(response_empty.status_code, 200)
        self.assertContains(response_empty, "Nenhum componente encontrado")

    def test_product_detail_view(self):
        response = self.client.get(reverse('store:product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, "Simular Prazo e Frete")

        # Simulação de frete
        response_frete = self.client.get(reverse('store:product_detail', kwargs={'slug': self.product.slug}) + "?cep=01310100")
        self.assertEqual(response_frete.status_code, 200)
        self.assertContains(response_frete, "Nexus Express")

        # Produto inexistente deve retornar 404
        response_404 = self.client.get(reverse('store:product_detail', kwargs={'slug': 'produto-fantasma'}))
        self.assertEqual(response_404.status_code, 404)

    def test_cart_operations(self):
        # 1. Adicionar ao carrinho
        add_url = reverse('store:cart_add', kwargs={'product_id': self.product.id})
        response = self.client.post(add_url, {'quantity': 1})
        self.assertEqual(response.status_code, 302)

        # 2. Visualizar carrinho
        cart_url = reverse('store:cart')
        cart_response = self.client.get(cart_url)
        self.assertEqual(cart_response.status_code, 200)
        self.assertContains(cart_response, "RTX 4090 OC")

        # 3. Atualizar quantidade
        cart = Cart.objects.first()
        item = cart.items.first()
        update_url = reverse('store:cart_update', kwargs={'item_id': item.id})
        self.client.post(update_url, {'action': 'increment'})
        item.refresh_from_db()
        self.assertEqual(item.quantity, 2)

        # 4. Remover do carrinho
        remove_url = reverse('store:cart_remove', kwargs={'item_id': item.id})
        self.client.post(remove_url)
        self.assertEqual(cart.items.count(), 0)

    def test_coupon_application(self):
        coupon = Coupon.objects.create(code="DESCONTO10", discount_percent=10, active=True)
        self.client.post(reverse('store:cart_add', kwargs={'product_id': self.product.id}), {'quantity': 1})

        coupon_url = reverse('store:coupon_apply')
        response = self.client.post(coupon_url, {'code': 'DESCONTO10'})
        self.assertEqual(response.status_code, 302)

        cart = Cart.objects.first()
        self.assertEqual(cart.coupon, coupon)

    def test_checkout_flow(self):
        # Adiciona item ao carrinho
        self.client.post(reverse('store:cart_add', kwargs={'product_id': self.product.id}), {'quantity': 1})

        # Submete formulário de checkout
        checkout_url = reverse('store:checkout')
        checkout_data = {
            'full_name': 'Carlos Cliente',
            'email': 'carlos@teste.com',
            'phone': '11999998888',
            'cpf': '12345678901',
            'cep': '01310-100',
            'address': 'Av Paulista',
            'number': '500',
            'neighborhood': 'Bela Vista',
            'city': 'São Paulo',
            'state': 'SP',
            'payment_method': 'PIX',
        }
        response = self.client.post(checkout_url, checkout_data)
        self.assertEqual(response.status_code, 302)

        # Verifica se o pedido foi criado
        order = Order.objects.filter(email='carlos@teste.com').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.total_amount, order.subtotal + order.shipping_fee)

    def test_user_authentication_flow(self):
        # 1. Login com credenciais válidas
        login_url = reverse('store:login')
        response = self.client.post(login_url, {'username': 'testuser', 'password': 'testpassword123'})
        self.assertEqual(response.status_code, 302)

        # 2. Acesso à Minha Conta
        account_url = reverse('store:account')
        acc_response = self.client.get(account_url)
        self.assertEqual(acc_response.status_code, 200)
        self.assertContains(acc_response, "Minha Conta")
        self.assertContains(acc_response, "testuser")

        # 3. Logout
        logout_url = reverse('store:logout')
        self.client.get(logout_url)
        acc_unauth = self.client.get(account_url)
        self.assertEqual(acc_unauth.status_code, 302)  # Redireciona para login
