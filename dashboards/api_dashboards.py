import streamlit as st
import requests
import json
import pandas as pd

# Configuração da página DEVE ser a primeira chamada do Streamlit
st.set_page_config(
    page_title="BookFlow API Dashboard",
    page_icon="📚",
    layout="wide"
)

BASE_URL = "http://localhost:8000/api/v1"

# Teste de conectividade na inicialização
try:
    health_resp = requests.get(f"{BASE_URL}/health", timeout=5)
    if health_resp.status_code == 200:
        st.sidebar.success(f"✅ API conectada: {health_resp.json()['message']}")
    else:
        st.sidebar.error(f"❌ API retornou status: {health_resp.status_code}")
except Exception as e:
    st.sidebar.error(f"❌ Erro de conectividade: {str(e)}")

st.title("📚 Painel da API BookFlow")
st.markdown("---")

# Sidebar para autenticação
st.sidebar.header("🔐 Autenticação")

# Inicializar variáveis de sessão se não existirem
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'refresh_token' not in st.session_state:
    st.session_state.refresh_token = None

# Login
with st.sidebar.expander("Login", expanded=True):
    username = st.text_input("Usuário:", value="admin")
    password = st.text_input("Senha:", type="password", value="password123")
    
    if st.button("🔑 Fazer Login"):
        login_data = {"username": username, "password": password}
        
        try:
            # Corrige endpoint de login para '/api/v1/login' (sem '/auth')
            resp = requests.post(f"{BASE_URL}/login", json=login_data, timeout=10)
            
            if resp.status_code == 200:
                token_data = resp.json()
                st.session_state.access_token = token_data.get("access_token")
                st.session_state.refresh_token = token_data.get("refresh_token")
                st.sidebar.success("✅ Login realizado com sucesso!")
                st.rerun()
            else:
                st.sidebar.error(f"❌ Erro de login: {resp.status_code}")
        except Exception as e:
            st.sidebar.error(f"❌ Erro de conexão: {str(e)}")

# Token manual (fallback)
manual_token = st.sidebar.text_input("Ou insira token manualmente:", type="password")

# Determinar qual token usar
token = None
if manual_token:
    token = manual_token
    st.sidebar.success("🔑 Token manual inserido")
elif st.session_state.access_token:
    token = st.session_state.access_token
    st.sidebar.success("🔑 Login realizado com sucesso")

if not token:
    st.warning("⚠️ Por favor, faça login ou insira um token para acessar a API.")
    st.info("👆 Use a barra lateral para fazer login com as credenciais: **admin** / **password123**")
    
    # Mostrar uma versão limitada do dashboard
    st.subheader("🔍 Preview do Dashboard")
    st.info("Após fazer login, você terá acesso a todas as funcionalidades:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**📚 Livros**\n- Listar todos os livros\n- Top livros por rating\n- Filtrar por preço")
    with col2:
        st.markdown("**📊 Categorias**\n- Listar categorias\n- Estatísticas gerais\n- Estatísticas por categoria")
    with col3:
        st.markdown("**🤖 ML & Mais**\n- Machine Learning\n- Web Scraping\n- Health Check")
    
    st.stop()

headers = {"Authorization": f"Bearer {token}"}

# Criar abas para organizar as funcionalidades
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📚 Livros", "📊 Categorias", "📈 Estatísticas", "🤖 Machine Learning", 
    "🕷️ Scraping", "🏥 Health Check", "🔄 Refresh Token"
])

# TAB 1: LIVROS
with tab1:
    st.header("📚 Gerenciamento de Livros")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔹 Listar Todos os Livros")
        if st.button("📋 Listar livros", key="list_books"):
            try:
                resp = requests.get(f"{BASE_URL}/books", headers=headers)
                if resp.status_code == 200:
                    books_data = resp.json()
                    if books_data:
                        df = pd.DataFrame(books_data)
                        st.dataframe(df, use_container_width=True)
                        st.info(f"📊 Total de livros: {len(books_data)}")
                    else:
                        st.info("📭 Nenhum livro encontrado.")
                else:
                    st.error(f"❌ Erro: {resp.status_code} - {resp.json().get('detail')}")
            except Exception as e:
                st.error(f"❌ Erro de conexão: {str(e)}")
    
    with col2:
        st.subheader("⭐ Top Livros por Rating")
        top_n = st.slider("Quantidade:", 1, 20, 5, key="top_rating_slider")
        if st.button("🏆 Buscar top livros", key="top_books"):
            try:
                resp = requests.get(f"{BASE_URL}/books/top-rated?number_items={top_n}", headers=headers)
                if resp.status_code == 200:
                    top_books = resp.json()
                    if top_books:
                        df = pd.DataFrame(top_books)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("📭 Nenhum livro encontrado.")
                else:
                    st.error(f"❌ Erro: {resp.status_code} - {resp.json().get('detail')}")
            except Exception as e:
                st.error(f"❌ Erro de conexão: {str(e)}")
    
    st.subheader("💰 Filtrar por Faixa de Preço")
    col3, col4 = st.columns(2)
    with col3:
        price_min = st.number_input("Preço mínimo:", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    with col4:
        price_max = st.number_input("Preço máximo:", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
    
    if st.button("💸 Buscar por faixa de preço", key="price_range"):
        try:
            resp = requests.get(
                f"{BASE_URL}/books/price_range?min={price_min}&max={price_max}",
                headers=headers
            )
            if resp.status_code == 200:
                price_books = resp.json()
                if price_books:
                    df = pd.DataFrame(price_books)
                    st.dataframe(df, use_container_width=True)
                    st.info(f"📊 Livros encontrados na faixa £{price_min} - £{price_max}: {len(price_books)}")
                else:
                    st.info("📭 Nenhum livro encontrado nesta faixa de preço.")
            else:
                st.error(f"❌ Erro: {resp.status_code} - {resp.json().get('detail')}")
        except Exception as e:
            st.error(f"❌ Erro de conexão: {str(e)}")

# TAB 2: CATEGORIAS
with tab2:
    st.header("📊 Categorias de Livros")
    
    if st.button("📂 Listar todas as categorias", key="list_categories"):
        try:
            resp = requests.get(f"{BASE_URL}/categories", headers=headers)
            if resp.status_code == 200:
                categories = resp.json()
                if categories:
                    df = pd.DataFrame(categories)
                    st.dataframe(df, use_container_width=True)
                    st.info(f"📊 Total de categorias: {len(categories)}")
                else:
                    st.info("📭 Nenhuma categoria encontrada.")
            else:
                st.error(f"❌ Erro: {resp.status_code} - {resp.json().get('detail')}")
        except Exception as e:
            st.error(f"❌ Erro de conexão: {str(e)}")

# TAB 3: ESTATÍSTICAS
with tab3:
    st.header("📈 Estatísticas dos Livros")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Visão Geral")
        if st.button("📈 Obter estatísticas gerais", key="stats_overview"):
            try:
                resp = requests.get(f"{BASE_URL}/stats-overview", headers=headers)
                if resp.status_code == 200:
                    stats = resp.json()
                    st.json(stats)
                else:
                    st.error(f"❌ Erro: {resp.status_code} - {resp.json().get('detail')}")
            except Exception as e:
                st.error(f"❌ Erro de conexão: {str(e)}")
    
    with col2:
        st.subheader("📊 Estatísticas por Categoria")
        if st.button("📊 Obter estatísticas por categoria", key="stats_categories"):
            try:
                resp = requests.get(f"{BASE_URL}/stats-categories", headers=headers)
                if resp.status_code == 200:
                    stats_cat = resp.json()
                    if stats_cat:
                        df = pd.DataFrame(stats_cat)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("📭 Nenhuma estatística encontrada.")
                else:
                    st.error(f"❌ Erro: {resp.status_code} - {resp.json().get('detail')}")
            except Exception as e:
                st.error(f"❌ Erro de conexão: {str(e)}")

# TAB 4: MACHINE LEARNING
with tab4:
    st.header("🤖 Machine Learning")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🔧 Features ML")
        if st.button("🔧 Obter features", key="ml_features"):
            try:
                resp = requests.get(f"{BASE_URL}/ml/features", headers=headers)
                if resp.status_code == 200:
                    features = resp.json()
                    st.json(features)
                else:
                    st.error(f"❌ Erro: {resp.status_code} - {resp.json().get('detail')}")
            except Exception as e:
                st.error(f"❌ Erro de conexão: {str(e)}")
    
    with col2:
        st.subheader("📚 Dados de Treinamento")
        if st.button("📚 Obter dados de treinamento", key="ml_training"):
            try:
                resp = requests.get(f"{BASE_URL}/ml/training-data", headers=headers)
                if resp.status_code == 200:
                    training_data = resp.json()
                    st.json(training_data)
                else:
                    st.error(f"❌ Erro: {resp.status_code} - {resp.json().get('detail')}")
            except Exception as e:
                st.error(f"❌ Erro de conexão: {str(e)}")
    
    with col3:
        st.subheader("🔮 Predições")
        st.text_area("Dados para predição (JSON):", 
                    value='{"model_type": "recommendation", "features": [1, 2, 3]}',
                    key="prediction_input")
        
        if st.button("🔮 Fazer predição", key="ml_prediction"):
            try:
                prediction_data = json.loads(st.session_state.prediction_input)
                resp = requests.post(f"{BASE_URL}/ml/predictions", 
                                   json=prediction_data, headers=headers)
                if resp.status_code == 200:
                    prediction = resp.json()
                    st.json(prediction)
                else:
                    st.error(f"❌ Erro: {resp.status_code} - {resp.json().get('detail')}")
            except json.JSONDecodeError:
                st.error("❌ JSON inválido nos dados de predição")
            except Exception as e:
                st.error(f"❌ Erro de conexão: {str(e)}")

# TAB 5: SCRAPING
with tab5:
    st.header("🕷️ Web Scraping")
    
    st.warning("⚠️ Esta operação pode demorar alguns minutos para ser concluída.")
    
    if st.button("🚀 Iniciar Scraping", key="trigger_scraping"):
        try:
            with st.spinner("🕷️ Executando scraping... Isso pode levar alguns minutos."):
                resp = requests.post(f"{BASE_URL}/scraping/trigger", headers=headers)
                if resp.status_code == 200:
                    scraping_result = resp.json()
                    st.success("✅ Scraping concluído com sucesso!")
                    st.json(scraping_result)
                else:
                    st.error(f"❌ Erro: {resp.status_code} - {resp.json().get('detail')}")
        except Exception as e:
            st.error(f"❌ Erro de conexão: {str(e)}")

# TAB 6: HEALTH CHECK
with tab6:
    st.header("🏥 Health Check")
    
    if st.button("🩺 Verificar saúde da API", key="health_check"):
        try:
            resp = requests.get(f"{BASE_URL}/health", headers=headers)
            if resp.status_code == 200:
                health = resp.json()
                st.success("✅ API está funcionando corretamente!")
                st.json(health)
            else:
                st.error(f"❌ Erro: {resp.status_code} - {resp.json().get('detail')}")
        except Exception as e:
            st.error(f"❌ Erro de conexão: {str(e)}")

# TAB 7: REFRESH TOKEN
with tab7:
    st.header("🔄 Refresh Token")
    
    if hasattr(st.session_state, 'refresh_token') and st.session_state.refresh_token:
        st.info(f"🔑 Refresh token disponível")
        
        if st.button("🔄 Renovar Access Token", key="refresh_token_button"):
            try:
                refresh_data = {"refresh_token": st.session_state.refresh_token}
                # Corrige endpoint de refresh para '/api/v1/refresh'
                resp = requests.post(f"{BASE_URL}/refresh", json=refresh_data)
                if resp.status_code == 200:
                    token_data = resp.json()
                    st.session_state.access_token = token_data.get("access_token")
                    st.success("✅ Token renovado com sucesso!")
                    st.rerun()
                else:
                    st.error(f"❌ Erro: {resp.status_code} - {resp.json().get('detail')}")
            except Exception as e:
                st.error(f"❌ Erro de conexão: {str(e)}")
    else:
        st.warning("⚠️ Nenhum refresh token disponível. Faça login primeiro.")

st.markdown("---")
st.markdown("**📚 BookFlow API Dashboard** - Desenvolvido para o Tech Challenge FIAP")
