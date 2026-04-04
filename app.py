import streamlit as st
import pandas as pd
import numpy as np

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Catálogo Luvidarte",
    page_icon="🏺",
    layout="wide"
)

# ============================================
# SUAS CONFIGURAÇÕES
# ============================================
ID_PLANILHA = "1DCmwFzQvbQYDBsQft17VO9szjixgq1Bp09dYTfu142w"
NOME_ABA = "base"

# ============================================
# ESTILO PERSONALIZADO
# ============================================
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 48px;
        color: #8B4513;
    }
    .price {
        color: #2e6b2f;
        font-size: 28px;
        font-weight: bold;
    }
    .product-card {
        background-color: #f9f9f9;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# TÍTULO
# ============================================
st.markdown("<h1 class='main-title'>🏺 Luvidarte - Catálogo Virtual</h1>", unsafe_allow_html=True)
st.markdown("### Peças em Resina e Decoração")
st.markdown("---")

# ============================================
# FUNÇÃO PARA CARREGAR A PLANILHA
# ============================================
@st.cache_data(ttl=600)
def carregar_planilha(id_planilha, nome_aba="base"):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{id_planilha}/gviz/tq?tqx=out:csv&sheet={nome_aba}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        
        # Converte preço para número
        if 'Preço Bruto - 2024' in df.columns:
            df['Preço Bruto - 2024'] = pd.to_numeric(df['Preço Bruto - 2024'], errors='coerce')
        
        # Preenche valores vazios
        df['GRUPO'] = df['GRUPO'].fillna('Sem Grupo')
        df['Descrição'] = df['Descrição'].fillna('Produto sem descrição')
        df['Referência'] = df['Referência'].fillna('').astype(str)
        
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

# Mostra total REAL de produtos
total_produtos_reais = len(dados)
st.sidebar.info(f"📊 Total no catálogo: **{total_produtos_reais} produtos**")

# ============================================
# FILTROS NA BARRA LATERAL
# ============================================
st.sidebar.header("🔍 Filtros")

# Filtro de Grupo APENAS (sem Família)
grupos = ["Todos"] + sorted(dados['GRUPO'].unique())
grupo_escolhido = st.sidebar.selectbox("📦 Grupo de Produto", grupos)

# Filtro de Preço (ignora NaN)
precos_validos = dados['Preço Bruto - 2024'].dropna()
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

# Busca por REFERÊNCIA (não mais por descrição)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔎 Buscar por Referência")
busca_referencia = st.sidebar.text_input(
    "Digite a referência do produto", 
    placeholder="Ex: 10, 40, 60, 73, 74..."
)

# Botão para resetar filtros
if st.sidebar.button("🔄 Resetar Filtros"):
    st.cache_data.clear()
    st.rerun()

# ============================================
# APLICAR FILTROS
# ============================================
dados_filtrados = dados.copy()

# Aplica grupo
if grupo_escolhido != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados['GRUPO'] == grupo_escolhido]

# Aplica preço
if len(precos_validos) > 0:
    dados_filtrados = dados_filtrados[
        (dados_filtrados['Preço Bruto - 2024'].isna()) |  
        ((dados_filtrados['Preço Bruto - 2024'] >= faixa_preco[0]) & 
         (dados_filtrados['Preço Bruto - 2024'] <= faixa_preco[1]))
    ]

# Aplica busca por REFERÊNCIA
if busca_referencia:
    dados_filtrados = dados_filtrados[
        dados_filtrados['Referência'].str.contains(busca_referencia, case=False, na=False)
    ]

# ============================================
# ESTATÍSTICAS
# ============================================
st.header(f"✨ Produtos Encontrados: {len(dados_filtrados)}")

# Mostra quantos foram filtrados
if len(dados_filtrados) < len(dados):
    st.caption(f"📌 Filtro aplicado: {len(dados_filtrados)} de {len(dados)} produtos")

# Se está buscando por referência, mostra qual
if busca_referencia:
    st.info(f"🔎 Buscando por referência que contenha: **{busca_referencia}**")

# ============================================
# EXIBIR PRODUTOS
# ============================================
if dados_filtrados.empty:
    st.warning("😕 Nenhum produto encontrado com esses filtros.")
    st.info("💡 Dicas:")
    st.info("- Digite apenas o número da referência (ex: 10, 40, 60)")
    st.info("- Remova o filtro de grupo para ver todos")
    st.info("- Amplie a faixa de preço")
else:
    # Criar 3 colunas
    colunas = st.columns(3)
    
    # Para cada produto
    for posicao, (indice, produto) in enumerate(dados_filtrados.iterrows()):
        with colunas[posicao % 3]:
            # Card do produto
            st.markdown("---")
            
            # Referência em destaque
            ref_produto = produto['Referência'] if pd.notna(produto['Referência']) else "---"
            st.markdown(f"### 🔖 Ref: {ref_produto}")
            
            # Nome do produto
            nome_produto = produto['Descrição'] if pd.notna(produto['Descrição']) else "Produto"
            st.markdown(f"**{nome_produto}**")
            
            # Imagem
            if pd.notna(produto.get('imagem_url')) and produto.get('imagem_url'):
                try:
                    st.image(produto['imagem_url'], use_container_width=True)
                except:
                    st.image("https://via.placeholder.com/300x200?text=Imagem+Indisponível", use_container_width=True)
            else:
                st.image("https://via.placeholder.com/300x200?text=Sem+Imagem", use_container_width=True)
            
            # Informações técnicas
            if pd.notna(produto.get('ml')):
                st.markdown(f"**Capacidade:** {produto['ml']} ml")
            
            if pd.notna(produto.get('Medidas')):
                st.markdown(f"**Medidas:** {produto['Medidas']}")
            
            # Preço
            preco = produto['Preço Bruto - 2024']
            if pd.notna(preco) and preco > 0:
                st.markdown(f"<p class='price'>R$ {preco:.2f}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p class='price'>💰 Preço sob consulta</p>", unsafe_allow_html=True)
            
            # Peso
            if pd.notna(produto.get('Peso Liq S/Cx')):
                st.markdown(f"⚖️ Peso: {produto['Peso Liq S/Cx']} kg")
            
            # Grupo
            if pd.notna(produto.get('GRUPO')):
                st.caption(f"📦 {produto['GRUPO']}")
            
            # Botão de orçamento
            chave_botao = f"btn_produto_{indice}"
            
            if st.button("📞 Solicitar Orçamento", key=chave_botao):
                st.success(f"✅ Produto **{nome_produto}** (Ref: {ref_produto}) selecionado!")
                st.info("📱 Entre em contato pelo WhatsApp para mais informações")
            
            st.markdown("---")

# ============================================
# RODAPÉ
# ============================================
with st.expander("ℹ️ Informações do Catálogo"):
    st.markdown(f"""
    **Estatísticas:**
    - Total de produtos: **{len(dados)}**
    - Produtos com preço: **{len(dados[dados['Preço Bruto - 2024'].notna()])}**
    - Grupos disponíveis: **{len(dados['GRUPO'].unique())}**
    
    **Como buscar por referência:**
    - Digite o número da referência (ex: 10, 40, 60, 73, 74)
    - A busca encontra referências que contenham o número digitado
    
    **Como usar:**
    - Use os filtros na lateral esquerda
    - Clique em "Solicitar Orçamento" no produto desejado
    """)