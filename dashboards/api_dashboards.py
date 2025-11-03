import streamlit as st
import requests
import os

# Usar API em produção por padrão, localhost para desenvolvimento
BASE_URL = os.getenv("API_URL", "https://book-flow-api-e1ac898fc906.herokuapp.com/api/v1")

st.title("📚 Painel da API de Livros")

token = st.text_input("Token de acesso (Bearer):", type="password")

if token:
    headers = {"Authorization": f"Bearer {token}"}

    st.subheader("🔹 Livros disponíveis")
    if st.button("Listar livros"):
        resp = requests.get(f"{BASE_URL}/books", headers=headers)
        if resp.status_code == 200:
            st.dataframe(resp.json())
        else:
            st.error(f"Erro: {resp.status_code} - {resp.json().get('detail')}")

    st.subheader("⭐ Top livros por rating")
    top_n = st.slider("Quantidade:", 1, 10, 5)
    if st.button("Buscar top livros"):
        resp = requests.get(f"{BASE_URL}/books/top-rated?number_items={top_n}", headers=headers)
        if resp.status_code == 200:
            st.dataframe(resp.json())
        else:
            st.error(f"Erro: {resp.status_code} - {resp.json().get('detail')}")

    st.subheader("💰 Top livros por rating")
    top_min = st.slider("Preço mínimo:", 0.0, 100.0, 0.0)
    top_max = st.slider("Preço máximo:", 0.0, 100.0, 100.0)
    if st.button("Buscar por preços"):
        resp = requests.get(
            f"{BASE_URL}/books/price_range?min={top_min}&max={top_max}",
            headers=headers
        )
        if resp.status_code == 200:
            st.dataframe(resp.json())
        else:
            st.error(f"Erro: {resp.status_code} - {resp.json().get('detail')}")
