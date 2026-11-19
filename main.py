from flask import Flask, request
import requests
app = Flask(__name__)

# PEGA AQUI TU TOKEN Y TU CHAT ID
TELEGRAM_TOKEN = 9054460199:AAHeiTsgDdT3ODRVuCkZ3MGRaT3u-nF-dCk
TELEGRAM_CHAT_ID = 8852751671

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje})

@app.route("/", methods=["GET", "POST"])
def home():
    senal = ""
    if request.method == "POST":
        partido = request.form.get("partido")
        jugador = request.form.get("jugador")
        mercado = request.form.get("mercado")
        betano = float(request.form.get("betano"))
        bet365 = float(request.form.get("bet365"))
        valor = (betano / bet365 - 1) * 100
        minima = bet365 * 1.05
        if valor >= 150:
            nivel = "🚨 POSIBLE ERROR DE CUOTA EN BETANO - ENTRALE DE UNA, PUEDE BAJAR EN MINUTOS"
        elif valor >= 80:
            nivel = "🔥 SENAL ALTA - POSIBLE BAJADA, ENTRALE DE UNA"
        elif valor >= 30:
            nivel = "⚡ SENAL MEDIA"
        else:
            nivel = "❌ SIN VALOR"
        senal = f"{nivel}\n\n{partido}\nJugador: {jugador}\nMercado: {mercado}\n\nBetano: {betano}\nBet365: {bet365}\nValor: +{valor:.1f}%\n\nPrediccion de bajada: Va a bajar de {betano} hasta {bet365}\nCuota minima para entrar: {minima:.2f}\n\nAprovecha antes de que lo corrijan."
        if valor >= 30:
            enviar_telegram(senal)
    return f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body{{font-family:Arial;background:#0f172a;color:white;text-align:center;padding:20px}} .card{{background:white;color:#111;border-radius:16px;padding:20px;max-width:400px;margin:auto;text-align:left}} input,select{{width:100%;padding:12px;margin:8px 0;border-radius:10px;border:1px solid #ddd}} button{{width:100%;padding:14px;background:#22c55e;color:white;border:none;border-radius:10px;font-size:18px;font-weight:bold}} pre{{white-space:pre-wrap;background:#111;color:#fff;padding:15px;border-radius:12px}}</style></head>
    <body><h1>🔍 VALUE SCOUT</h1><p>Betano vs Bet365</p>
    <div class="card"><form method="POST">
    <input name="partido" placeholder="Partido: Real vs Barca" required>
    <input name="jugador" placeholder="Jugador: Courtois" required>
    <select name="mercado"><option>Remates totales</option><option>Remates al arco</option><option>Tackles</option><option>Faltas cometidas</option><option>Faltas recibidas</option><option>Atajadas</option></select>
    <input name="betano" type="number" step="0.01" placeholder="Cuota Betano ej: 15" required>
    <input name="bet365" type="number" step="0.01" placeholder="Cuota Bet365 ej: 5" required>
    <button>GENERAR SENAL + ENVIAR A TELEGRAM</button></form></div>
    <pre>{senal}</pre></body></html>
    """

if __name__ == "__main__":
    app.run()
