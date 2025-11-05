import asyncio
import time
import psutil
import platform
import logging
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
        cpu_freq = psutil.cpu_freq()
        cpu_freq_current = round(cpu_freq.current, 2) if cpu_freq else "N/A"
        
        # Información de la memoria
        memory = psutil.virtual_memory()
        memory_total = round(memory.total / (1024 ** 3), 2)
        memory_used = round(memory.used / (1024 ** 3), 2)
        memory_percent = memory.percent
        
        # Información del disco
        disk = psutil.disk_usage('/')
        disk_total = round(disk.total / (1024 ** 3), 2)
        disk_used = round(disk.used / (1024 ** 3), 2)
        disk_percent = disk.percent
        
        # Información del sistema operativo
        system_info = platform.system()
        system_version = platform.version()
        architecture = platform.architecture()[0]
        processor = platform.processor() or "No detectado"
        
        # Tiempo de actividad
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
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
• Frecuencia: {cpu_freq_current} MHz

**💾 Memoria RAM:**
• Total: {memory_total} GB
• Usado: {memory_used} GB
• Porcentaje: {memory_percent}%

**💽 Disco Duro:**
• Total: {disk_total} GB
• Usado: {disk_used} GB
• Porcentaje: {disk_percent}%

**⏰ Tiempo de Actividad:**
• {uptime_days}d {uptime_hours}h {uptime_minutes}m

**🔄 Bot Activo desde:**
• {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return info
    except Exception as e:
        logger.error(f"Error en get_system_info: {e}")
        return f"❌ Error al obtener información del sistema: {str(e)}"

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Comando /start"""
    try:
        await message.reply_text(
            "🤖 **Bot de Monitoreo del Sistema**\n\n"
            "Comandos disponibles:\n"
            "• /info - Mostrar información del sistema\n"
            "• /ping - Probar latencia del bot\n"
            "• /status - Estado general del sistema\n"
            "• /help - Mostrar esta ayuda"
        )
        logger.info(f"Comando start ejecutado por {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error en start_command: {e}")

@app.on_message(filters.command("info"))
async def info_command(client: Client, message: Message):
    """Comando /info - Muestra información detallada del sistema"""
    try:
        processing_msg = await message.reply_text("🔄 Obteniendo información del sistema...")
        system_info = get_system_info()
        await processing_msg.edit_text(system_info)
        logger.info(f"Comando info ejecutado por {message.from_user.id}")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
        logger.error(f"Error en info_command: {e}")

@app.on_message(filters.command("ping"))
async def ping_command(client: Client, message: Message):
    """Comando /ping - Mide la latencia del bot"""
    try:
        start_time = time.time()
        ping_msg = await message.reply_text("🏓 Pong!")
        end_time = time.time()
        ping_time = round((end_time - start_time) * 1000, 2)
        
        await ping_msg.edit_text(
            f"🏓 **Pong!**\n\n"
            f"⏱ **Latencia:** {ping_time} ms\n"
            f"⚡ **Bot activo**\n"
            f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        logger.info(f"Comando ping ejecutado - Latencia: {ping_time}ms")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
        logger.error(f"Error en ping_command: {e}")

@app.on_message(filters.command("status"))
async def status_command(client: Client, message: Message):
    """Comando /status - Estado rápido del sistema"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Emojis según el uso
        cpu_emoji = "🟢" if cpu_percent < 70 else "🟡" if cpu_percent < 90 else "🔴"
        ram_emoji = "🟢" if memory.percent < 70 else "🟡" if memory.percent < 90 else "🔴"
        disk_emoji = "🟢" if disk.percent < 70 else "🟡" if disk.percent < 90 else "🔴"
        
        status_text = f"""
📊 **ESTADO DEL SISTEMA**

{cpu_emoji} **CPU:** {cpu_percent}%
{ram_emoji} **RAM:** {memory.percent}%
{disk_emoji} **Disco:** {disk.percent}%

🤖 **Bot:** 🟢 Conectado
⏰ **Hora:** {datetime.now().strftime('%H:%M:%S')}

Usa /info para información detallada
"""
        await message.reply_text(status_text)
        logger.info(f"Comando status ejecutado por {message.from_user.id}")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
        logger.error(f"Error en status_command: {e}")

@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """Comando /help"""
    await start_command(client, message)

async def main():
    """Función principal para ejecutar el bot"""
    logger.info("🤖 Iniciando bot de monitoreo del sistema...")
    try:
        await app.start()
        logger.info("✅ Bot iniciado correctamente!")
        
        # Obtener información del bot
        me = await app.get_me()
        logger.info(f"🤖 Bot: @{me.username} (ID: {me.id})")
        
        # Mantener el bot corriendo
        await asyncio.Event().wait()
        
    except Exception as e:
        logger.error(f"❌ Error al iniciar el bot: {e}")
    finally:
        await app.stop()
        logger.info("🛑 Bot detenido")

if __name__ == "__main__":
    # Ejecutar el bot
    asyncio.run(main())