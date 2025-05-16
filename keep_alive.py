import os
from flask import Flask
from threading import Thread
import logging

app = Flask('')
logger = logging.getLogger('discord')

@app.route('/')
def home():
    logger.info("External request received at / endpoint")
    return "Bot is alive!"

@app.route('/ping')
def ping():
    logger.info("External request received at /ping endpoint")
    return "pong"

@app.route('/status')
def status():
    logger.info("External request received at /status endpoint")
    return "OK - Bot is running"

@app.route('/health')
def health():
    logger.info("External request received at /health endpoint")
    # Monitoramento do bot
    return {"status": "ok", "message": "Bot is healthy"}

def run():
    # Use uma váriavel de ambiente no Render para habilitar uma porta, ou deixe algum número padrão: 10000, 3000, 400, etc
    port = int(os.environ.get('PORT', 10000))
    
    logger.info(f"Starting web server on port {port}")
    # Importante: Use 0.0.0.0 para vincular todas as interfaces
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
    return t
