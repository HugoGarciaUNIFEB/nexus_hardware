# Project Plan: Nexus Hardware E-Commerce (Django)

> Task Slug: `nexus-hardware`  
> Data de Criação: 2026-09-12  
> Status: Planejamento Concluído — Aguardando Aprovação  

---

## 👥 Atribuições dos Agentes

| Agente | Domínio / Responsabilidade |
| :--- | :--- |
| `orchestrator` | Coordenação geral, conformidade de arquitetura e integração dos módulos |
| `database-architect` | Modelagem relacional (`Category`, `Product`, `ProductImage`, `Coupon`, `Cart`, `CartItem`, `Order`, `OrderItem`), índices e migrações |
| `backend-specialist` | Configurações Django, views de catálogo/busca/detalhes, autenticação, controle de carrinho por sessão/usuário, checkout e context processors |
| `test-engineer` | Criação da suíte de testes automatizados (`store/tests/`), validação CSRF em todos os formulários e verificação de arquivos estáticos |
| `debugger` | Monitoramento e correção de anomalias durante a execução dos testes |

---

## 🛠️ Detalhamento das Etapas de Execução

### Fase 1: Fundação do Projeto Django
- Inicializar a estrutura padrão Django: projeto `nexus_hardware` e app `store`.
- Configurar `settings.py` (banco de dados SQLite local com suporte a transações, templates com context processors globais para categorias e carrinho, static e media roots, tags de mensagens de alerta).
- Criar `DESIGN.md` e organizar pastas `store/templates/` e `store/static/` preservando os tokens do Stitch (*Stealth / Performance*).

### Fase 2: Modelagem de Dados (`database-architect`)
- `Category`: `name`, `slug`, `icon`, `description`.
- `Product`: `name`, `slug`, `brand`, `description`, `technical_specs` (JSON), `price`, `pix_price`, `stock`, `main_image`, `is_featured`, `is_hot_deal`, `category` (FK).
- `ProductImage`: `product` (FK), `image`, `caption`, `order`.
- `Coupon`: `code`, `discount_percent`, `active`, `valid_until`.
- `Cart` & `CartItem`: persistência por sessão para anônimos e foreign key para usuários logados; cálculo de subtotais e totais.
- `Order` & `OrderItem`: dados de envio, método de pagamento, status, tracking e itens históricos.
- Executar `makemigrations` e `migrate`.

### Fase 3: Regras de Negócio e Views (`backend-specialist`)
- **Autenticação**: Formulários customizados para cadastro com validação de dados, login, logout e painel "Minha Conta" com histórico de pedidos.
- **Vitrine & Catálogo**:
  - `home_view`: Banner herói com specs de telemetria, produtos em destaque e categorias.
  - `catalog_view`: Busca textual (`q`), filtros por categoria, fabricante/marca e faixa de preço, ordenação e paginação.
- **Detalhes do Produto**:
  - `product_detail_view`: Galeria interativa de fotos, tabela de telemetria de specs, cálculo de parcelas vs desconto PIX e simulação de frete.
- **Carrinho & Checkout**:
  - Adição, incremento/decremento e remoção de itens.
  - Aplicação de cupom de desconto com validação.
  - Checkout com endereço, validação de campos e criação do pedido.
  - Tela de sucesso com status do pedido.

### Fase 4: Templates & Static Files (Design Stitch)
- Converter as telas geradas no Stitch para templates Django modulares (`base.html`, `home.html`, `catalog.html`, `product_detail.html`, `cart.html`, `checkout.html`, `order_success.html`, `login.html`, `register.html`, `account.html`).
- Garantir tags `{% static %}` para imagens e assets e `{% csrf_token %}` em formulários.

### Fase 5: Seed de Dados e Suíte de Testes (`test-engineer`)
- Comando `python manage.py seed_data` com dados realistas de hardware (RTX 4090, RTX 4080 Super, Ryzen 9 7950X3D, Core i9 14900K, memórias DDR5, etc.).
- Testes automatizados em `store/tests/test_models.py` e `store/tests/test_views.py`.
- Execução dos testes e verificação de integridade (`manage.py check`).
