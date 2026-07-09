from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx
import os

app = FastAPI()

# Mapa de tarefas — adicione novas aqui
TASKS = {
    "t01": {"nome": "Bom dia Camila ☀️",         "msg": "Rodar tarefa 01"},
    "t02": {"nome": "Avisos de Agenda ",         "msg": "Rodar tarefa 02"},
    "t03": {"nome": "Monitor NF-e ",             "msg": "Rodar tarefa 03"},
    "t04": {"nome": "Briefing Mercado ",         "msg": "Rodar tarefa 04"},
    "t05": {"nome": "Resumo Mensagens ",    "msg": "Rodar tarefa 05"},
    "t06": {"nome": "Lembrete Alongamento ",     "msg": "Rodar tarefa 06"},
    "t07": {"nome": "Reflexão Noturna ",         "msg": "Rodar tarefa 07"},
    "t08": {"nome": "Reset Alimentação ",        "msg": "Rodar tarefa 08"},
    "t09": {"nome": "Resumo Semanal ",           "msg": "Rodar tarefa 09"},
    "t10": {"nome": "Análise Mensal ",           "msg": "Rodar tarefa 10"},
    "t11": {"nome": "Status Agenda","msg": "Rodar tarefa 11"},
}

ZAPIER_WEBHOOK_URL = os.getenv("ZAPIER_WEBHOOK_URL", "https://hook.us2.make.com/ykgwvvfa4jvxqi6jftdjj5g3cgnw129p")

@app.get("/", response_class=HTMLResponse)
async def index():
    links = "".join([
        f'<li><a href="/{k}" style="color:#00d4ff">{v["nome"]}</a></li>'
        for k, v in TASKS.items()
    ])
    return HTMLResponse(f"""
    <html><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body{{font-family:sans-serif;background:#1a1a2e;color:white;padding:20px;}}
    ul{{line-height:2.5;}}</style>
    </head><body>
    <h2>🚀 Zapia Tasks</h2><ul>{links}</ul>
    </body></html>
    """)

@app.get("/{task_id}", response_class=HTMLResponse)
async def trigger_task(task_id: str):
    task = TASKS.get(task_id)
    if not task:
        return HTMLResponse("<h2>Tarefa não encontrada.</h2>", status_code=404)

    success = False
    if ZAPIER_WEBHOOK_URL:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(ZAPIER_WEBHOOK_URL, json={
                    "task_id": task_id,
                    "task_nome": task["nome"],
                    "mensagem": task["msg"]
                }, timeout=10)
                success = resp.status_code < 400
        except Exception:
            pass

    if success:
        return HTMLResponse(f"""
        <html><head><meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>body{{font-family:sans-serif;display:flex;align-items:center;justify-content:center;
        height:100vh;margin:0;background:#1a1a2e;color:white;text-align:center;}}</style>
        </head><body>
        <div><div style="font-size:60px">✅</div>
        <h2>{task['nome']}</h2>
        <p>Disparado com sucesso!<br>Verifique o WhatsApp.</p></div>
        </body></html>
        """)
    else:
        return HTMLResponse(f"""
        <html><head><meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>body{{font-family:sans-serif;display:flex;align-items:center;justify-content:center;
        height:100vh;margin:0;background:#1a1a2e;color:white;text-align:center;}}</style>
        </head><body>
        <div><div style="font-size:60px">⚠️</div>
        <h2>{task['nome']}</h2>
        <p>Webhook não configurado.<br>Configure ZAPIER_WEBHOOK_URL.</p></div>
        </body></html>
        """)
