import uuid
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from store.models import Category, Product, ProductImage, Coupon, Order, OrderItem


class Command(BaseCommand):
    help = "Popula o banco de dados com categorias, produtos reais, cupons e usuários de teste"

    def handle(self, *args, **options):
        self.stdout.write("Inicializando seed do Nexus Hardware...")

        # 1. Usuários de Teste
        admin_user, admin_created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@nexushardware.com.br",
                "is_staff": True,
                "is_superuser": True,
                "first_name": "Administrador",
                "last_name": "Nexus",
            }
        )
        if admin_created:
            admin_user.set_password("adminpassword123")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Superusuário criado: admin / adminpassword123"))

        customer_user, cust_created = User.objects.get_or_create(
            username="cliente",
            defaults={
                "email": "cliente@nexushardware.com.br",
                "first_name": "Carlos Eduardo",
                "last_name": "Silva",
            }
        )
        if cust_created:
            customer_user.set_password("clientepassword123")
            customer_user.save()
            self.stdout.write(self.style.SUCCESS("Usuário cliente criado: cliente / clientepassword123"))

        # 2. Cupons de Desconto
        Coupon.objects.get_or_create(
            code="NEXUS10",
            defaults={"discount_percent": 10, "active": True}
        )
        Coupon.objects.get_or_create(
            code="PROMO15",
            defaults={"discount_percent": 15, "active": True}
        )
        self.stdout.write("Cupons de desconto configurados: NEXUS10 (10% OFF), PROMO15 (15% OFF)")

        # 3. Categorias
        categories_data = [
            {"name": "Processadores (CPUs)", "slug": "processadores", "icon": "memory", "desc": "Processadores topo de linha Intel e AMD com arquiteturas de ponta."},
            {"name": "Placas de Vídeo (GPUs)", "slug": "placas-de-video", "icon": "developer_board", "desc": "Placas gráficas GeForce RTX e Radeon para 4K e ray tracing extremo."},
            {"name": "Placas-Mãe", "slug": "placas-mae", "icon": "dashboard", "desc": "Motherboards enthusiast com VRMs de alta potência e suporte PCIe 5.0."},
            {"name": "Memórias & Armazenamento", "slug": "memorias-armazenamento", "icon": "storage", "desc": "Módulos DDR5 de alta frequência e SSDs NVMe de ultrarrápida leitura."},
            {"name": "Periféricos & Áudio", "slug": "perifericos-audio", "icon": "headphones", "desc": "Teclados com switches magnéticos e headsets com drivers audiófilos."},
            {"name": "Setups Prontos", "slug": "setups-prontos", "icon": "desktop_windows", "desc": "Workstations completas com calibração térmica e testes de estresse em laboratório."},
        ]

        cat_objs = {}
        for cdata in categories_data:
            cat, _ = Category.objects.get_or_create(
                slug=cdata["slug"],
                defaults={
                    "name": cdata["name"],
                    "icon": cdata["icon"],
                    "description": cdata["desc"],
                }
            )
            cat_objs[cdata["slug"]] = cat

        self.stdout.write("Categorias criadas com sucesso.")

        # 4. Produtos
        products_data = [
            {
                "category": cat_objs["placas-de-video"],
                "name": "GeForce RTX 4090 OC ROG Strix 24GB",
                "slug": "geforce-rtx-4090-oc-rog-strix-24gb",
                "sku": "NX-RTX4090-STRIX",
                "brand": "ASUS ROG",
                "description": "A mais poderosa placa de vídeo para entusiastas e criadores. Com 24GB GDDR6X, arquitetura Ada Lovelace, câmara de vapor patenteada e acabamento em alumínio usinado.",
                "price": Decimal("14999.00"),
                "pix_price": Decimal("12749.15"),
                "stock": 6,
                "is_featured": True,
                "is_hot_deal": True,
                "image_url": "https://images.unsplash.com/photo-1591488320449-011701bb6704?auto=format&fit=crop&w=800&q=80",
                "specs": {
                    "Arquitetura": "NVIDIA Ada Lovelace (4N TSMC)",
                    "VRAM": "24GB GDDR6X",
                    "Clock Boost": "2.640 MHz",
                    "Interface de Memória": "384-bit",
                    "Núcleos CUDA": "16.384",
                    "TDP": "450W",
                    "Conexões": "2x HDMI 2.1a, 3x DisplayPort 1.4a",
                }
            },
            {
                "category": cat_objs["placas-de-video"],
                "name": "GeForce RTX 4080 Super ASUS ROG Strix 16GB",
                "slug": "geforce-rtx-4080-super-asus-rog-strix-16gb",
                "sku": "NX-RTX4080S-STRIX",
                "brand": "ASUS ROG",
                "description": "Desempenho gráfico de elite para 4K a 144Hz. Refrigeração com 3 ventoinhas Axial-tech, backplate reforçado e BIOS duplo comutável.",
                "price": Decimal("8450.00"),
                "pix_price": Decimal("7182.50"),
                "stock": 10,
                "is_featured": True,
                "is_hot_deal": False,
                "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=800&q=80",
                "specs": {
                    "Arquitetura": "NVIDIA Ada Lovelace",
                    "VRAM": "16GB GDDR6X",
                    "Clock Boost": "2.580 MHz",
                    "Interface de Memória": "256-bit",
                    "Núcleos CUDA": "10.240",
                    "TDP": "320W",
                    "Conexões": "2x HDMI 2.1a, 3x DisplayPort 1.4a",
                }
            },
            {
                "category": cat_objs["placas-de-video"],
                "name": "AMD Radeon RX 7900 XTX Nitro+ 24GB",
                "slug": "amd-radeon-rx-7900-xtx-nitro-24gb",
                "sku": "NX-RX7900XTX-SAPPHIRE",
                "brand": "Sapphire",
                "description": "O ápice da arquitetura RDNA 3 com chiplets. 24GB de memória de alta velocidade, dissipador Vapor-X e iluminação ARGB sincronizável.",
                "price": Decimal("7990.00"),
                "pix_price": Decimal("6791.50"),
                "stock": 5,
                "is_featured": True,
                "is_hot_deal": False,
                "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80",
                "specs": {
                    "Arquitetura": "AMD RDNA 3 (Chiplet)",
                    "VRAM": "24GB GDDR6",
                    "Clock Boost": "2.680 MHz",
                    "Interface": "384-bit",
                    "TDP": "355W",
                    "Conexões": "2x HDMI 2.1, 2x DisplayPort 2.1",
                }
            },
            {
                "category": cat_objs["processadores"],
                "name": "AMD Ryzen 9 7950X3D (16 Núcleos / 32 Threads)",
                "slug": "amd-ryzen-9-7950x3d",
                "sku": "NX-RYZEN-7950X3D",
                "brand": "AMD",
                "description": "O processador definitivo para jogos e produção de conteúdo pesado. Com 144MB de cache combinado 3D V-Cache para máxima taxa de quadros e estabilidade de 1% low.",
                "price": Decimal("4590.00"),
                "pix_price": Decimal("3901.50"),
                "stock": 12,
                "is_featured": True,
                "is_hot_deal": True,
                "image_url": "https://images.unsplash.com/photo-1555680202-c86f0e12f086?auto=format&fit=crop&w=800&q=80",
                "specs": {
                    "Núcleos / Threads": "16 Cores / 32 Threads",
                    "Clock Base / Turbo": "4.2 GHz / 5.7 GHz",
                    "Cache Total": "144 MB (128MB L3 3D V-Cache)",
                    "Socket": "AM5",
                    "TDP": "120W",
                    "Suporte": "PCIe 5.0 e DDR5 Nativo",
                }
            },
            {
                "category": cat_objs["processadores"],
                "name": "Intel Core i9 14900K (24 Núcleos / 32 Threads)",
                "slug": "intel-core-i9-14900k",
                "sku": "NX-INTEL-14900K",
                "brand": "Intel",
                "description": "Frequências astronômicas de até 6.0 GHz direto da caixa. Arquitetura híbrida de performance para renderização 3D, compilação de código e multitasking sem gargalos.",
                "price": Decimal("4290.00"),
                "pix_price": Decimal("3646.50"),
                "stock": 8,
                "is_featured": False,
                "is_hot_deal": True,
                "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80",
                "specs": {
                    "Núcleos / Threads": "24 Cores (8P + 16E) / 32 Threads",
                    "Clock Turbo Max": "6.0 GHz",
                    "Intel Smart Cache": "36 MB L3",
                    "Socket": "LGA 1700",
                    "TDP": "125W Base / 253W Boost",
                }
            },
            {
                "category": cat_objs["placas-mae"],
                "name": "ASUS ROG Maximus Z790 Dark Hero Wi-Fi 7",
                "slug": "asus-rog-maximus-z790-dark-hero",
                "sku": "NX-MB-DARKHERO",
                "brand": "ASUS ROG",
                "description": "Placa-mãe topo de linha com 20+1 fases de VRM de 90A, 5 slots M.2 integrados (incluindo PCIe 5.0), conectividade Wi-Fi 7 e áudio ROG SupremeFX.",
                "price": Decimal("4890.00"),
                "pix_price": Decimal("4156.50"),
                "stock": 4,
                "is_featured": False,
                "is_hot_deal": False,
                "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=800&q=80",
                "specs": {
                    "Chipset": "Intel Z790",
                    "VRM": "20+1 Fases de Alimentação",
                    "Memória": "4x DDR5 até 8000+ MHz (OC)",
                    "Slots M.2": "5x M.2 NVMe (1x PCIe 5.0 x4)",
                    "Rede": "Wi-Fi 7 + Intel 2.5Gb Ethernet",
                }
            },
            {
                "category": cat_objs["memorias-armazenamento"],
                "name": "Corsair Dominator Titanium RGB 64GB (2x32GB) DDR5 6000MHz",
                "slug": "corsair-dominator-titanium-rgb-64gb-ddr5-6000mhz",
                "sku": "NX-RAM-DOMINATOR64",
                "brand": "Corsair",
                "description": "Design de alumínio forjado de precisão com módulos de topo intercambiáveis. Chips selecionados à mão e 11 LEDs RGB endereçáveis individualmente.",
                "price": Decimal("2190.00"),
                "pix_price": Decimal("1861.50"),
                "stock": 15,
                "is_featured": True,
                "is_hot_deal": False,
                "image_url": "https://images.unsplash.com/photo-1562976540-1502c2145186?auto=format&fit=crop&w=800&q=80",
                "specs": {
                    "Capacidade": "64GB (2x 32GB)",
                    "Frequência": "6.000 MT/s",
                    "Latência": "CL30 (30-36-36-76)",
                    "Tensão": "1.35V",
                    "Perfis": "Intel XMP 3.0 & AMD EXPO",
                }
            },
            {
                "category": cat_objs["memorias-armazenamento"],
                "name": "SSD Samsung 990 PRO 2TB NVMe M.2 PCIe 4.0",
                "slug": "ssd-samsung-990-pro-2tb-nvme-pcie-4",
                "sku": "NX-SSD-990PRO-2TB",
                "brand": "Samsung",
                "description": "Velocidades no limite da interface PCIe 4.0: 7.450 MB/s de leitura sequencial. Controle térmico inteligente para máxima consistência em transferências gigantes.",
                "price": Decimal("1590.00"),
                "pix_price": Decimal("1351.50"),
                "stock": 20,
                "is_featured": False,
                "is_hot_deal": True,
                "image_url": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?auto=format&fit=crop&w=800&q=80",
                "specs": {
                    "Capacidade": "2.000 GB (2TB)",
                    "Leitura Sequencial": "7.450 MB/s",
                    "Gravação Sequencial": "6.900 MB/s",
                    "DRAM Cache": "2GB LPDDR4",
                    "Durabilidade": "1200 TBW",
                }
            },
            {
                "category": cat_objs["setups-prontos"],
                "name": "Nexus Apex Titan V3 Custom Workstation",
                "slug": "nexus-apex-titan-v3-custom-workstation",
                "sku": "NX-BUILD-TITAN-V3",
                "brand": "Nexus Custom",
                "description": "Máquina montada e afinada à mão em nosso laboratório de precisão. RTX 4090, Ryzen 9 7950X3D, 64GB DDR5 e refrigeração customizada com fluido não-condutivo.",
                "price": Decimal("22990.00"),
                "pix_price": Decimal("18899.00"),
                "stock": 3,
                "is_featured": True,
                "is_hot_deal": True,
                "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=1000&q=80",
                "specs": {
                    "Placa de Vídeo": "GeForce RTX 4090 24GB Liquid",
                    "Processador": "AMD Ryzen 9 7950X3D (16C/32T)",
                    "Memória": "64GB DDR5 6000MHz Dominator Titanium",
                    "Armazenamento": "4TB NVMe Samsung 990 PRO",
                    "Fonte": "Corsair 1200W Platinum Modular",
                    "Gabinete": "Lian Li O11 Dynamic EVO Dark",
                }
            },
            {
                "category": cat_objs["perifericos-audio"],
                "name": "Teclado Mecânico Wooting 60HE+ Rapid Trigger",
                "slug": "teclado-mecanico-wooting-60he-plus",
                "sku": "NX-PERIF-WOOTING60",
                "brand": "Wooting",
                "description": "O padrão ouro em eSports competitivo. Switches magnéticos com efeito Hall e ponto de atuação milimétrico customizável de 0.1mm a 4.0mm.",
                "price": Decimal("1890.00"),
                "pix_price": Decimal("1606.50"),
                "stock": 7,
                "is_featured": False,
                "is_hot_deal": False,
                "image_url": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?auto=format&fit=crop&w=800&q=80",
                "specs": {
                    "Switches": "Lekker Hall Effect Magnéticos",
                    "Ponto de Atuação": "0.1mm a 4.0mm por tecla",
                    "Rapid Trigger": "Ativação e Reset Instantâneo",
                    "Polling Rate": "1000 Hz",
                    "Layout": "60% ANSI",
                }
            }
        ]

        for pdata in products_data:
            prod, created = Product.objects.get_or_create(
                slug=pdata["slug"],
                defaults={
                    "category": pdata["category"],
                    "name": pdata["name"],
                    "sku": pdata["sku"],
                    "brand": pdata["brand"],
                    "description": pdata["description"],
                    "price": pdata["price"],
                    "pix_price": pdata["pix_price"],
                    "stock": pdata["stock"],
                    "is_featured": pdata["is_featured"],
                    "is_hot_deal": pdata["is_hot_deal"],
                    "image_url": pdata["image_url"],
                    "technical_specs": pdata["specs"],
                }
            )

            # Cria imagens adicionais para a galeria
            if created:
                ProductImage.objects.create(
                    product=prod,
                    image_url=pdata["image_url"],
                    caption=f"{prod.name} - Vista Angular",
                    order=1
                )
                ProductImage.objects.create(
                    product=prod,
                    image_url="https://images.unsplash.com/photo-1591488320449-011701bb6704?auto=format&fit=crop&w=800&q=80",
                    caption=f"{prod.name} - Conexões e Detalhes",
                    order=2
                )

        self.stdout.write("10 Produtos cadastrados com especificações completas e galeria.")

        # 5. Criação de um Pedido de Demonstração para o Cliente
        sample_prod1 = Product.objects.get(slug="geforce-rtx-4080-super-asus-rog-strix-16gb")
        sample_prod2 = Product.objects.get(slug="ssd-samsung-990-pro-2tb-nvme-pcie-4")

        demo_order, order_created = Order.objects.get_or_create(
            order_number="NX-DEMO-2026",
            defaults={
                "user": customer_user,
                "full_name": "Carlos Eduardo Silva",
                "email": "cliente@nexushardware.com.br",
                "phone": "(11) 98888-7777",
                "cpf": "123.456.789-00",
                "cep": "01310-100",
                "address": "Avenida Paulista",
                "number": "1000",
                "complement": "Conjunto 42",
                "neighborhood": "Bela Vista",
                "city": "São Paulo",
                "state": "SP",
                "payment_method": "PIX",
                "status": "PAID",
                "subtotal": sample_prod1.pix_price + sample_prod2.pix_price,
                "shipping_fee": Decimal("24.90"),
                "discount_amount": Decimal("0.00"),
                "total_amount": sample_prod1.pix_price + sample_prod2.pix_price + Decimal("24.90"),
                "tracking_code": "NX-BR-99482710",
            }
        )
        if order_created:
            OrderItem.objects.create(
                order=demo_order,
                product=sample_prod1,
                price_at_purchase=sample_prod1.pix_price,
                quantity=1
            )
            OrderItem.objects.create(
                order=demo_order,
                product=sample_prod2,
                price_at_purchase=sample_prod2.pix_price,
                quantity=1
            )
            self.stdout.write("Pedido de demonstração criado com sucesso para o usuário cliente.")

        self.stdout.write(self.style.SUCCESS("[OK] Seed de dados concluido com 100% de sucesso!"))
