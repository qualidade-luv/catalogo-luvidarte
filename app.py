import streamlit as st
import pandas as pd
import numpy as np
import re
from PIL import Image
import requests
from io import BytesIO
import base64

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
# PALETA DE CORES
# ============================================
CORES = {
    "fundo_pagina": "#F7F7F7",        # Fundo cinza claro
    "fundo_card": "#FFFFFF",          # Fundo branco dos cards
    "preto": "#000000",               # Preto para títulos principais
    "cinza_texto": "#333333",         # Cinza escuro para textos
    "cinza_claro": "#666666",         # Cinza claro para textos secundários
    "destaque_preco": "#D35400",      # Laranja/terracota para preços
    "dourado": "#C9A03D",            # Dourado para detalhes
    "borda_card": "#E0E0E0",          # Borda suave para cards
    "fundo_banner": "#FFFFFF",        # Fundo branco para o banner
    "borda_banner": "#E0E0E0"         # Borda do banner
}

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
    /* Fundo principal */
    .stApp {{
        background-color: {CORES["fundo_pagina"]};
    }}
    
    /* Sidebar - mesma cor do fundo */
    .css-1d391kg, .css-12oz5g7, section[data-testid="stSidebar"] {{
        background-color: {CORES["fundo_pagina"]};
    }}
    
    /* Banner principal - fundo claro, letras pretas */
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
    
    /* Contato centralizado */
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
    
    /* Preço - cor de destaque */
    .price {{
        color: {CORES["destaque_preco"]};
        font-size: 26px;
        font-weight: bold;
        margin: 10px 0;
    }}
    
    /* Card do produto */
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
    
    /* Referência */
    .ref {{
        color: {CORES["cinza_claro"]};
        font-size: 11px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    /* Nome do produto */
    .product-name {{
        color: {CORES["preto"]};
        font-size: 17px;
        font-weight: 600;
        margin: 6px 0;
    }}
    
    /* Categoria/Grupo */
    .product-category {{
        color: {CORES["cinza_claro"]};
        font-size: 12px;
        font-weight: 400;
        margin-bottom: 10px;
    }}
    
    /* Botão de orçamento */
    .stButton > button {{
        background-color: {CORES["preto"]};
        color: white;
        border: none;
        border-radius: 30px;
        padding: 10px 16px;
        font-weight: 600;
        font-size: 14px;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s;
    }}
    
    .stButton > button:hover {{
        background-color: {CORES["dourado"]};
        color: {CORES["preto"]};
    }}
    
    /* Separador */
    hr {{
        border-color: #E8E8E8;
        margin: 25px 0;
    }}
    
    /* Títulos das seções */
    h1, h2, h3 {{
        color: {CORES["preto"]};
    }}
    
    /* Labels dos filtros */
    .stSelectbox label, .stSlider label, .stTextInput label {{
        color: {CORES["cinza_texto"]} !important;
        font-weight: 500 !important;
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
# EXIBIR PRODUTOS
# ============================================
st.markdown(f"## ✨ Produtos Encontrados: {len(dados_filtrados)}")

if dados_filtrados.empty:
    st.warning("😕 Nenhum produto encontrado.")
else:
    colunas = st.columns(3)
    
    for posicao, (indice, produto) in enumerate(dados_filtrados.iterrows()):
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
            
            if pd.notna(produto.get('ml')) and produto['ml'] > 0:
                st.markdown(f"📏 **{produto['ml']:.0f} ml**")
            
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
            
            if st.button("📞 Solicitar Orçamento", key=f"btn_{indice}"):
                st.success(f"✅ {produto['Descrição']} (Ref: {produto['Referência']})")
                st.info("📱 WhatsApp: (11) 4676-9000")
            
            st.markdown("---")

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
# WHATSAPP FLUTUANTE
# ============================================
st.markdown("""
<style>
.whatsapp-float {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #25D366;
    color: white;
    border-radius: 50px;
    padding: 12px 20px;
    text-align: center;
    font-size: 14px;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    z-index: 1000;
}
.whatsapp-float a {
    color: white;
    text-decoration: none;
}
</style>
<div class="whatsapp-float">
    <a href="https://wa.me/551146769000?text=Olá! Gostaria de informações sobre os produtos Luvidarte" target="_blank">
        💬 Fale conosco no WhatsApp
    </a>
</div>
""", unsafe_allow_html=True)
