from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone

from .models import Category, Product, Cart, CartItem, Coupon, Order, OrderItem
from .forms import UserRegisterForm, UserLoginForm, CheckoutForm, CouponApplyForm, ShippingSimulationForm


def _get_or_create_cart(request):
    """
    Recupera ou instancia o carrinho atual associado ao usuário ou à sessão anônima.
    Realiza o merge de carrinhos de sessão quando o usuário faz login.
    """
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    if request.user.is_authenticated:
        # Recupera carrinho do usuário
        user_cart, _ = Cart.objects.get_or_create(user=request.user)

        # Se houver carrinho anônimo da sessão anterior, migra os itens
        session_cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()
        if session_cart and session_cart != user_cart:
            for item in session_cart.items.all():
                existing_item = user_cart.items.filter(product=item.product).first()
                if existing_item:
                    existing_item.quantity += item.quantity
                    existing_item.save()
                else:
                    item.cart = user_cart
                    item.save()
            if session_cart.coupon and not user_cart.coupon:
                user_cart.coupon = session_cart.coupon
                user_cart.save()
            session_cart.delete()

        return user_cart
    else:
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
        return cart


def home_view(request):
    """
    Vitrine Principal:
    - Produtos em destaque (RTX 4090, Ryzen 9 7950X3D, etc.)
    - Ofertas HOT da semana
    - Grid de vantagens
    - Categorias
    """
    featured_products = Product.objects.filter(is_featured=True)[:6]
    hot_deals = Product.objects.filter(is_hot_deal=True)[:4]
    latest_products = Product.objects.all().order_by('-created_at')[:8]
    categories = Category.objects.all()
    total_skus = Product.objects.count()

    context = {
        'featured_products': featured_products,
        'hot_deals': hot_deals,
        'latest_products': latest_products,
        'categories': categories,
        'total_skus': total_skus,
    }
    return render(request, 'store/home.html', context)


def catalog_view(request):
    """
    Catálogo Geral de Produtos com Filtros Dinâmicos e Busca:
    - Filtragem por categoria, marca, faixa de preço
    - Busca textual por nome, descrição e marca
    - Ordenação (menor preço, maior preço, mais recentes, nome)
    - Paginação de 9 itens por página
    """
    products = Product.objects.all()
    categories = Category.objects.all()

    # Extrai todas as marcas únicas para o filtro
    all_brands = Product.objects.values_list('brand', flat=True).distinct().order_by('brand')

    # Filtros
    q = request.GET.get('q', '').strip()
    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(brand__icontains=q) |
            Q(description__icontains=q) |
            Q(sku__icontains=q)
        )

    category_slug = request.GET.get('category', '').strip()
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    selected_brand = request.GET.get('brand', '').strip()
    if selected_brand:
        products = products.filter(brand__iexact=selected_brand)

    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    if min_price:
        try:
            products = products.filter(pix_price__gte=Decimal(min_price))
        except (ValueError, ArithmeticError):
            pass
    if max_price:
        try:
            products = products.filter(pix_price__lte=Decimal(max_price))
        except (ValueError, ArithmeticError):
            pass

    in_stock_only = request.GET.get('in_stock', '')
    if in_stock_only == '1':
        products = products.filter(stock__gt=0)

    # Ordenação
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_asc':
        products = products.order_by('pix_price')
    elif sort == 'price_desc':
        products = products.order_by('-pix_price')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    # Paginação
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'all_brands': all_brands,
        'selected_category': selected_category,
        'selected_brand': selected_brand,
        'q': q,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock_only': in_stock_only,
        'sort': sort,
        'total_count': products.count(),
    }
    return render(request, 'store/catalog.html', context)


def product_detail_view(request, slug):
    """
    Página do Produto:
    - Galeria e especificações técnicas
    - Cálculo de frete simulado
    - Produtos correlatos da mesma categoria
    """
    product = get_object_or_404(Product, slug=slug)
    gallery = product.gallery.all()
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    shipping_quote = None
    cep_queried = request.GET.get('cep', '').strip()
    if cep_queried:
        # Simulação realista de frete
        shipping_quote = [
            {'name': 'Nexus Express (Telemetria Prioritária)', 'days': '1 a 2 dias úteis', 'price': Decimal('24.90')},
            {'name': 'Sedex Express', 'days': '2 a 4 dias úteis', 'price': Decimal('32.50')},
            {'name': 'PAC Econômico', 'days': '5 a 8 dias úteis', 'price': Decimal('18.00')},
        ]

    context = {
        'product': product,
        'gallery': gallery,
        'related_products': related_products,
        'shipping_quote': shipping_quote,
        'cep_queried': cep_queried,
    }
    return render(request, 'store/product_detail.html', context)


def cart_view(request):
    """
    Visualização do Carrinho com listagem de itens, cupom e resumo de compra.
    """
    cart = _get_or_create_cart(request)
    coupon_form = CouponApplyForm()

    context = {
        'cart': cart,
        'coupon_form': coupon_form,
    }
    return render(request, 'store/cart.html', context)


def cart_add_view(request, product_id):
    """
    Adiciona produto ao carrinho ou incrementa sua quantidade.
    Suporta POST padrão ou AJAX.
    """
    if request.method != 'POST':
        return redirect('store:catalog')

    product = get_object_or_404(Product, id=product_id)
    cart = _get_or_create_cart(request)

    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    messages.success(request, f"{product.name} adicionado ao seu carrinho!")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': f"{product.name} adicionado ao carrinho!",
            'cart_count': cart.get_total_items(),
            'cart_subtotal': str(cart.get_pix_subtotal()),
        })

    next_url = request.POST.get('next', 'store:cart')
    return redirect(next_url)


def cart_update_view(request, item_id):
    """
    Atualiza quantidade de um item no carrinho (+ ou -).
    """
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id)
        cart = _get_or_create_cart(request)

        # Garante que o item pertence ao carrinho ativo
        if item.cart == cart:
            action = request.POST.get('action')
            if action == 'increment':
                item.quantity += 1
                item.save()
            elif action == 'decrement':
                if item.quantity > 1:
                    item.quantity -= 1
                    item.save()
                else:
                    item.delete()
                    messages.info(request, f"{item.product.name} removido do carrinho.")
            elif 'quantity' in request.POST:
                qty = int(request.POST.get('quantity', 1))
                if qty > 0:
                    item.quantity = qty
                    item.save()
                else:
                    item.delete()

    return redirect('store:cart')


def cart_remove_view(request, item_id):
    """
    Remove definitivamente um item do carrinho.
    """
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id)
        cart = _get_or_create_cart(request)
        if item.cart == cart:
            prod_name = item.product.name
            item.delete()
            messages.info(request, f"{prod_name} foi removido do seu carrinho.")

    return redirect('store:cart')


def coupon_apply_view(request):
    """
    Valida e aplica um cupom de desconto ao carrinho ativo.
    """
    if request.method == 'POST':
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code'].strip().upper()
            coupon = Coupon.objects.filter(code__iexact=code, active=True).first()
            if coupon and coupon.is_valid():
                cart = _get_or_create_cart(request)
                cart.coupon = coupon
                cart.save()
                messages.success(request, f"Cupom {coupon.code} aplicado com sucesso! ({coupon.discount_percent}% OFF)")
            else:
                messages.error(request, "Cupom inválido, expirado ou inativo.")
        else:
            messages.error(request, "Código de cupom inválido.")

    return redirect('store:cart')


def checkout_view(request):
    """
    Processo de Finalização de Compra (Checkout):
    - Coleta de dados de entrega e faturamento
    - Seleção do método de pagamento (PIX, Cartão ou Boleto)
    - Criação de Order e OrderItem
    """
    cart = _get_or_create_cart(request)
    if cart.get_total_items() == 0:
        messages.warning(request, "Seu carrinho está vazio. Adicione produtos antes de prosseguir.")
        return redirect('store:catalog')

    # Dados pré-preenchidos se o usuário estiver autenticado
    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user

            order.subtotal = cart.get_pix_subtotal()
            order.discount_amount = cart.get_discount_amount()
            order.shipping_fee = Decimal('24.90')  # Frete fixo Expresso Nexus
            order.total_amount = max(Decimal('0.00'), order.subtotal - order.discount_amount + order.shipping_fee)
            if cart.coupon:
                order.coupon_code = cart.coupon.code

            order.save()

            # Cria os itens do pedido a partir do carrinho
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    price_at_purchase=cart_item.product.pix_price,
                    quantity=cart_item.quantity
                )

            # Limpa o carrinho
            cart.items.all().delete()
            cart.coupon = None
            cart.save()

            messages.success(request, f"Pedido #{order.order_number} gerado com sucesso!")
            return redirect('store:order_success', order_number=order.order_number)
        else:
            messages.error(request, "Por favor, corrija os erros no formulário de entrega.")
    else:
        form = CheckoutForm(initial=initial_data)

    shipping_fee = Decimal('24.90')
    total_with_shipping = cart.get_total() + shipping_fee

    context = {
        'cart': cart,
        'form': form,
        'shipping_fee': shipping_fee,
        'total_with_shipping': total_with_shipping,
    }
    return render(request, 'store/checkout.html', context)


def order_success_view(request, order_number):
    """
    Tela de Confirmação do Pedido:
    - Apresenta resumo, código de pedido, QR Code mock para PIX e telemetria de entrega.
    """
    order = get_object_or_404(Order, order_number=order_number)
    context = {
        'order': order,
    }
    return render(request, 'store/order_success.html', context)


def register_view(request):
    """
    Cadastro de novos clientes com validação de senha e e-mail único.
    """
    if request.user.is_authenticated:
        return redirect('store:account')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Mescla carrinho anônimo se existir
            _get_or_create_cart(request)
            messages.success(request, f"Conta Nexus criada com sucesso! Bem-vindo(a), {user.username}.")
            return redirect('store:account')
        else:
            messages.error(request, "Erro ao criar conta. Verifique os campos abaixo.")
    else:
        form = UserRegisterForm()

    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    """
    Autenticação de Usuários com estilização Tailwind.
    """
    if request.user.is_authenticated:
        return redirect('store:account')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Mescla carrinho anônimo após login
            _get_or_create_cart(request)
            messages.success(request, f"Login efetuado com sucesso. Olá, {user.username}!")
            next_url = request.GET.get('next', 'store:account')
            return redirect(next_url)
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = UserLoginForm()

    return render(request, 'store/login.html', {'form': form})


def logout_view(request):
    """
    Encerramento de sessão do usuário.
    """
    logout(request)
    messages.info(request, "Sessão encerrada com sucesso.")
    return redirect('store:home')


@login_required
def account_view(request):
    """
    Painel do Usuário (Minha Conta / Meus Pedidos):
    - Histórico detalhado de pedidos
    - Informações de perfil
    """
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': user_orders,
    }
    return render(request, 'store/account.html', context)
