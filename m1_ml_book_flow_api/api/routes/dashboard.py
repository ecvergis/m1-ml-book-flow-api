"""
Rotas para o dashboard Streamlit integrado.

Este módulo fornece endpoints para servir o dashboard Streamlit na mesma porta da API,
permitindo acesso via /streamlit em vez de uma porta separada.
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import requests
import os

router = APIRouter()

@router.get("/streamlit", response_class=HTMLResponse)
async def get_streamlit_dashboard():
    """
    Serve o dashboard Streamlit diretamente via iframe.
    
    Returns:
        HTMLResponse: Página HTML com iframe do Streamlit incorporado
    """
    
    # Verifica se o Streamlit está disponível
    # Agora no mesmo container, usa localhost
    streamlit_available = True
    try:
        response = requests.get("http://localhost:8501", timeout=3)
        streamlit_available = response.status_code == 200
    except Exception as e:
        streamlit_available = False
    
    # HTML com iframe incorporado do Streamlit
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>📚 Dashboard - BookFlow API</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #f8fafc;
                height: 100vh;
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1rem 1.5rem;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                position: relative;
                z-index: 1000;
            }}
            .header h1 {{
                margin: 0;
                font-size: 1.5rem;
                font-weight: 600;
            }}
            .header p {{
                margin: 0.25rem 0 0 0;
                opacity: 0.9;
                font-size: 0.9rem;
            }}
            .iframe-container {{
                width: 100%;
                height: calc(100vh - 80px);
                background: white;
                position: relative;
            }}
            iframe {{
                width: 100%;
                height: 100%;
                border: none;
                display: block;
            }}
            .loading {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
                font-size: 1.2rem;
                color: #666;
                flex-direction: column;
                background: white;
            }}
            .error {{
                background: #fef2f2;
                color: #991b1b;
                padding: 2rem;
                text-align: center;
                margin: 2rem;
                border-radius: 8px;
                border: 1px solid #fecaca;
            }}
            .spinner {{
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 20px auto;
            }}
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            .status-indicator {{
                position: absolute;
                top: 1rem;
                right: 1.5rem;
                background: {'rgba(34, 197, 94, 0.9)' if streamlit_available else 'rgba(239, 68, 68, 0.9)'};
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 12px;
                font-size: 0.75rem;
                font-weight: 500;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📚 Dashboard BookFlow</h1>
            <p>Painel de controle integrado</p>
            <div class="status-indicator">
                {'🟢 Online' if streamlit_available else '🔴 Carregando...'}
            </div>
        </div>
        
        <div class="iframe-container">
            {f'''
            <iframe 
                src="http://localhost:8501" 
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
                onload="this.style.opacity=1" 
                style="opacity:0;transition:opacity 0.5s"
            ></iframe>
            ''' if streamlit_available else '''
            <div class="loading">
                <div class="spinner"></div>
                <p><strong>Iniciando Dashboard...</strong></p>
                <p><small>Aguarde alguns segundos para o Streamlit carregar</small></p>
                <p><small><a href="javascript:window.location.reload()" style="color: #667eea;">🔄 Recarregar página</a></small></p>
            </div>
            '''}
        </div>
        
        <script>
            // Auto-reload se o dashboard não estiver disponível
            {f'console.log("Dashboard Streamlit carregado com sucesso");' if streamlit_available else '''
            console.log("Dashboard não disponível, recarregando em 10 segundos...");
            
            // Recarrega a página após 10 segundos se o Streamlit não estiver disponível
            setTimeout(function() {
                window.location.reload();
            }, 10000);
            '''}
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@router.get("/streamlit/external")
async def redirect_to_streamlit():
    """
    Redireciona para o Streamlit externo na porta 8501.
    
    Returns:
        RedirectResponse: Redirecionamento para o Streamlit
    """
    return RedirectResponse(url="http://localhost:8501")