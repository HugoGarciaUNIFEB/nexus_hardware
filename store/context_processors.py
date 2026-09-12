from decimal import Decimal
from .models import Category, Cart


def store_context(request):
    """
    Context processor para disponibilizar dados globais da loja:
    - Categorias para a barra de navegação
    - Contagem e total do carrinho para o cabeçalho
    """
    categories = Category.objects.all()
    
    cart = None
    cart_count = 0
    cart_subtotal = Decimal('0.00')

    # Identifica o carrinho por usuário ou sessão
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if session_key:
            cart = Cart.objects.filter(session_key=session_key).first()

    if cart:
        cart_count = cart.get_total_items()
        cart_subtotal = cart.get_pix_subtotal()

    return {
        'nav_categories': categories,
        'cart_count': cart_count,
        'cart_subtotal': cart_subtotal,
        'active_cart': cart,
    }
