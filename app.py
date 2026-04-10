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
# ESTILO PERSONALIZADO - TOTALMENTE RESPONSIVO
# ============================================
st.markdown("""
<style>
/* Reset e configurações base responsivas */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Remover elementos não obrigatórios */
.stDecoration { display: none; }
.stAppDeployButton { display: none !important; }

/* Configuração principal responsiva */
.main > div {
    padding-top: 0.5rem;
}

.stApp {
    background-color: #F7F7F7;
}

/* ========== BANNER RESPONSIVO ========== */
.main-banner {
    background-color: #FFFFFF;
    border-radius: 16px;
    padding: 15px 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    min-height: 90px;
    border: 1px solid #E0E0E0;
    flex-wrap: wrap;
}

.logo-container {
    flex-shrink: 0;
}

.logo-img {
    max-height: 60px;
    width: auto;
    object-fit: contain;
}

.banner-text {
    flex-grow: 1;
    text-align: center;
}

.banner-text h1 {
    font-size: clamp(20px, 5vw, 38px);
    margin: 0;
    font-weight: bold;
    color: #000000;
}

.banner-text p {
    font-size: clamp(11px, 3vw, 15px);
    margin: 5px 0 0 0;
    color: #333333;
}

/* ========== CONTATO CENTRAL RESPONSIVO ========== */
.contato-central {
    text-align: center;
    margin: 10px 0 20px 0;
    padding: 10px;
    font-size: clamp(11px, 3vw, 13px);
    color: #666666;
    background-color: #FFFFFF;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    border: 1px solid #E8E8E8;
    word-wrap: break-word;
}

/* ========== CARDS DE PRODUTO RESPONSIVOS ========== */
.product-card {
    background-color: #FFFFFF;
    border-radius: 12px;
    padding: clamp(12px, 3vw, 16px);
    margin: 10px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    transition: all 0.2s ease;
    height: 100%;
    position: relative;
}

.product-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* Estilo para card de promoção */
.product-card.promo-card {
    border: 1.5px solid #D32F2F;
    box-shadow: 0 2px 8px rgba(211, 47, 47, 0.15);
}

.product-card.promo-card:hover {
    border-color: #B71C1C;
    box-shadow: 0 4px 12px rgba(211, 47, 47, 0.25);
}

/* Badge de PROMOÇÃO */
.promo-badge {
    position: absolute;
    top: -8px;
    right: -8px;
    background: linear-gradient(135deg, #D32F2F 0%, #B71C1C 100%);
    color: white;
    font-size: 10px;
    font-weight: bold;
    padding: 4px 10px;
    border-radius: 20px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    z-index: 10;
    letter-spacing: 0.5px;
}

/* Badge de TABELA */
.tabela-badge {
    position: absolute;
    top: -8px;
    right: -8px;
    background: linear-gradient(135deg, #666666 0%, #444444 100%);
    color: white;
    font-size: 10px;
    font-weight: bold;
    padding: 4px 10px;
    border-radius: 20px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    z-index: 10;
    letter-spacing: 0.5px;
}

/* Estilo para card normal */
.product-card.normal-card {
    border: 1px solid #E0E0E0;
}

.ref {
    color: #666666;
    font-size: clamp(10px, 2.5vw, 11px);
    font-weight: 500;
    text-transform: uppercase;
    display: block;
    word-break: break-word;
}

.product-name {
    color: #000000;
    font-size: clamp(14px, 4vw, 17px);
    font-weight: 600;
    margin: 8px 0;
    word-break: break-word;
    line-height: 1.3;
}

.product-category {
    color: #666666;
    font-size: clamp(11px, 2.8vw, 12px);
    margin-bottom: 10px;
    word-break: break-word;
}

/* ========== REDES SOCIAIS RESPONSIVAS ========== */
.social-links-container {
    text-align: center;
    margin: 15px 0;
}

.social-title {
    color: #C9A03D;
    font-weight: bold;
    font-size: clamp(12px, 3.5vw, 14px);
    display: inline-block;
    margin-bottom: 10px;
}

.social-links {
    display: flex;
    justify-content: center;
    gap: clamp(12px, 4vw, 25px);
    margin: 10px 0 15px 0;
    flex-wrap: wrap;
}

.social-link {
    text-decoration: none;
    font-size: clamp(12px, 3.5vw, 14px);
    font-weight: 500;
    transition: all 0.3s ease;
    padding: 5px 0;
    white-space: nowrap;
}

@media (max-width: 480px) {
    .social-links {
        gap: 15px;
    }
    .social-link {
        font-size: 12px;
        white-space: normal;
    }
}

/* ========== CONTATO RODAPÉ RESPONSIVO ========== */
.contact-footer {
    text-align: center;
    font-size: clamp(11px, 3vw, 13px);
    color: #555555;
    margin: 10px 0;
    word-break: break-word;
    line-height: 1.5;
}

.footer-bottom {
    text-align: center;
    font-size: clamp(10px, 2.8vw, 12px);
    color: #666666;
    padding: 15px 0 10px 0;
    border-top: 1px solid #E0E0E0;
    margin-top: 20px;
}

.horario-atendimento {
    text-align: center;
    margin: 10px 0;
    font-size: clamp(11px, 3vw, 13px);
}

.horario-label {
    color: #C9A03D;
    font-weight: bold;
}

.horario-text {
    color: #555555;
}

/* ========== BOTÃO WHATSAPP RESPONSIVO ========== */
.whatsapp-float {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #25D366;
    color: white;
    border-radius: 50px;
    padding: 10px 18px;
    text-align: center;
    font-size: clamp(11px, 3vw, 13px);
    font-weight: bold;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    z-index: 999999 !important;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
}

.whatsapp-float:hover {
    transform: scale(1.05);
    background-color: #075E54;
}

.whatsapp-float a {
    color: white;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 8px;
}

@media (max-width: 480px) {
    .whatsapp-float {
        bottom: 15px;
        right: 15px;
        padding: 8px 14px;
    }
    .whatsapp-float span:last-child {
        display: none;
    }
    .whatsapp-float span:first-child {
        font-size: 20px;
    }
}

/* ========== GRID DE PRODUTOS RESPONSIVA ========== */
@media (max-width: 768px) {
    .stColumn {
        padding: 0 5px !important;
    }
}

/* ========== TABELAS E TEXTOS RESPONSIVOS ========== */
.stMarkdown, .stInfo, .stSuccess, .stWarning {
    word-break: break-word;
}

hr {
    margin: 20px 0;
    border-color: #E8E8E8;
}

/* Ajustes para selectbox e inputs em mobile */
@media (max-width: 768px) {
    .stSelectbox div[data-baseweb="select"] {
        font-size: 14px;
    }
    .stButton button {
        width: 100%;
        padding: 8px 12px;
        font-size: 14px;
    }
    .stSlider {
        margin-top: 20px;
    }
}

/* Sidebar responsiva */
@media (max-width: 768px) {
    section[data-testid="stSidebar"] {
        width: 280px !important;
    }
}

/* Ajuste para imagens de produto */
.stImage img {
    width: 100%;
    height: auto;
    object-fit: cover;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNÇÃO PARA CONVERTER MOEDA
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
# FUNÇÃO PARA CONVERTER PERCENTUAL
# ============================================
def converter_percentual_para_numero(valor):
    if pd.isna(valor) or valor == '' or valor is None:
        return 0.0
    valor_str = str(valor).strip()
    valor_str = valor_str.replace('%', '')
    valor_str = valor_str.replace(',', '.')
    try:
        percentual = float(valor_str)
        if percentual > 1 and percentual <= 100:
            percentual = percentual / 100
        return percentual
    except:
        return 0.0

# ============================================
# FUNÇÃO PARA FORMATAR ML CORRETAMENTE
# ============================================
def formatar_ml(valor):
    """Formata ML para mostrar 300 ml ou 1.300 L corretamente"""
    if pd.isna(valor) or valor == 0 or valor is None:
        return None
    
    try:
        ml_valor = float(valor)
        
        # Se for maior ou igual a 1000, converter para litros
        if ml_valor >= 1000:
            litros = ml_valor / 1000
            # Formatar com ponto como separador decimal
            return f"{litros:.3f}".replace(',', '.') + " L"
        else:
            # Para valores menores que 1000, mostrar em ml sem decimais desnecessários
            # Se for inteiro, mostra sem decimais
            if ml_valor == int(ml_valor):
                return f"{int(ml_valor)} ml"
            else:
                # Remove zeros desnecessários no final
                return f"{ml_valor:.3f}".rstrip('0').rstrip('.') + " ml"
    except:
        return None

# ============================================
# FUNÇÃO PARA CARREGAR A PLANILHA PRINCIPAL
# ============================================
@st.cache_data(ttl=600)
def carregar_planilha(id_planilha, nome_aba="base"):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{id_planilha}/gviz/tq?tqx=out:csv&sheet={nome_aba}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        
        # Renomear coluna "Codigo SISTEMA" para "Promo" se existir
        if 'Codigo SISTEMA' in df.columns:
            df = df.rename(columns={'Codigo SISTEMA': 'Promo'})
        
        if 'Preço Bruto' in df.columns:
            df['Preço'] = df['Preço Bruto'].apply(converter_moeda_para_numero)
        
        df['GRUPO'] = df['GRUPO'].fillna('Outros')
        df['Descrição'] = df['Descrição'].fillna('Produto sem descrição')
        df['Referência'] = df['Referência'].fillna('').astype(str)
        
        # Garantir que a coluna Promo existe
        if 'Promo' not in df.columns:
            df['Promo'] = ''
        
        if 'ml' in df.columns:
            df['ml'] = pd.to_numeric(df['ml'], errors='coerce')
        
        return df
        
    except Exception as erro:
        st.error(f"❌ Erro ao carregar a planilha: {erro}")
        return pd.DataFrame()

# ============================================
# FUNÇÃO PARA CARREGAR A PLANILHA DE PROMOÇÕES
# ============================================
@st.cache_data(ttl=600)
def carregar_planilha_promo(id_planilha, nome_aba="PROMO"):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{id_planilha}/gviz/tq?tqx=out:csv&sheet={nome_aba}"
        df_promo = pd.read_csv(url)
        df_promo.columns = df_promo.columns.str.strip()
        return df_promo
    except Exception as erro:
        st.warning(f"⚠️ Planilha PROMO não encontrada. As promoções não serão aplicadas.")
        return pd.DataFrame()

# ============================================
# FUNÇÃO PARA CARREGAR A PLANILHA BASE_ST
# ============================================
@st.cache_data(ttl=600)
def carregar_base_st(id_planilha_st, nome_aba_st="BASE_ST"):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{id_planilha_st}/gviz/tq?tqx=out:csv&sheet={nome_aba_st}"
        df_st = pd.read_csv(url)
        df_st.columns = df_st.columns.str.strip()
        return df_st
    except Exception as erro:
        st.warning(f"⚠️ Planilha de ST não encontrada.")
        return pd.DataFrame()

# ============================================
# FUNÇÃO PARA CARREGAR A PLANILHA DE DESCONTOS (NORMAL)
# ============================================
@st.cache_data(ttl=600)
def carregar_descontos_normal(id_planilha, nome_aba="NORMAL"):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{id_planilha}/gviz/tq?tqx=out:csv&sheet={nome_aba}"
        df_normal = pd.read_csv(url)
        df_normal.columns = df_normal.columns.str.strip()
        return df_normal
    except Exception as erro:
        st.warning(f"⚠️ Planilha NORMAL não encontrada.")
        return pd.DataFrame()

# ============================================
# FUNÇÃO PARA CARREGAR A PLANILHA DE DESCONTOS (ISENTO)
# ============================================
@st.cache_data(ttl=600)
def carregar_descontos_isento(id_planilha, nome_aba="ISENTO"):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{id_planilha}/gviz/tq?tqx=out:csv&sheet={nome_aba}"
        df_isento = pd.read_csv(url)
        df_isento.columns = df_isento.columns.str.strip()
        return df_isento
    except Exception as erro:
        st.warning(f"⚠️ Planilha ISENTO não encontrada.")
        return pd.DataFrame()

# ============================================
# FUNÇÃO PARA BUSCAR PREÇO NA PLANILHA PROMO
# ============================================
def buscar_preco_promo(referencia: str, uf: str, df_promo: pd.DataFrame) -> float:
    """
    Busca o preço promocional na planilha PROMO
    Referência na coluna A (primeira coluna)
    UF no cabeçalho das colunas (18%, 12%, 7% etc.)
    Mapeia a UF para a coluna de ICMS correspondente
    """
    if df_promo.empty or not referencia:
        return None
    
    # Limpar referência para busca (remover espaços extras)
    ref_limpa = str(referencia).strip()
    
    # A primeira coluna é a referência
    coluna_ref = df_promo.columns[0]
    
    # Filtrar linha da referência (busca exata)
    df_promo[coluna_ref] = df_promo[coluna_ref].astype(str).str.strip()
    linha_produto = df_promo[df_promo[coluna_ref] == ref_limpa]
    
    if linha_produto.empty:
        # Tentar busca parcial se não encontrar exata
        linha_produto = df_promo[df_promo[coluna_ref].str.contains(ref_limpa, case=False, na=False)]
        if linha_produto.empty:
            return None
    
    # Mapear UF para a coluna de ICMS correspondente
    uf_upper = uf.upper()
    
    if uf_upper == "SP":
        coluna_icms = "18%"
    elif uf_upper in ["MG", "RS", "SE", "PR", "RJ", "SC"]:
        coluna_icms = "12%"
    else:
        coluna_icms = "7%"
    
    # Encontrar a coluna no DataFrame que corresponde ao percentual
    coluna_preco = None
    for col in df_promo.columns:
        col_str = str(col).strip()
        if col_str == coluna_icms:
            coluna_preco = col
            break
    
    if coluna_preco is None:
        return None
    
    # Obter o valor do preço
    valor = linha_produto.iloc[0][coluna_preco]
    
    if pd.isna(valor):
        return None
    
    # Converter formato brasileiro (vírgula como decimal) para float
    if isinstance(valor, str):
        valor = valor.strip().replace('.', '').replace(',', '.')
        try:
            valor = float(valor)
        except:
            return None
    
    return float(valor) if not pd.isna(valor) else None

# ============================================
# FUNÇÃO PARA BUSCAR IPI NA BASE_ST
# ============================================
def buscar_ipi(ncm: str, df_st: pd.DataFrame) -> float:
    if df_st.empty or not ncm:
        return 0.0
    
    ncm_limpo = str(ncm).replace(".", "").strip()
    df_st['NCM_LIMPO'] = df_st.iloc[:, 1].astype(str).str.replace(".", "").str.strip()
    
    linha_ncm = df_st[df_st['NCM_LIMPO'] == ncm_limpo]
    if linha_ncm.empty:
        return 0.0
    
    valor_ipi = linha_ncm.iloc[0, 0]
    
    if pd.isna(valor_ipi):
        return 0.0
    
    if isinstance(valor_ipi, str):
        valor_ipi = valor_ipi.replace("%", "").replace(",", ".").strip()
    
    try:
        ipi = float(valor_ipi)
        if ipi > 1 and ipi <= 100:
            ipi = ipi / 100
        return ipi
    except:
        return 0.0

# ============================================
# FUNÇÃO PARA BUSCAR ALÍQUOTA ST
# ============================================
def buscar_aliquota_st(ncm: str, uf: str, df_st: pd.DataFrame) -> float:
    if df_st.empty or not ncm or not uf:
        return 0.0
    
    ncm_limpo = str(ncm).replace(".", "").strip()
    df_st['NCM_LIMPO'] = df_st.iloc[:, 1].astype(str).str.replace(".", "").str.strip()
    
    linha_ncm = df_st[df_st['NCM_LIMPO'] == ncm_limpo]
    if linha_ncm.empty:
        return 0.0
    
    colunas_uf = {col.strip().upper(): col for col in df_st.columns[2:]}
    if uf.upper() not in colunas_uf:
        return 0.0
    
    nome_coluna = colunas_uf[uf.upper()]
    valor = linha_ncm.iloc[0][nome_coluna]
    
    if pd.isna(valor):
        return 0.0
    
    if isinstance(valor, str):
        valor = valor.replace("%", "").replace(",", ".").strip()
    
    try:
        aliquota = float(valor)
        if aliquota > 1 and aliquota <= 100:
            aliquota = aliquota / 100
        return aliquota
    except:
        return 0.0

# ============================================
# FUNÇÃO PARA DETERMINAR ICMS BASEADO NA UF
# ============================================
def determinar_icms_por_uf(uf: str) -> float:
    uf_upper = uf.upper()
    
    if uf_upper == "SP":
        return 18.0
    elif uf_upper in ["MG", "RS", "SE", "PR", "RJ", "SC"]:
        return 12.0
    else:
        return 7.0

# ============================================
# FUNÇÃO PARA BUSCAR DESCONTO
# ============================================
def buscar_desconto(icms: float, forma_pagamento: str, df_desconto: pd.DataFrame) -> float:
    if df_desconto.empty:
        return 0.0
    
    if forma_pagamento == "PREÇO BASE":
        return 0.0
    
    df_temp = df_desconto.copy()
    
    df_temp['ICMS_LIMPO'] = df_temp['ICMS'].astype(str).str.replace('%', '').str.replace(',', '.').str.strip()
    df_temp['ICMS_LIMPO'] = pd.to_numeric(df_temp['ICMS_LIMPO'], errors='coerce')
    
    icms_percent = float(icms)
    df_temp['FORMA_LIMPO'] = df_temp['FORMA'].apply(lambda x: str(x).strip() if pd.notna(x) else "")
    
    if forma_pagamento == "VISTA":
        forma_para_buscar = ""
    else:
        try:
            forma_numero = float(forma_pagamento)
            forma_para_buscar = f"{forma_numero:.1f}"
        except:
            forma_para_buscar = forma_pagamento
    
    df_filtrado = df_temp[
        (df_temp['ICMS_LIMPO'] == icms_percent) & 
        (df_temp['FORMA_LIMPO'] == forma_para_buscar)
    ]
    
    if df_filtrado.empty and forma_pagamento != "VISTA":
        try:
            forma_numero = float(forma_pagamento)
            forma_int = str(int(forma_numero))
            df_filtrado = df_temp[
                (df_temp['ICMS_LIMPO'] == icms_percent) & 
                (df_temp['FORMA_LIMPO'] == forma_int)
            ]
        except:
            pass
    
    if not df_filtrado.empty:
        valor_desconto = df_filtrado.iloc[0]['DESCONTO']
        desconto = converter_percentual_para_numero(valor_desconto)
        return desconto
    
    return 0.0

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
    except:
        pass
    return None

# ============================================
# FUNÇÃO PARA GERENCIAR COOKIES
# ============================================
def init_cookie_consent():
    if 'cookie_consent' not in st.session_state:
        st.session_state.cookie_consent = None
    if 'mensagem_visivel' not in st.session_state:
        st.session_state.mensagem_visivel = True

def set_cookie_consent(consent):
    st.session_state.cookie_consent = consent

def fechar_mensagem_informativa():
    st.session_state.mensagem_visivel = False

def show_cookie_banner():
    if 'cookie_consent' not in st.session_state:
        st.session_state.cookie_consent = None
    
    if st.session_state.cookie_consent is None:
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
        
        st.markdown("""
        <style>
        .cookie-banner-simple {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            color: white;
            padding: 20px 25px;
            z-index: 9999;
            box-shadow: 0 -4px 20px rgba(0,0,0,0.3);
            border-top: 3px solid #C9A03D;
        }
        .cookie-content-simple {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
            flex-wrap: wrap;
        }
        .cookie-text-simple {
            flex: 2;
            min-width: 200px;
        }
        .cookie-text-simple h3 {
            margin: 0 0 5px 0;
            font-size: 16px;
            color: #C9A03D;
        }
        .cookie-text-simple p {
            margin: 0;
            font-size: 12px;
            line-height: 1.4;
            color: #e0e0e0;
        }
        @media (max-width: 768px) {
            .cookie-banner-simple { padding: 15px; }
            .cookie-text-simple h3 { font-size: 14px; }
            .cookie-text-simple p { font-size: 11px; }
        }
        </style>
        <div class="cookie-banner-simple">
            <div class="cookie-content-simple">
                <div class="cookie-text-simple">
                    <h3>🍪 Nós usamos cookies</h3>
                    <p>Utilizamos cookies para melhorar sua experiência de navegação.</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
        with col2:
            if st.button("✅ Aceitar Cookies", key="accept_btn", use_container_width=True):
                st.query_params["cookie_choice"] = "accepted"
                st.rerun()
        with col3:
            if st.button("❌ Recusar Cookies", key="decline_btn", use_container_width=True):
                st.query_params["cookie_choice"] = "declined"
                st.rerun()
        st.stop()
    
    elif st.session_state.cookie_consent == True and st.session_state.mensagem_visivel:
        st.markdown("""
        <style>
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
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
        }
        @media (max-width: 768px) {
            .info-message { padding: 12px 15px; }
            .info-message-title { font-size: 14px; }
            .info-message-text { font-size: 12px; }
            .info-message-contact { flex-direction: column; text-align: center; }
        }
        </style>
        """, unsafe_allow_html=True)
        
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
                            <a href="https://wa.me/5511930119335?text=Olá! Gostaria de informações sobre os produtos Luvidarte" target="_blank">
                                💬 WhatsApp (11) 93011-9335
                            </a>
                            <span style="margin: 0 8px">|</span>
                            <span>📞 Fixo (11) 4676-9000</span>
                            <span style="margin: 0 8px">|</span>
                            <span>📧 sac@luvidarte.com.br</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                if st.button("✖️", key="close_info_message", help="Fechar mensagem"):
                    fechar_mensagem_informativa()
                    st.rerun()

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
    "borda_promo": "#D32F2F",
    "fundo_banner": "#FFFFFF",
    "borda_banner": "#E0E0E0"
}

# ============================================
# LISTA DE UFs DO BRASIL
# ============================================
UFS_BRASIL = ["SP", "MG", "RS", "SE", "PR", "RJ", "SC", "MT", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MS", "PA", "PB", "PE", "PI", "RN", "RO", "RR", "TO"]

# ============================================
# INICIALIZAR E MOSTRAR BANNER DE COOKIES
# ============================================
init_cookie_consent()
show_cookie_banner()

# ============================================
# BANNER COM LOGO
# ============================================
logo_img = carregar_logo()
if logo_img:
    buffered = BytesIO()
    logo_img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    st.markdown(f"""
    <div class='main-banner'>
        <div class='logo-container'>
            <img src='data:image/png;base64,{img_base64}' class='logo-img'>
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

st.markdown(f"""
<div class='contato-central'>
    📍 Rua Caetano Rubio, 213 - Ferraz de Vasconcelos - SP &nbsp;|&nbsp;
    📞 (11) 4676-9000 &nbsp;|&nbsp;
    💬 (11) 93011-9335 &nbsp;|&nbsp;
    ✉️ sac@luvidarte.com.br
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================
# CONFIGURAÇÕES DAS PLANILHAS
# ============================================
ID_PLANILHA = "1DCmwFzQvbQYDBsQft17VO9szjixgq1Bp09dYTfu142w"
NOME_ABA = "base"
NOME_ABA_PROMO = "PROMO"
NOME_ABA_ST = "BASE_ST"
NOME_ABA_NORMAL = "NORMAL"
NOME_ABA_ISENTO = "ISENTO"

# ============================================
# CARREGAR DADOS
# ============================================
with st.spinner("🔄 Carregando catálogo..."):
    dados = carregar_planilha(ID_PLANILHA, NOME_ABA)
    dados_promo = carregar_planilha_promo(ID_PLANILHA, NOME_ABA_PROMO)
    dados_st = carregar_base_st(ID_PLANILHA, NOME_ABA_ST)
    dados_normal = carregar_descontos_normal(ID_PLANILHA, NOME_ABA_NORMAL)
    dados_isento = carregar_descontos_isento(ID_PLANILHA, NOME_ABA_ISENTO)

if dados.empty:
    st.stop()

# ============================================
# SIDEBAR - FILTROS E CONFIGURAÇÕES
# ============================================

st.sidebar.header("🔍 FILTRAR PRODUTOS")
st.sidebar.markdown(f"📊 **Total encontrado:** {len(dados)} produtos")

st.sidebar.markdown("---")
st.sidebar.header("⚙️ CONFIGURAÇÕES")

uf_selecionada = st.sidebar.selectbox(
    "📍 UF (ICMS)",
    options=UFS_BRASIL,
    index=UFS_BRASIL.index("SP"),
    help="Selecione a UF para cálculo do ICMS e descontos"
)

# Lista de grupos incluindo "Promoção"
grupos = ["Todos"] + sorted(dados['GRUPO'].unique())
# Adicionar "Promoção" como opção especial
if "Promoção" not in grupos:
    grupos.insert(1, "Promoção")
grupo_escolhido = st.sidebar.selectbox("📦 Grupo", grupos)

busca_referencia = st.sidebar.text_input("🔎 Buscar por Referência", placeholder="Ex: 10, 40, 60...")

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

cliente_isento = st.sidebar.checkbox("🏷️ Cliente Isento", value=False, help="Ative esta opção para clientes isentos")

st.sidebar.markdown("---")
st.sidebar.markdown("### 💳 FORMA DE PAGAMENTO")

# Removidas as opções 75 e 90
forma_pagamento = st.sidebar.radio(
    "Selecione a condição:",
    options=["PREÇO BASE", "VISTA", "30", "45", "60"],
    index=0,
    help="PREÇO BASE: Sem desconto | VISTA: À vista | Demais: Prazos"
)

st.sidebar.markdown("---")

if st.sidebar.button("🔄 Limpar Filtros"):
    st.cache_data.clear()
    st.session_state.pagina_atual = 1
    st.rerun()

# ============================================
# DETERMINAR ICMS BASEADO NA UF
# ============================================
icms_uf = determinar_icms_por_uf(uf_selecionada)

# ============================================
# SELECIONAR A TABELA DE DESCONTO CORRETA
# ============================================
if cliente_isento:
    tabela_desconto = dados_isento
    tipo_cliente = "ISENTO"
else:
    tabela_desconto = dados_normal
    tipo_cliente = "NORMAL"

# ============================================
# APLICAR FILTROS
# ============================================
dados_filtrados = dados.copy()

# Filtro especial para "Promoção"
if grupo_escolhido == "Promoção":
    # Mostrar apenas produtos onde a coluna Promo contém "SIM" (case insensitive)
    dados_filtrados = dados_filtrados[dados_filtrados['Promo'].astype(str).str.upper().str.contains('SIM', na=False)]
elif grupo_escolhido != "Todos":
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
# PAGINAÇÃO - 9 ITENS POR PÁGINA (responsivo)
# ============================================
ITENS_POR_PAGINA = 9
total_encontrados = len(dados_filtrados)
total_paginas = max(1, (total_encontrados + ITENS_POR_PAGINA - 1) // ITENS_POR_PAGINA)

if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = 1

if 'ultimos_filtros' not in st.session_state:
    st.session_state.ultimos_filtros = (grupo_escolhido, faixa_preco, busca_referencia, uf_selecionada, cliente_isento, forma_pagamento)
else:
    filtros_atual = (grupo_escolhido, faixa_preco, busca_referencia, uf_selecionada, cliente_isento, forma_pagamento)
    if filtros_atual != st.session_state.ultimos_filtros:
        st.session_state.pagina_atual = 1
        st.session_state.ultimos_filtros = filtros_atual

if st.session_state.pagina_atual > total_paginas:
    st.session_state.pagina_atual = total_paginas
if st.session_state.pagina_atual < 1:
    st.session_state.pagina_atual = 1

indice_inicio = (st.session_state.pagina_atual - 1) * ITENS_POR_PAGINA
indice_fim = min(indice_inicio + ITENS_POR_PAGINA, total_encontrados)
dados_pagina = dados_filtrados.iloc[indice_inicio:indice_fim]

# ============================================
# EXIBIR PRODUTOS - Layout responsivo
# ============================================
st.markdown(f"## ✨ Produtos Encontrados: {total_encontrados}")

# Informações em colunas responsivas
col_info1, col_info2, col_info3, col_info4 = st.columns(4)
with col_info1:
    st.info(f"🏢 **UF:** {uf_selecionada} (ICMS {icms_uf}%)")
with col_info2:
    st.info(f"📋 **Cliente:** {tipo_cliente}")
with col_info3:
    if forma_pagamento == "PREÇO BASE":
        st.warning(f"💰 **Condição:** {forma_pagamento} (Sem desconto)")
    else:
        st.success(f"💰 **Condição:** {forma_pagamento} dias")
with col_info4:
    if grupo_escolhido == "Promoção":
        st.success(f"🏷️ **Grupo:** {grupo_escolhido} - Ofertas Especiais!")
    else:
        st.info(f"📦 **Grupo:** {grupo_escolhido}")

st.markdown("---")

if dados_filtrados.empty:
    st.warning("😕 Nenhum produto encontrado.")
else:
    # Grid responsivo com 3 colunas
    colunas = st.columns(3)
    
    for posicao, (indice, produto) in enumerate(dados_pagina.iterrows()):
        # Verificar se o produto está em promoção
        is_promo = False
        promo_valor_str = str(produto.get('Promo', '')).strip().upper()
        if 'SIM' in promo_valor_str:
            is_promo = True
        
        # Buscar preço promocional se aplicável
        preco_promo = None
        if is_promo and not dados_promo.empty:
            preco_promo = buscar_preco_promo(produto['Referência'], uf_selecionada, dados_promo)
            
            # Debug - remover em produção
            if preco_promo is not None:
                st.session_state['debug_promo'] = f"Promo encontrado: R$ {preco_promo:.2f}"
        
        with colunas[posicao % 3]:
            # Definir classe do card baseada em promoção
            card_class = "product-card promo-card" if is_promo else "product-card normal-card"
            
            # HTML do card
            st.markdown(f"""
            <div class='{card_class}'>
                <span class='ref'>🔖 REF: {produto['Referência']}</span>
                <p class='product-name'>{produto['Descrição']}</p>
                <p class='product-category'>{produto['GRUPO']}</p>
            """, unsafe_allow_html=True)
            
            # Adicionar badge apropriado
            if is_promo:
                st.markdown(f"<div class='promo-badge'>🔥 PROMOÇÃO</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='tabela-badge'>📋 TABELA</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)  # Fechar product-card
            
            # Imagem do produto
            if pd.notna(produto.get('imagem_url')) and produto.get('imagem_url'):
                try:
                    st.image(produto['imagem_url'], use_container_width=True)
                except:
                    st.image("https://via.placeholder.com/300x200?text=Sem+Imagem", use_container_width=True)
            else:
                st.image("https://via.placeholder.com/300x200?text=Sem+Imagem", use_container_width=True)
            
            # ML e Medidas - usando nova formatação
            if 'ml' in produto:
                ml_formatado = formatar_ml(produto.get('ml'))
                if ml_formatado:
                    st.markdown(f"📏 **{ml_formatado}**")
                else:
                    st.markdown(f"📏 **---**")
            
            if pd.notna(produto.get('Medidas')) and str(produto['Medidas']).strip():
                st.markdown(f"📐 {produto['Medidas']}")
            
            # ========================================
            # CÁLCULO DE PREÇOS
            # ========================================
            
            # Verificar se é promoção e se encontrou preço na planilha PROMO
            if is_promo and preco_promo is not None and preco_promo > 0:
                # PRODUTO EM PROMOÇÃO - Usar preço da planilha PROMO
                preco_base = preco_promo
                
                st.markdown(f"🏷️ **Preço Promocional:** R$ {preco_base:.2f}")
                
                # Para promoção: NÃO aplicar descontos da tabela NORMAL/ISENTO
                # Apenas aplicar +10% se cliente isento
                if cliente_isento:
                    preco_base = preco_base * 1.10  # +10%
                    st.caption("✨ +10% (Cliente Isento)")
                    st.markdown(f"💰 **Preço com acréscimo:** R$ {preco_base:.2f}")
                
                # Aplicar desconto de 4% APENAS se for pagamento à vista
                if forma_pagamento == "VISTA":
                    desconto_percentual = 0.04  # 4% fixo para promoções à vista
                    valor_com_desconto = preco_base * (1 - desconto_percentual)
                    st.markdown(f"🎯 **Desconto à vista:** 4%")
                    st.markdown(f"💰 **Valor com desconto:** R$ {valor_com_desconto:.2f}")
                else:
                    desconto_percentual = 0.0
                    valor_com_desconto = preco_base
                    if forma_pagamento != "PREÇO BASE":
                        st.markdown(f"🎯 **Desconto:** Não aplicável em promoção")
                
                # Calcular IPI (mesma regra existente)
                ncm_produto = produto.get('NCM', '')
                ipi_percentual = buscar_ipi(ncm_produto, dados_st)
                valor_ipi = valor_com_desconto * ipi_percentual
                
                # Calcular ST (mesma regra existente)
                aliquota_st = buscar_aliquota_st(ncm_produto, uf_selecionada, dados_st)
                
                if cliente_isento:
                    valor_st = 0.0
                    aliquota_st = 0.0
                else:
                    valor_st = valor_com_desconto * aliquota_st
                
                valor_total = valor_com_desconto + valor_ipi + valor_st
                
                # Exibir IPI
                if ipi_percentual > 0:
                    st.markdown(f"🔷 **IPI:** {ipi_percentual*100:.2f}% = R$ {valor_ipi:.2f}")
                else:
                    st.markdown(f"🔷 **IPI:** Não aplicável")
                
                # Exibir ST
                if cliente_isento:
                    st.markdown(f"🟣 **ST ({uf_selecionada}):** Cliente Isento - ST não aplicada")
                    st.markdown(f"✅ **TOTAL COM IPI:** R$ {valor_com_desconto + valor_ipi:.2f}")
                elif aliquota_st > 0:
                    st.markdown(f"🟣 **Alíq. ST ({uf_selecionada}):** {aliquota_st*100:.2f}%")
                    st.markdown(f"📊 **Valor ST:** R$ {valor_st:.2f}")
                    st.markdown(f"✅ **TOTAL COM IPI + ST:** R$ {valor_total:.2f}")
                else:
                    st.markdown(f"🟣 **ST ({uf_selecionada}):** Não aplicável")
                    st.markdown(f"✅ **TOTAL COM IPI:** R$ {valor_com_desconto + valor_ipi:.2f}")
                
            else:
                # PRODUTO NORMAL - Usar cálculo existente
                preco_bruto = produto['Preço'] if pd.notna(produto['Preço']) and produto['Preço'] > 0 else 0
                
                if is_promo and preco_promo is None:
                    st.caption("⚠️ Promoção disponível mas preço não encontrado na planilha")
                
                if forma_pagamento == "PREÇO BASE":
                    desconto_percentual = 0.0
                else:
                    desconto_percentual = buscar_desconto(icms_uf, forma_pagamento, tabela_desconto)
                
                valor_com_desconto = preco_bruto * (1 - desconto_percentual)
                ncm_produto = produto.get('NCM', '')
                ipi_percentual = buscar_ipi(ncm_produto, dados_st)
                valor_ipi = valor_com_desconto * ipi_percentual
                aliquota_st = buscar_aliquota_st(ncm_produto, uf_selecionada, dados_st)
                
                if cliente_isento:
                    valor_st = 0.0
                    aliquota_st = 0.0
                else:
                    valor_st = valor_com_desconto * aliquota_st
                
                valor_total = valor_com_desconto + valor_ipi + valor_st
                
                if preco_bruto > 0:
                    st.markdown(f"💰 **Preço Bruto:** R$ {preco_bruto:.2f}")
                else:
                    st.markdown(f"💰 **Preço Bruto:** Sob consulta")
                
                if desconto_percentual > 0:
                    valor_desconto_reais = preco_bruto * desconto_percentual
                    st.markdown(f"🎯 **Desconto:** {desconto_percentual*100:.2f}% (R$ {valor_desconto_reais:.2f})")
                    st.markdown(f"📉 **Valor com Desconto:** R$ {valor_com_desconto:.2f}")
                elif forma_pagamento != "PREÇO BASE":
                    st.markdown(f"🎯 **Desconto:** 0,00%")
                    st.markdown(f"📉 **Valor com Desconto:** R$ {valor_com_desconto:.2f}")
                
                if ipi_percentual > 0:
                    st.markdown(f"🔷 **IPI:** {ipi_percentual*100:.2f}% = R$ {valor_ipi:.2f}")
                else:
                    st.markdown(f"🔷 **IPI:** Não aplicável")
                
                if cliente_isento:
                    st.markdown(f"🟣 **ST ({uf_selecionada}):** Cliente Isento - ST não aplicada")
                    if preco_bruto > 0:
                        st.markdown(f"✅ **TOTAL COM IPI:** R$ {valor_com_desconto + valor_ipi:.2f}")
                elif aliquota_st > 0:
                    st.markdown(f"🟣 **Alíq. ST ({uf_selecionada}):** {aliquota_st*100:.2f}%")
                    st.markdown(f"📊 **Valor ST:** R$ {valor_st:.2f}")
                    st.markdown(f"✅ **TOTAL COM IPI + ST:** R$ {valor_total:.2f}")
                else:
                    st.markdown(f"🟣 **ST ({uf_selecionada}):** Não aplicável")
                    if preco_bruto > 0:
                        st.markdown(f"✅ **TOTAL COM IPI:** R$ {valor_com_desconto + valor_ipi:.2f}")
            
            # Peso
            if pd.notna(produto.get('Peso Liq S/Cx')):
                try:
                    peso = float(produto['Peso Liq S/Cx'])
                    st.caption(f"⚖️ Peso: {peso:.3f} kg")
                except:
                    st.caption(f"⚖️ Peso: {produto['Peso Liq S/Cx']}")
            
            st.markdown("---")
    
    if total_paginas > 1:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div style="text-align: center; padding: 20px; background: #fafafa; border-radius: 12px; border: 1px solid #E0E0E0;">', unsafe_allow_html=True)
            
            pagina_selecionada = st.selectbox(
                "📄 Navegar para página",
                options=list(range(1, total_paginas + 1)),
                index=st.session_state.pagina_atual - 1,
                key="page_select_central"
            )
            
            if pagina_selecionada != st.session_state.pagina_atual:
                st.session_state.pagina_atual = pagina_selecionada
                st.rerun()
            
            st.markdown(f"""
            <div style='text-align: center; margin-top: 8px; font-size: 12px; color: #666;'>
                Mostrando {indice_inicio + 1} - {min(indice_fim, total_encontrados)} de {total_encontrados} produtos
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        progresso = st.session_state.pagina_atual / total_paginas
        st.progress(progresso, text=f"📄 Página {st.session_state.pagina_atual} de {total_paginas}")

# ============================================
# RODAPÉ COM REDES SOCIAIS
# ============================================
st.markdown("---")

st.markdown("""
<div class='horario-atendimento'>
    <span class='horario-label'>🕒 Horário de Atendimento:</span>
    <span class='horario-text'> Segunda a Quinta: 07:00 às 17:00 | Sexta: 07:00 às 16:00</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='social-links-container'>
    <div class='social-title'>Siga nossas redes sociais:</div>
    <div class='social-links'>
        <a href='https://www.facebook.com/luvidarte' target='_blank' class='social-link' style='color: #3b5998;'>
            Facebook
        </a>
        <a href='https://www.instagram.com/luvidartevidros/' target='_blank' class='social-link' style='color: #E4405F;'>
            Instagram
        </a>
        <a href='https://www.linkedin.com/company/luvidarte/' target='_blank' class='social-link' style='color: #0077b5;'>
            LinkedIn
        </a>
        <a href='https://www.youtube.com/@luvidartevidros7291' target='_blank' class='social-link' style='color: #ff0000;'>
            YouTube
        </a>
        <a href='https://wa.me/5511930119335?text=Olá! Gostaria de informações sobre os produtos Luvidarte' target='_blank' class='social-link' style='color: #25D366;'>
            WhatsApp
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='contact-footer'>
    📞 Fixo: (11) 4676-9000 | 💬 WhatsApp: (11) 93011-9335 | ✉️ sac@luvidarte.com.br
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class='footer-bottom'>
    © 2026 Luvidarte - Canal exclusivo para empresas
</div>
""", unsafe_allow_html=True)

# ============================================
# WHATSAPP FLUTUANTE
# ============================================
st.markdown("""
<style>
.whatsapp-float {
    position: fixed;
    bottom: 80px;
    right: 20px;
    background-color: #25D366;
    color: white;
    border-radius: 50px;
    padding: 10px 18px;
    text-align: center;
    font-size: 13px;
    font-weight: bold;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    z-index: 999999 !important;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
}
.whatsapp-float:hover {
    transform: scale(1.05);
    background-color: #075E54;
}
.whatsapp-float a {
    color: white;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 8px;
}
@media (max-width: 480px) {
    .whatsapp-float {
        bottom: 70px;
        right: 15px;
        padding: 10px 14px;
    }
    .whatsapp-float span:last-child {
        font-size: 12px;
    }
    .whatsapp-float span:first-child {
        font-size: 18px;
    }
}
@media (min-width: 481px) and (max-width: 768px) {
    .whatsapp-float {
        bottom: 80px;
        right: 20px;
    }
}
</style>
<div class="whatsapp-float">
    <a href="https://wa.me/5511930119335?text=Olá! Gostaria de informações sobre os produtos Luvidarte" target="_blank">
        <span>💬</span>
        <span>WhatsApp (11) 93011-9335</span>
    </a>
</div>
""", unsafe_allow_html=True)
