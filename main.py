from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
import os

app = FastAPI()

# Mapa de tarefas — adicione novas aqui
TASKS = {
    "t01": {"nome": "Bom dia Camila ☀️",          "msg": "Rodar tarefa 01"},
    "t02": {"nome": "Avisos de Agenda 📅",          "msg": "Rodar tarefa 02"},
    "t03": {"nome": "Monitor NF-e 📦",              "msg": "Rodar tarefa 03"},
    "t04": {"nome": "Briefing Mercado 📊",          "msg": "Rodar tarefa 04"},
    "t05": {"nome": "Resumo Mensagens Loja 📱",     "msg": "Rodar tarefa 05"},
    "t06": {"nome": "Lembrete Alongamento 🧘",      "msg": "Rodar tarefa 06"},
    "t07": {"nome": "Reflexão Noturna 🌙",          "msg": "Rodar tarefa 07"},
    "t08": {"nome": "Reset Alimentação 🥤",         "msg": "Rodar tarefa 08"},
    "t09": {"nome": "Resumo Semanal 📝",            "msg": "Rodar tarefa 09"},
    "t10": {"nome": "Análise Mensal 📆",            "msg": "Rodar tarefa 10"},
    "t11": {"nome": "Agenda + Status + Limpeza 📋", "msg": "Rodar tarefa 11"},
}

# URLs dos relatórios via Google Apps Script
GAS_AGENDA = "https://script.google.com/macros/s/AKfycbz7UriJN2UP4dlz0UdcVc2mAZPdMuYWBDAccH01a4ZL-3VHiJuByT05ZbAooB2VJSre/exec"
GAS_NFE    = ""  # será preenchido após publicar o script NF-e

# Seu número do WhatsApp (sem + e sem @)
WHATSAPP_NUMBER = "5551981599250"

@app.get("/", response_class=HTMLResponse)
async def index():
    links = "".join([
        f'<li><a href="/{k}" style="color:#00d4ff;font-size:18px">{v["nome"]}</a></li>'
        for k, v in TASKS.items()
    ])
    relatorios = f"""
    <h3 style="color:#aaa;margin-top:32px;margin-bottom:12px;font-size:14px;text-transform:uppercase;letter-spacing:1px">📊 Relatórios</h3>
    <div style="display:flex;flex-direction:column;gap:12px">
      <a href="/agenda" style="display:block;padding:14px 18px;background:#111827;border-radius:10px;border-left:4px solid #00d4ff;color:#00d4ff;font-size:16px;text-decoration:none">📅 Agenda da Semana</a>
      <a href="/nfe" style="display:block;padding:14px 18px;background:#111827;border-radius:10px;border-left:4px solid #10b981;color:#10b981;font-size:16px;text-decoration:none">📦 Resumo NF-e</a>
    </div>
    """
    return HTMLResponse(f"""
    <html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body{{font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#0d1117;color:white;padding:20px;max-width:500px;margin:0 auto;}}
      h2{{color:#00d4ff;margin-bottom:4px;}}
      .sub{{color:#666;font-size:12px;margin-bottom:24px;}}
      ul{{line-height:3;padding:0;list-style:none;}}
      ul li a{{display:block;padding:10px 14px;background:#111827;border-radius:8px;text-decoration:none;margin-bottom:6px;}}
      ul li a:hover{{background:#1f2937;}}
    </style>
    </head><body>
    <h2>🚀 Zapia Tasks</h2>
    <div class="sub">MG Ribeiro</div>
    {relatorios}
    <h3 style="color:#aaa;margin-top:32px;margin-bottom:12px;font-size:14px;text-transform:uppercase;letter-spacing:1px">⚡ Tarefas</h3>
    <ul>{links}</ul>
    </body></html>
    """)

@app.get("/agenda", response_class=HTMLResponse)
async def relatorio_agenda():
    return HTMLResponse(f"""
    <html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      *{{margin:0;padding:0;box-sizing:border-box;}}
      body{{background:#0d1117;font-family:-apple-system,BlinkMacSystemFont,sans-serif;}}
      .header{{background:#111827;padding:12px 16px;display:flex;align-items:center;gap:12px;border-bottom:1px solid #1f2937;position:sticky;top:0;z-index:10;}}
      .back{{color:#00d4ff;text-decoration:none;font-size:14px;}}
      .title{{color:white;font-size:16px;font-weight:600;}}
      iframe{{width:100%;height:calc(100vh - 50px);border:none;}}
    </style>
    </head><body>
    <div class="header">
      <a href="/" class="back">← Voltar</a>
      <span class="title">📅 Agenda da Semana</span>
    </div>
    <iframe src="{GAS_AGENDA}" loading="lazy"></iframe>
    </body></html>
    """)

@app.get("/nfe", response_class=HTMLResponse)
async def relatorio_nfe():
    if not GAS_NFE:
        return HTMLResponse("""
        <html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
        <style>body{{background:#0d1117;color:#aaa;font-family:sans-serif;padding:40px;text-align:center;}}</style>
        </head><body>
        <div style="font-size:48px;margin-bottom:16px">📦</div>
        <h2 style="color:white;margin-bottom:8px">Resumo NF-e</h2>
        <p>Script em configuração — em breve disponível.</p>
        <a href="/" style="color:#10b981;margin-top:24px;display:inline-block">← Voltar</a>
        </body></html>
        """)
    return HTMLResponse(f"""
    <html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      *{{margin:0;padding:0;box-sizing:border-box;}}
      body{{background:#0d1117;font-family:-apple-system,BlinkMacSystemFont,sans-serif;}}
      .header{{background:#111827;padding:12px 16px;display:flex;align-items:center;gap:12px;border-bottom:1px solid #1f2937;position:sticky;top:0;z-index:10;}}
      .back{{color:#10b981;text-decoration:none;font-size:14px;}}
      .title{{color:white;font-size:16px;font-weight:600;}}
      iframe{{width:100%;height:calc(100vh - 50px);border:none;}}
    </style>
    </head><body>
    <div class="header">
      <a href="/" class="back">← Voltar</a>
      <span class="title">📦 Resumo NF-e</span>
    </div>
    <iframe src="{GAS_NFE}" loading="lazy"></iframe>
    </body></html>
    """)

@app.get("/{task_id}")
async def trigger_task(task_id: str):
    task = TASKS.get(task_id)
    if not task:
        return HTMLResponse("<h2>Tarefa não encontrada.</h2>", status_code=404)

    import urllib.parse
    msg_encoded = urllib.parse.quote(task["msg"])
    whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={msg_encoded}"
    return RedirectResponse(url=whatsapp_url)
