import streamlit as st
import pandas as pd
import numpy as np
import re
from PIL import Image
import requests
from io import BytesIO
import base64
from datetime import datetime
import time

# ============================================
# CONFIGURAÇÃO DA PÁGINA (com favicon)
# ============================================
def carregar_logo_favicon():
    url_drive = "https://drive.google.com/uc?export=download&id=1wiwp3txOXGsEMRrUgzdLFlxQL2188uTw"
    try:
        response = requests.get(url_drive, timeout=10)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img = img.resize((32, 32))
            return img
    except:
        pass
    return None

favicon = carregar_logo_favicon()
if favicon:
    st.set_page_config(
        page_title="Luvidarte - Catálogo Virtual",
        page_icon=favicon,
        layout="wide"
    )
else:
    st.set_page_config(
        page_title="Luvidarte - Catálogo Virtual",
        page_icon="📦",
        layout="wide"
    )

# ============================================
# REMOVER BOTÃO "MANAGE APP" DO STREAMLIT - VERSÃO COMPLETA
# ============================================
st.markdown("""
<style>
/* Esconder o botão Manage app e todo o toolbar */
.stApp header div[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

/* Esconder o botão de menu (três pontinhos) */
button[aria-label="View app menu"] {
    display: none !important;
}

button[aria-label="Manage app"] {
    display: none !important;
}

/* Esconder o toolbar inteiro do header */
header[data-testid="stHeader"] {
    display: none !important;
}

/* Esconder elementos específicos do Streamlit Cloud */
.css-1kyxreq {
    display: none !important;
}

.stDecoration {
    display: none !important;
}

/* Esconder qualquer elemento que contenha "manage" */
button:has(span:contains("Manage")),
a:has(span:contains("Manage")) {
    display: none !important;
}

/* Esconder o footer do Streamlit */
footer {
    display: none !important;
}

/* Remover o espaço extra do header */
.main > div {
    padding-top: 0rem !important;
}

/* Remover qualquer overlay ou elemento extra */
#MainMenu {
    visibility: hidden;
    display: none;
}

/* Para versões mais recentes do Streamlit */
[data-testid="collapsedControl"] {
    display: none !important;
}

/* Remover borda superior quando deploy no cloud */
.stApp > header {
    display: none !important;
}

/* Esconder botão de deploy */
.stAppDeployButton {
    display: none !important;
}
</style>

<script>
// JavaScript para remover qualquer elemento que possa aparecer depois
(function() {
    function removeManageElements() {
        // Procurar e remover botões Manage por texto
        const allElements = document.querySelectorAll('button, a, div, span');
        allElements.forEach(el => {
            if (el.innerText && el.innerText.toLowerCase().includes('manage')) {
                el.style.display = 'none';
                if (el.parentNode) {
                    // Também tenta esconder o container pai
                    if (el.parentNode.style) {
                        el.parentNode.style.display = 'none';
                    }
                }
            }
        });
        
        // Remover toolbar
        const toolbars = document.querySelectorAll('[data-testid="stToolbar"]');
        toolbars.forEach(toolbar => {
            if (toolbar && toolbar.remove) {
                toolbar.remove();
            } else if (toolbar) {
                toolbar.style.display = 'none';
            }
        });
        
        // Remover header
        const headers = document.querySelectorAll('header');
        headers.forEach(header => {
            if (header.getAttribute('data-testid') === 'stHeader') {
                header.style.display = 'none';
            }
        });
        
        // Remover qualquer elemento com classe relacionada a manage
        const manageClasses = document.querySelectorAll('[class*="manage"], [class*="Manage"]');
        manageClasses.forEach(el => {
            el.style.display = 'none';
        });
    }
    
    // Executar imediatamente
    removeManageElements();
    
    // Executar novamente após um pequeno delay
    setTimeout(removeManageElements, 100);
    setTimeout(removeManageElements, 500);
    setTimeout(removeManageElements, 1000);
})();
</script>
""", unsafe_allow_html=True)

# ============================================
# FUNÇÃO PARA GERENCIAR COOKIES (VERSÃO CORRIGIDA COM MENSAGEM)
# ============================================
def init_cookie_consent():
    """Inicializa o sistema de consentimento de cookies"""
    if 'cookie_consent' not in st.session_state:
        st.session_state.cookie_consent = None
    if 'mensagem_visivel' not in st.session_state:
        st.session_state.mensagem_visivel = True

def set_cookie_consent(consent):
    """Define o consentimento de cookies"""
    st.session_state.cookie_consent = consent

def fechar_mensagem_informativa():
    """Fecha a mensagem informativa"""
    st.session_state.mensagem_visivel = False

def show_cookie_banner():
    """Exibe o banner de cookies com botões Streamlit"""
    # Garantir que a variável existe (segurança extra)
    if 'cookie_consent' not in st.session_state:
        st.session_state.cookie_consent = None
    
    if st.session_state.cookie_consent is None:
        # Verificar se veio alguma escolha via query params
        if 'cookie_choice' in st.query_params:
            choice = st.query_params['cookie_choice']
            if choice == 'accepted':
                set_cookie_consent(True)
                st.query_params.clear()
                st.rerun()
            elif choice == 'declined':
                set_cookie_consent(False)
                st.query_params.clear()
                st.rerun()
        
        # CSS para o banner
        st.markdown("""
        <style>
        .cookie-banner-simple {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            color: white;
            padding: 25px 30px;
            z-index: 9999;
            box-shadow: 0 -4px 20px rgba(0,0,0,0.3);
            border-top: 3px solid #C9A03D;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        .cookie-content-simple {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 30px;
            flex-wrap: wrap;
        }
        
        .cookie-text-simple {
            flex: 2;
            min-width: 250px;
        }
        
        .cookie-text-simple h3 {
            margin: 0 0 8px 0;
            font-size: 18px;
            color: #C9A03D;
        }
        
        .cookie-text-simple p {
            margin: 0;
            font-size: 13px;
            line-height: 1.5;
            color: #e0e0e0;
        }
        
        .cookie-buttons-simple {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }
        
        @media (max-width: 768px) {
            .cookie-content-simple {
                flex-direction: column;
                text-align: center;
            }
            
            .cookie-buttons-simple {
                justify-content: center;
            }
        }
        </style>
        
        <div class="cookie-banner-simple">
            <div class="cookie-content-simple">
                <div class="cookie-text-simple">
                    <h3>🍪 Nós usamos cookies</h3>
                    <p>Utilizamos cookies para melhorar sua experiência de navegação, 
                    analisar o tráfego do site e personalizar conteúdo.</p>
                </div>
                <div class="cookie-buttons-simple">
                    <!-- Botões serão renderizados abaixo -->
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Criar colunas para os botões
        col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
        
        with col2:
            if st.button("✅ Aceitar Cookies", key="accept_btn", use_container_width=True):
                # Salvar escolha e recarregar
                st.query_params["cookie_choice"] = "accepted"
                st.rerun()
        
        with col3:
            if st.button("❌ Recusar Cookies", key="decline_btn", use_container_width=True):
                # Salvar escolha e recarregar
                st.query_params["cookie_choice"] = "declined"
                st.rerun()
        
        # Parar execução até o usuário escolher
        st.stop()
    
    # Exibir mensagem informativa após aceitar os cookies
    elif st.session_state.cookie_consent == True and st.session_state.mensagem_visivel:
        # CSS para a mensagem profissional
        st.markdown("""
        <style>
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .info-message {
            background: linear-gradient(135deg, #FFF9E6 0%, #FFF4D6 100%);
            border-left: 4px solid #C9A03D;
            border-radius: 8px;
            padding: 16px 20px;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            animation: slideDown 0.5s ease-out;
        }
        
        .info-message-title {
            color: #C9A03D;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .info-message-text {
            color: #5a5a5a;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 12px;
        }
        
        .info-message-contact {
            background-color: #C9A03D20;
            border-radius: 6px;
            padding: 10px 15px;
            margin-top: 8px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .info-message-contact span {
            color: #C9A03D;
            font-weight: 500;
        }
        
        .info-message-contact a {
            color: #25D366;
            text-decoration: none;
            font-weight: bold;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }
        
        .info-message-contact a:hover {
            text-decoration: underline;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Usando o container do Streamlit para a mensagem com botão funcional
        with st.container():
            col_msg, col_btn = st.columns([20, 1])
            
            with col_msg:
                st.markdown("""
                <div class="info-message">
                    <div class="info-message-title">
                        <span>📋</span> Informação Importante
                    </div>
                    <div class="info-message-text">
                        <strong>Prezado(a) cliente,</strong><br>
                        Os valores, especificações técnicas, medidas e disponibilidade dos produtos apresentados neste catálogo 
                        estão sujeitos a alterações sem aviso prévio, conforme política comercial da Luvidarte. 
                        Recomendamos sempre confirmar as informações atualizadas diretamente com nossa equipe de vendas.
                    </div>
                    <div class="info-message-contact">
                        <span>📞 Para mais informações, entre em contato conosco:</span>
                        <div>
                            <a href="https://wa.me/551146769000?text=Olá! Gostaria de confirmar informações sobre os produtos do catálogo" target="_blank">
                                💬 WhatsApp (11) 4676-9000
                            </a>
                            <span style="margin: 0 8px">|</span>
                            <span>📧 sac@luvidarte.com.br</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_btn:
                # Botão "X" funcional usando Streamlit
                if st.button("✖️", key="close_info_message", help="Fechar mensagem"):
                    fechar_mensagem_informativa()
                    st.rerun()

# ============================================
# INICIALIZAR E MOSTRAR BANNER DE COOKIES
# ============================================
init_cookie_consent()
show_cookie_banner()

# ============================================
# PALETA DE CORES
# ============================================
CORES = {
    "fundo_pagina": "#F7F7F7",
    "fundo_card": "#FFFFFF",
    "preto": "#000000",
    "cinza_texto": "#333333",
    "cinza_claro": "#666666",
    "destaque_preco": "#D35400",
    "dourado": "#C9A03D",
    "borda_card": "#E0E0E0",
    "fundo_banner": "#FFFFFF",
    "borda_banner": "#E0E0E0"
}

# ============================================
# FUNÇÃO PARA FORMATAR ML
# ============================================
def formatar_ml(valor):
    """Formata valores de ml com separador de milhar e 3 casas decimais"""
    if pd.isna(valor) or valor == 0:
        return None
    
    # Formatar com separador de milhar e 3 casas decimais
    # Ex: 2625 -> 2.625
    # Ex: 750 -> 750,000
    valor_formatado = f"{valor:,.3f}"
    
    # Converter formato americano para brasileiro
    # Troca vírgula por ponto e ponto por vírgula
    partes = valor_formatado.split('.')
    if len(partes) > 1:
        # Separador de milhar: ponto
        inteiro = partes[0].replace(',', '.')
        # Casas decimais: vírgula
        decimal = partes[1]
        return f"{inteiro},{decimal}"
    else:
        return valor_formatado.replace(',', '.')

# ============================================
# FUNÇÃO PARA CARREGAR O LOGO
# ============================================
@st.cache_data(ttl=3600)
def carregar_logo():
    url_drive = "https://drive.google.com/uc?export=download&id=1wiwp3txOXGsEMRrUgzdLFlxQL2188uTw"
    
    try:
        response = requests.get(url_drive, timeout=15)
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'image' in content_type:
                img = Image.open(BytesIO(response.content))
                return img
    except Exception as e:
        pass
    return None

# ============================================
# FUNÇÃO PARA CONVERTER MOEDA BRASILEIRA
# ============================================
def converter_moeda_para_numero(valor):
    if pd.isna(valor) or valor == '' or valor is None:
        return np.nan
    
    valor_str = str(valor)
    valor_str = valor_str.replace('R$', '').replace(' ', '')
    valor_str = valor_str.replace('.', '')
    valor_str = valor_str.replace(',', '.')
    valor_str = re.sub(r'[^0-9.]', '', valor_str)
    
    try:
        return float(valor_str)
    except:
        return np.nan

# ============================================
# ESTILO PERSONALIZADO
# ============================================
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {CORES["fundo_pagina"]};
    }}
    
    .css-1d391kg, .css-12oz5g7, section[data-testid="stSidebar"] {{
        background-color: {CORES["fundo_pagina"]};
    }}
    
    .main-banner {{
        background-color: {CORES["fundo_banner"]};
        border-radius: 16px;
        padding: 20px 30px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
        min-height: 110px;
        border: 1px solid {CORES["borda_banner"]};
    }}
    
    .logo-container {{
        flex-shrink: 0;
        height: 100%;
        display: flex;
        align-items: center;
        padding: 5px;
    }}
    
    .logo-img {{
        max-height: 70px;
        width: auto;
        object-fit: contain;
    }}
    
    .banner-text {{
        flex-grow: 1;
        text-align: center;
    }}
    
    .banner-text h1 {{
        font-size: 38px;
        margin: 0;
        font-weight: bold;
        color: {CORES["preto"]};
    }}
    
    .banner-text p {{
        font-size: 15px;
        margin: 5px 0 0 0;
        color: {CORES["cinza_texto"]};
    }}
    
    .contato-central {{
        text-align: center;
        margin: 15px 0 25px 0;
        padding: 10px;
        font-size: 13px;
        color: {CORES["cinza_claro"]};
        background-color: {CORES["fundo_card"]};
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #E8E8E8;
    }}
    
    .price {{
        color: {CORES["destaque_preco"]};
        font-size: 26px;
        font-weight: bold;
        margin: 10px 0;
    }}
    
    .product-card {{
        background-color: {CORES["fundo_card"]};
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border: 1px solid {CORES["borda_card"]};
        transition: all 0.2s ease;
    }}
    
    .product-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-color: {CORES["dourado"]};
    }}
    
    .ref {{
        color: {CORES["cinza_claro"]};
        font-size: 11px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .product-name {{
        color: {CORES["preto"]};
        font-size: 17px;
        font-weight: 600;
        margin: 6px 0;
    }}
    
    .product-category {{
        color: {CORES["cinza_claro"]};
        font-size: 12px;
        font-weight: 400;
        margin-bottom: 10px;
    }}
    
    hr {{
        border-color: #E8E8E8;
        margin: 25px 0;
    }}
    
    h1, h2, h3 {{
        color: {CORES["preto"]};
    }}
    
    .stSelectbox label {{
        color: {CORES["cinza_texto"]} !important;
        font-weight: 500 !important;
    }}
    
    /* Estilizar o selectbox de página */
    .stSelectbox div[data-baseweb="select"] {{
        min-width: 120px;
    }}
    </style>
""", unsafe_allow_html=True)

# ============================================
# BANNER COM LOGO (fundo claro)
# ============================================

logo_img = carregar_logo()

if logo_img:
    buffered = BytesIO()
    logo_img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    st.markdown(f"""
    <div class='main-banner'>
        <div class='logo-container'>
            <img src='data:image/png;base64,{img_base64}' class='logo-img' style='max-height: 70px; width: auto;'>
        </div>
        <div class='banner-text'>
            <h1>Catálogo Virtual</h1>
            <p>Peças exclusivas em vidro e decoração</p>
        </div>
        <div style='width: 80px;'></div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class='main-banner'>
        <div class='banner-text' style='width: 100%;'>
            <h1>Catálogo Virtual</h1>
            <p>Peças exclusivas em vidro e decoração</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Texto de contato
st.markdown(f"""
<div class='contato-central'>
    📍 Rua Caetano Rubio, 213 - Ferraz de Vasconcelos - SP &nbsp;|&nbsp;
    📞 (11) 4676-9000 &nbsp;|&nbsp;
    ✉️ sac@luvidarte.com.br
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================
# CONFIGURAÇÕES DA PLANILHA
# ============================================
ID_PLANILHA = "1DCmwFzQvbQYDBsQft17VO9szjixgq1Bp09dYTfu142w"
NOME_ABA = "base"

# ============================================
# FUNÇÃO PARA CARREGAR A PLANILHA
# ============================================
@st.cache_data(ttl=600)
def carregar_planilha(id_planilha, nome_aba="base"):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{id_planilha}/gviz/tq?tqx=out:csv&sheet={nome_aba}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        
        if 'Preço Bruto' in df.columns:
            df['Preço'] = df['Preço Bruto'].apply(converter_moeda_para_numero)
            precos_validos = df['Preço'].dropna()
            if len(precos_validos) > 0:
                st.sidebar.success(f"✅ {len(precos_validos)} produtos com preço")
        
        df['GRUPO'] = df['GRUPO'].fillna('Outros')
        df['FAMILIA'] = df['FAMILIA'].fillna('Outros')
        df['Descrição'] = df['Descrição'].fillna('Produto sem descrição')
        df['Referência'] = df['Referência'].fillna('').astype(str)
        
        if 'ml' in df.columns:
            df['ml'] = pd.to_numeric(df['ml'], errors='coerce')
        
        return df
        
    except Exception as erro:
        st.error(f"❌ Erro ao carregar a planilha: {erro}")
        return pd.DataFrame()

# ============================================
# CARREGAR DADOS
# ============================================
with st.spinner("🔄 Carregando catálogo..."):
    dados = carregar_planilha(ID_PLANILHA, NOME_ABA)

if dados.empty:
    st.stop()

# ============================================
# FILTROS
# ============================================
st.sidebar.header("🔍 Filtrar Produtos")
st.sidebar.markdown(f"📊 **Total: {len(dados)} produtos**")

familias = ["Todas"] + sorted(dados['FAMILIA'].unique())
familia_escolhida = st.sidebar.selectbox("📌 Família", familias)

if familia_escolhida != "Todas":
    grupos_disponiveis = dados[dados['FAMILIA'] == familia_escolhida]['GRUPO'].unique()
else:
    grupos_disponiveis = dados['GRUPO'].unique()

grupos = ["Todos"] + sorted(grupos_disponiveis)
grupo_escolhido = st.sidebar.selectbox("📦 Grupo", grupos)

precos_validos = dados['Preço'].dropna()
if len(precos_validos) > 0:
    preco_min = float(precos_validos.min())
    preco_max = float(precos_validos.max())
    faixa_preco = st.sidebar.slider(
        "💰 Faixa de Preço (R$)",
        min_value=preco_min,
        max_value=preco_max,
        value=(preco_min, preco_max),
        step=10.0
    )
else:
    faixa_preco = (0, 1000)

st.sidebar.markdown("---")
busca_referencia = st.sidebar.text_input("🔎 Buscar por Referência", placeholder="Ex: 10, 40, 60...")

if st.sidebar.button("🔄 Limpar Filtros"):
    st.cache_data.clear()
    # Resetar página quando limpar filtros
    st.session_state.pagina_atual = 1
    st.rerun()

# ============================================
# APLICAR FILTROS
# ============================================
dados_filtrados = dados.copy()

if familia_escolhida != "Todas":
    dados_filtrados = dados_filtrados[dados_filtrados['FAMILIA'] == familia_escolhida]

if grupo_escolhido != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados['GRUPO'] == grupo_escolhido]

if len(precos_validos) > 0:
    dados_filtrados = dados_filtrados[
        (dados_filtrados['Preço'].isna()) |  
        ((dados_filtrados['Preço'] >= faixa_preco[0]) & 
         (dados_filtrados['Preço'] <= faixa_preco[1]))
    ]

if busca_referencia:
    dados_filtrados = dados_filtrados[
        dados_filtrados['Referência'].str.contains(busca_referencia, case=False, na=False)
    ]

# ============================================
# PAGINAÇÃO CENTRAL - 9 ITENS POR PÁGINA
# ============================================
ITENS_POR_PAGINA = 9
total_encontrados = len(dados_filtrados)
total_paginas = max(1, (total_encontrados + ITENS_POR_PAGINA - 1) // ITENS_POR_PAGINA)

# Inicializar página atual
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = 1

# Resetar página quando filtros mudarem
if 'ultimos_filtros' not in st.session_state:
    st.session_state.ultimos_filtros = (familia_escolhida, grupo_escolhido, faixa_preco, busca_referencia)
else:
    filtros_atual = (familia_escolhida, grupo_escolhido, faixa_preco, busca_referencia)
    if filtros_atual != st.session_state.ultimos_filtros:
        st.session_state.pagina_atual = 1
        st.session_state.ultimos_filtros = filtros_atual

# Garantir que a página atual está dentro dos limites
if st.session_state.pagina_atual > total_paginas:
    st.session_state.pagina_atual = total_paginas
if st.session_state.pagina_atual < 1:
    st.session_state.pagina_atual = 1

# Calcular índices da página atual
indice_inicio = (st.session_state.pagina_atual - 1) * ITENS_POR_PAGINA
indice_fim = min(indice_inicio + ITENS_POR_PAGINA, total_encontrados)

# Fatiar os dados para a página atual
dados_pagina = dados_filtrados.iloc[indice_inicio:indice_fim]

# ============================================
# EXIBIR PRODUTOS
# ============================================
st.markdown(f"## ✨ Produtos Encontrados: {total_encontrados}")

if dados_filtrados.empty:
    st.warning("😕 Nenhum produto encontrado.")
else:
    # Exibir produtos em 3 colunas (3x3 = 9 itens)
    colunas = st.columns(3)
    
    for posicao, (indice, produto) in enumerate(dados_pagina.iterrows()):
        with colunas[posicao % 3]:
            st.markdown(f"""
            <div class='product-card'>
                <span class='ref'>🔖 REF: {produto['Referência']}</span>
                <p class='product-name'>{produto['Descrição']}</p>
                <p class='product-category'>{produto['GRUPO']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if pd.notna(produto.get('imagem_url')) and produto.get('imagem_url'):
                try:
                    st.image(produto['imagem_url'], use_container_width=True)
                except:
                    st.image("https://via.placeholder.com/300x200?text=Sem+Imagem", use_container_width=True)
            else:
                st.image("https://via.placeholder.com/300x200?text=Sem+Imagem", use_container_width=True)
            
            # ============================================
            # EXIBIR ML COM FORMATAÇÃO DE MILHAR E 3 CASAS DECIMAIS
            # ============================================
            if pd.notna(produto.get('ml')) and produto['ml'] > 0:
                ml_formatado = formatar_ml(produto['ml'])
                if ml_formatado:
                    st.markdown(f"📏 **{ml_formatado} ml**")
            
            if pd.notna(produto.get('Medidas')):
                st.markdown(f"📐 {produto['Medidas']}")
            
            preco = produto['Preço']
            if pd.notna(preco) and preco > 0:
                st.markdown(f"<p class='price'>R$ {preco:.2f}</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p class='price'>💰 Sob consulta</p>", unsafe_allow_html=True)
            
            if pd.notna(produto.get('Peso Liq S/Cx')):
                try:
                    peso = float(produto['Peso Liq S/Cx'])
                    st.caption(f"⚖️ Peso: {peso:.3f} kg")
                except:
                    st.caption(f"⚖️ Peso: {produto['Peso Liq S/Cx']}")
            
            st.markdown("---")
    
    # ============================================
    # CONTROLE DE PAGINAÇÃO - APARECE APENAS QUANDO NECESSÁRIO
    # ============================================
    if total_paginas > 1:
        st.markdown("---")
        
        # Container centralizado para o combobox
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #FFFFFF 0%, #fafafa 100%); border-radius: 12px; border: 1px solid #E0E0E0;">', unsafe_allow_html=True)
            
            # Selectbox para navegação de páginas
            pagina_selecionada = st.selectbox(
                "📄 Navegar para página",
                options=list(range(1, total_paginas + 1)),
                index=st.session_state.pagina_atual - 1,
                key="page_select_central"
            )
            
            if pagina_selecionada != st.session_state.pagina_atual:
                st.session_state.pagina_atual = pagina_selecionada
                st.rerun()
            
            # Informações resumidas
            st.markdown(f"""
            <div style='text-align: center; margin-top: 8px; font-size: 12px; color: #666;'>
                Mostrando {indice_inicio + 1} - {min(indice_fim, total_encontrados)} de {total_encontrados} produtos
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Barra de progresso
        progresso = st.session_state.pagina_atual / total_paginas
        st.progress(progresso, text=f"📄 Página {st.session_state.pagina_atual} de {total_paginas}")

# ============================================
# RODAPÉ
# ============================================
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("**📍 Onde Estamos**  \nRua Caetano Rubio, 213  \nFerraz de Vasconcelos - SP")

with col2:
    st.markdown("**📞 Contato**  \n(11) 4676-9000  \nsac@luvidarte.com.br")

with col3:
    st.markdown("**🕒 Horário**  \nSegunda a Sexta: 8h às 18h  \nSábado: 8h às 12h")

with col4:
    st.markdown("**🔗 Links**  \n[Catálogos](#)  \n[Fale Conosco](#)")

st.markdown("---")
st.markdown(f"<p style='text-align: center; font-size: 12px; color:{CORES['cinza_claro']}'>© 2024 Luvidarte - Canal exclusivo para empresas</p>", unsafe_allow_html=True)

# ============================================
# WHATSAPP FLUTUANTE - POSICIONADO NO CANTO SUPERIOR DIREITO
# ============================================
st.markdown("""
<style>
.whatsapp-float {
    position: fixed;
    top: 80px;
    right: 20px;
    background-color: #25D366;
    color: white;
    border-radius: 50px;
    padding: 10px 18px;
    text-align: center;
    font-size: 13px;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    z-index: 999999 !important;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
}
.whatsapp-float:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    background-color: #075E54;
}
.whatsapp-float a {
    color: white;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 8px;
}
.whatsapp-icon {
    font-size: 18px;
    font-weight: normal;
}
</style>
<div class="whatsapp-float">
    <a href="https://wa.me/551146769000?text=Olá! Gostaria de informações sobre os produtos Luvidarte" target="_blank">
        <span class="whatsapp-icon">💬</span>
        <span>WhatsApp</span>
    </a>
</div>
""", unsafe_allow_html=True)
