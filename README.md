# ⚡ Nexus Hardware E-Commerce

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

O **Nexus Hardware E-Commerce** é uma plataforma de comércio eletrônico robusta e completa desenvolvida com **Django**, inspirada nas principais referências do mercado nacional e internacional de informática de alta performance (como Pichau, Terabyte e Kabum). 

O projeto é focado na comercialização de componentes de computador entusiasta, placas de vídeo de última geração, processadores, memórias de alta frequência, periféricos competitivos e setups pré-montados com calibração de laboratório.

---

## 🎯 Funcionalidades Principais

- **🏠 Vitrine Dinâmica (Home)**:
  - Destaque hero com telemetria ao vivo de componentes topo de linha (*RTX 4090 OC / Ryzen 9 7950X3D*).
  - Grid de vantagens institucionais (garantia de 3 anos, envio expresso blindado, montagem em laboratório e 15% de desconto no PIX).
  - Carrossel e vitrine de lançamentos e ofertas relâmpago (*HOT Deals*).
  - Navegação rápida por categorias.

- **🔍 Catálogo & Filtros Avançados**:
  - Busca textual em tempo real por nome, marca, SKU e especificações técnicas.
  - Filtros dinâmicos laterais: por categoria, marca/fabricante, disponibilidade física imediata e faixa de preço configurável.
  - Ordenação dinâmica (menor preço à vista, maior preço, mais recentes e alfabética).
  - Paginação fluida e contagem de SKUs ativos.

- **⚡ Detalhes do Produto**:
  - Galeria de imagens de alta fidelidade com alternador dinâmico de miniaturas.
  - Matriz de telemetria e especificações técnicas completas estruturada em formato tabular.
  - Exibição de preço com 15% de desconto à vista no PIX e parcelamento em até 10x sem juros.
  - Simulador de frete e prazos de entrega (Nexus Express, Sedex e PAC).
  - Vitrine de produtos relacionados da mesma categoria.

- **🛒 Carrinho de Compras & Cupons**:
  - Controle de quantidade (+ / -) e remoção instantânea de itens.
  - Validação e aplicação de cupons de desconto (`NEXUS10` para 10% OFF e `PROMO15` para 15% OFF).
  - Cálculo automático de subtotais e totais à vista.
  - Suporte desacoplado a sessões anônimas e migração automática para a conta após login.

- **🔒 Checkout & Conclusão de Pedido**:
  - Formulário completo de endereço de entrega com validação de campos.
  - Seleção de método de pagamento (PIX Instantâneo, Cartão de Crédito ou Boleto Bancário).
  - Tela de confirmação com geração de número de pedido rastreável (`NX-YYYYMMDD-XXXXXX`), instruções completas e mock de QR Code PIX "Copia e Cola".

- **👤 Autenticação & Painel do Cliente**:
  - Cadastro de novos clientes com validação de dados e senhas seguras.
  - Autenticação e encerramento seguro de sessão.
  - Painel **Minha Conta**: histórico detalhado de pedidos, status em tempo real e dados de perfil.

---

## 🎨 Identidade Visual: *Stealth / Performance*

O projeto adota o conceito visual **Stealth Dark Tech**, abandonando o excesso de iluminação RGB tradicional em favor de uma estética tática, limpa e de alta precisão inspirada na aviação e na engenharia mecânica.

| Elemento | Tom / Cor | Código Hex | Aplicação |
| :--- | :--- | :--- | :--- |
| **Fundo Principal (Canvas)** | Cinza Grafite Profundo | `#18181B` / `#131316` | Absorção de ruído visual e contraste com produtos |
| **Cards & Superfícies** | Cinza Neutro / Zinc | `#27272A` / `#1F1F22` | Containers, gavetas contextuais e módulos |
| **Bordas Estruturais** | Cinza Escuro de Contorno | `#3F3F46` | Delimitação de 1px com precisão milimétrica |
| **Destaque / Ação (CTA)** | Verde Esmeralda Neon | `#10B981` / `#4EDEA3` | Botões primários, telemetria e badges ativos |
| **Texto Primário** | Branco Gelo | `#F9FAFB` | Títulos, preços destacados e leitura acessível |
| **Texto Secundário** | Cinza Claro / Frio | `#9CA3AF` | Metadados, descrições secundárias e legendas |

### Tipografia
- **Headlines & Componentes**: `Space Grotesk`
- **Corpo & Legibilidade**: `Inter`
- **Telemetria, Clocks, Moeda e SKUs**: `JetBrains Mono`

---

## 🛠️ Tecnologias Utilizadas

- **Back-end**:
  - [Python 3.11+](https://www.python.org/)
  - [Django](https://www.djangoproject.com/) (MTV Architecture, ORM, Auth, Messages)
- **Front-end**:
  - HTML5 Semântico com Django Template Language (DTL)
  - CSS3 & [Tailwind CSS](https://tailwindcss.com/)
  - JavaScript Vanilla (atalho `Ctrl + K`, galeria dinâmica, dismiss de toasts)
  - Google Material Symbols & Google Fonts
  - Design gerado e prototipado via **Stitch UI Design**
- **Servidor & Estáticos**:
  - [WhiteNoise](http://whitenoise.evans.io/) (serving e compressão de arquivos estáticos em produção)
  - WSGI Standard
- **Banco de Dados**:
  - SQLite (Ambiente de Desenvolvimento) / Compatível com PostgreSQL
- **Deploy & Versionamento**:
  - [Git](https://git-scm.com/) & [GitHub](https://github.com/)
  - [Vercel](https://vercel.com/) (Serverless Python Deployment)

---

## 📁 Estrutura do Projeto

```text
nexus_hardware/
├── manage.py                   # Ponto de entrada CLI do Django
├── requirements.txt            # Dependências do projeto Python
├── vercel.json                 # Configuração de build e rotas para deploy na Vercel
├── build_files.sh              # Script de build de pacotes e coleta de estáticos
├── DESIGN.md                   # Tokens e documentação do design system Stitch
├── README.md                   # Documentação oficial do projeto
│
├── nexus_hardware/             # Diretório central de configuração do Django
│   ├── __init__.py
│   ├── settings.py             # Configurações gerais, apps, static e middleware
│   ├── urls.py                 # Roteador central do projeto
│   ├── wsgi.py                 # Entrada WSGI (com export da variável 'app' para a Vercel)
│   └── asgi.py
│
├── store/                      # Aplicação principal de e-commerce
│   ├── admin.py                # Painel administrativo customizado
│   ├── apps.py
│   ├── context_processors.py   # Injeção global de carrinho e categorias
│   ├── forms.py                # Formulários de registro, login, checkout e cupom
│   ├── models.py               # Modelos relacionais (Category, Product, Cart, Order...)
│   ├── urls.py                 # Rotas da loja e endpoints de checkout
│   ├── views.py                # Controladores de negócio e renderização de views
│   │
│   ├── management/commands/
│   │   └── seed_data.py        # Script para popular dados realistas de hardware
│   │
│   ├── static/                 # Arquivos estáticos da loja
│   │   ├── css/theme.css       # Regras de tema e efeitos HUD
│   │   ├── js/app.js           # Interações client-side
│   │   └── images/             # Logotipos e ícones vetoriais
│   │
│   ├── templates/store/        # Templates específicos do app store
│   │   ├── home.html
│   │   ├── catalog.html
│   │   ├── product_detail.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── order_success.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── account.html
│   │
│   └── tests/                  # Suíte de testes automatizados
│       ├── __init__.py
│       ├── test_models.py      # Testes unitários de modelos e integridade
│       └── test_views.py       # Testes de integração de rotas e compras
│
└── templates/
    └── base.html               # Template base com header, navbar e footer Stitch
```

---

## 💻 Como Executar Localmente

### Pré-requisitos
- Python 3.11 ou superior instalado
- Git configurado

### Passo a Passo

1. **Clonar o Repositório**:
   ```bash
   git clone https://github.com/HugoGarciaUNIFEB/nexus_hardware.git
   cd nexus_hardware
   ```

2. **Criar e Ativar o Ambiente Virtual**:
   - **Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

3. **Instalar Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplicar Migrações do Banco de Dados**:
   ```bash
   python manage.py migrate
   ```

5. **Popular o Banco com Dados de Demonstração (Seed)**:
   ```bash
   python manage.py seed_data
   ```
   > Esse comando cria automaticamente 10 produtos de hardware entusiasta, categorias, cupons de desconto (`NEXUS10`, `PROMO15`) e as contas de teste:
   > - **Admin:** `admin` / `adminpassword123`
   > - **Cliente:** `cliente` / `clientepassword123`

6. **Iniciar o Servidor de Desenvolvimento**:
   ```bash
   python manage.py runserver
   ```
   Acesse a aplicação no navegador em: **`http://127.0.0.1:8000/`**

7. **Executar a Suíte de Testes**:
   ```bash
   python manage.py test store
   ```

---

## 🚀 Deploy na Vercel

O repositório já está configurado para deploy contínuo (*Serverless*) na Vercel através dos arquivos:

- **`vercel.json`**:
  Configura o handler `@vercel/python` apontando para `nexus_hardware/wsgi.py` e mapeia o diretório de estáticos `staticfiles` coletado pelo `build_files.sh`.
- **`build_files.sh`**:
  Executa a instalação das dependências do `requirements.txt` e o comando `collectstatic` no container de build da Vercel:
  ```bash
  pip install -r requirements.txt
  python3 manage.py collectstatic --noinput --clear
  ```
- **`nexus_hardware/wsgi.py`**:
  Exporta a variável `app = application` exigida pela runtime Python da Vercel.

### Variáveis de Ambiente na Vercel
Ao importar o projeto no Dashboard da Vercel, cadastre as seguintes variáveis em **Settings > Environment Variables**:

| Variável | Valor Recomendado | Descrição |
| :--- | :--- | :--- |
| `SECRET_KEY` | *(sua-chave-secreta-de-produção)* | Chave de segurança criptográfica do Django |
| `DEBUG` | `False` | Desativa o modo de depuração em produção |

---

## 📄 Licença & Direitos

Projeto desenvolvido para fins educacionais e de demonstração prática de engenharia de software e e-commerce de alta performance. Todos os direitos reservados.
