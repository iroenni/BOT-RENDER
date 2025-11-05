import asyncio
import time
import psutil
import platform
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message

# Configuración del bot
API_ID = 14681595
API_HASH = "a86730aab5c59953c424abb4396d32d5"
BOT_TOKEN = "7486499541:AAEouB0D_NwkrxC81L-7RE99jO9oTZCCcfo"

# Crear el cliente de Pyrogram
app = Client("system_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def get_system_info():
    """Obtiene información detallada del sistema"""
    try:
        # Información de la CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Información de la memoria
        memory = psutil.virtual_memory()
        memory_total = round(memory.total / (1024 ** 3), 2)  # GB
        memory_used = round(memory.used / (1024 ** 3), 2)    # GB
        memory_percent = memory.percent
        
        # Información del disco
        disk = psutil.disk_usage('/')
        disk_total = round(disk.total / (1024 ** 3), 2)      # GB
        disk_used = round(disk.used / (1024 ** 3), 2)        # GB
        disk_percent = disk.percent
        
        # Información del sistema operativo
        system_info = platform.system()
        system_version = platform.version()
        architecture = platform.architecture()[0]
        processor = platform.processor() or "No detectado"
        
        # Tiempo de actividad del sistema
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        # Formatear tiempo de actividad
        uptime_days = uptime.days
        uptime_hours = uptime.seconds // 3600
        uptime_minutes = (uptime.seconds % 3600) // 60
        
        info = f"""
🖥 **INFORMACIÓN DEL SISTEMA**

**💻 Sistema Operativo:**
• OS: {system_info} {architecture}
• Versión: {system_version}
• Procesador: {processor}

**⚡ CPU:**
• Uso: {cpu_percent}%
• Núcleos: {cpu_count}

**💾 Memoria RAM:**
• Total: {memory_total} GB
• Usado: {memory_used} GB
• Porcentaje: {memory_percent}%

**💽 Disco Duro:**
• Total: {disk_total} GB
• Usado: {disk_used} GB
• Porcentaje: {disk_percent}%

**⏰ Tiempo de Actividad:**
• {uptime_days} días, {uptime_hours} horas, {uptime_minutes} minutos

**🔄 Bot Activo desde:**
• {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return info
    except Exception as e:
        return f"❌ Error al obtener información del sistema: {str(e)}"

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Comando /start"""
    await message.reply_text(
        "🤖 **Bot de Monitoreo del Sistema**\n\n"
        "Comandos disponibles:\n"
        "• /info - Mostrar información del sistema\n"
        "• /ping - Probar latencia del bot\n"
        "• /status - Estado general del sistema"
    )

@app.on_message(filters.command("info"))
async def info_command(client: Client, message: Message):
    """Comando /info - Muestra información detallada del sistema"""
    try:
        # Enviar mensaje de "procesando"
        processing_msg = await message.reply_text("🔄 Obteniendo información del sistema...")
        
        # Obtener información del sistema
        system_info = get_system_info()
        
        # Editar el mensaje con la información
        await processing_msg.edit_text(system_info)
        
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("ping"))
async def ping_command(client: Client, message: Message):
    """Comando /ping - Mide la latencia del bot"""
    try:
        start_time = time.time()
        
        # Enviar mensaje inicial
        ping_msg = await message.reply_text("🏓 Pong!")
        
        end_time = time.time()
        ping_time = round((end_time - start_time) * 1000, 2)
        
        # Editar mensaje con el ping
        await ping_msg.edit_text(f"🏓 **Pong!**\n\n⏱ **Latencia:** {ping_time} ms\n⚡ **Bot activo**")
        
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("status"))
async def status_command(client: Client, message: Message):
    """Comando /status - Estado rápido del sistema"""
    try:
        # Información rápida
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        status_text = f"""
📊 **ESTADO DEL SISTEMA**

🟢 **CPU:** {cpu_percent}%
🟢 **RAM:** {memory.percent}%
🟢 **Disco:** {disk.percent}%

🤖 **Bot:** 🟢 Conectado
⏰ **Hora:** {datetime.now().strftime('%H:%M:%S')}

Usa /info para información detallada
"""
        await message.reply_text(status_text)
        
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

async def main():
    """Función principal para ejecutar el bot"""
    print("🤖 Iniciando bot de monitoreo del sistema...")
    await app.start()
    print("✅ Bot iniciado correctamente!")
    
    # Mantener el bot corriendo
    await asyncio.Event().wait()

if __name__ == "__main__":
    # Ejecutar el bot
    asyncio.run(main())