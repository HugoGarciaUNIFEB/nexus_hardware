import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


class Category(models.Model):
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Slug', max_length=120, unique=True)
    icon = models.CharField('Ícone Material Symbols', max_length=50, blank=True, default='memory')
    description = models.TextField('Descrição', blank=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Categoria')
    name = models.CharField('Nome do Produto', max_length=255)
    slug = models.SlugField('Slug', max_length=255, unique=True, db_index=True)
    sku = models.CharField('SKU', max_length=50, unique=True, blank=True)
    brand = models.CharField('Marca / Fabricante', max_length=100)
    description = models.TextField('Descrição Completa')
    technical_specs = models.JSONField('Especificações Técnicas', default=dict, blank=True)
    price = models.DecimalField('Preço a Prazo (R$)', max_digits=10, decimal_places=2)
    pix_price = models.DecimalField('Preço à Vista no PIX (R$)', max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField('Estoque Disponível', default=10)
    main_image = models.ImageField('Imagem Principal', upload_to='products/', blank=True, null=True)
    image_url = models.URLField('URL Externa da Imagem', max_length=500, blank=True, null=True)
    is_featured = models.BooleanField('Destaque na Vitrine', default=False)
    is_hot_deal = models.BooleanField('Oferta Quente (HOT)', default=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'slug']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return f"{self.brand} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.sku:
            self.sku = f"NX-{uuid.uuid4().hex[:8].upper()}"
        if not self.pix_price and self.price:
            # Padrão: 15% de desconto no PIX
            self.pix_price = (self.price * Decimal('0.85')).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)

    @property
    def get_image(self):
        if self.main_image and hasattr(self.main_image, 'url'):
            return self.main_image.url
        if self.image_url:
            return self.image_url
        return 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=800&q=80'

    @property
    def discount_percent(self):
        if self.price and self.pix_price and self.price > self.pix_price:
            diff = self.price - self.pix_price
            return int(round((diff / self.price) * 100))
        return 0

    @property
    def installment_price(self):
        if self.price:
            return (self.price / Decimal('10')).quantize(Decimal('0.01'))
        return Decimal('0.00')


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery', verbose_name='Produto')
    image = models.ImageField('Imagem', upload_to='products/gallery/', blank=True, null=True)
    image_url = models.URLField('URL Externa', max_length=500, blank=True, null=True)
    caption = models.CharField('Legenda', max_length=150, blank=True)
    order = models.PositiveIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Imagem da Galeria'
        verbose_name_plural = 'Imagens da Galeria'
        ordering = ['order']

    @property
    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        if self.image_url:
            return self.image_url
        return 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=800&q=80'


class Coupon(models.Model):
    code = models.CharField('Código do Cupom', max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField('Percentual de Desconto (%)', default=10)
    active = models.BooleanField('Ativo', default=True)
    valid_until = models.DateTimeField('Válido até', null=True, blank=True)

    class Meta:
        verbose_name = 'Cupom de Desconto'
        verbose_name_plural = 'Cupons de Desconto'

    def __str__(self):
        return f"{self.code} ({self.discount_percent}% OFF)"

    def is_valid(self):
        if not self.active:
            return False
        if self.valid_until and timezone.now() > self.valid_until:
            return False
        return True


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts', verbose_name='Usuário')
    session_key = models.CharField('Chave de Sessão', max_length=40, null=True, blank=True, db_index=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Cupom Aplicado')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'

    def __str__(self):
        return f"Carrinho #{self.id} - {'User: ' + self.user.username if self.user else 'Sessão: ' + str(self.session_key)}"

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

    def get_subtotal(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def get_pix_subtotal(self):
        return sum(item.get_pix_subtotal() for item in self.items.all())

    def get_discount_amount(self):
        if self.coupon and self.coupon.is_valid():
            subtotal = self.get_pix_subtotal()
            discount = (subtotal * Decimal(self.coupon.discount_percent) / Decimal('100')).quantize(Decimal('0.01'))
            return discount
        return Decimal('0.00')

    def get_total(self):
        subtotal = self.get_pix_subtotal()
        discount = self.get_discount_amount()
        return max(Decimal('0.00'), subtotal - discount)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Carrinho')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Produto')
    quantity = models.PositiveIntegerField('Quantidade', default=1)

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens do Carrinho'
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    def get_subtotal(self):
        return self.product.price * self.quantity

    def get_pix_subtotal(self):
        return self.product.pix_price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Aguardando Pagamento'),
        ('PAID', 'Pagamento Aprovado / Em Separação'),
        ('SHIPPED', 'Enviado / Em Trânsito'),
        ('DELIVERED', 'Entregue com Sucesso'),
        ('CANCELLED', 'Cancelado'),
    ]

    PAYMENT_CHOICES = [
        ('PIX', 'PIX Instantâneo (-15% OFF)'),
        ('CREDIT_CARD', 'Cartão de Crédito em até 10x'),
        ('BOLETO', 'Boleto Bancário'),
    ]

    order_number = models.CharField('Número do Pedido', max_length=32, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name='Usuário')

    # Dados do Comprador
    full_name = models.CharField('Nome Completo', max_length=150)
    email = models.EmailField('E-mail')
    phone = models.CharField('Telefone / WhatsApp', max_length=20)
    cpf = models.CharField('CPF', max_length=20, blank=True)

    # Endereço de Entrega
    cep = models.CharField('CEP', max_length=10)
    address = models.CharField('Endereço', max_length=255)
    number = models.CharField('Número', max_length=20)
    complement = models.CharField('Complemento', max_length=100, blank=True)
    neighborhood = models.CharField('Bairro', max_length=100)
    city = models.CharField('Cidade', max_length=100)
    state = models.CharField('Estado (UF)', max_length=2)

    # Dados Financeiros
    payment_method = models.CharField('Método de Pagamento', max_length=20, choices=PAYMENT_CHOICES, default='PIX')
    status = models.CharField('Status do Pedido', max_length=20, choices=STATUS_CHOICES, default='PENDING')
    subtotal = models.DecimalField('Subtotal (R$)', max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField('Frete (R$)', max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField('Desconto (R$)', max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField('Valor Total (R$)', max_digits=10, decimal_places=2)
    coupon_code = models.CharField('Cupom Utilizado', max_length=50, blank=True)
    tracking_code = models.CharField('Código de Rastreio', max_length=50, blank=True)

    created_at = models.DateTimeField('Data do Pedido', auto_now_add=True)
    updated_at = models.DateTimeField('Última Atualização', auto_now=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']

    def __str__(self):
        return f"Pedido #{self.order_number} - {self.full_name} (R$ {self.total_amount})"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"NX-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Pedido')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Produto')
    price_at_purchase = models.DecimalField('Preço Unitário (R$)', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Quantidade', default=1)

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Pedido #{self.order.order_number})"

    def get_subtotal(self):
        return self.price_at_purchase * self.quantity
