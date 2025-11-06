from pyrogram import Client, filters
from pyrogram.types import Message

# Configuración del bot
API_ID = 14681595
API_HASH = "a86730aab5c59953c424abb4396d32d5"
BOT_TOKEN = "7486499541:AAEouB0D_NwkrxC81L-7RE99jO9oTZCCcfo"

# Crear el cliente de Pyrogram
app = Client("simple_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("Stat"))
async def stat_command(client: Client, message: Message):
    """Comando Stat - Responde con un simple hola"""
    await message.reply_text("hola")

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Comando /start"""
    await message.reply_text(
        "🤖 **Bot Simple**\n\n"
        "Comandos disponibles:\n"
        "• /Stat - El bot dice hola\n"
        "• /start - Mostrar esta ayuda"
    )

async def main():
    """Función principal para ejecutar el bot"""
    print("🤖 Iniciando bot simple...")
    await app.start()
    print("✅ Bot iniciado correctamente!")
    
    # Mantener el bot corriendo
    await asyncio.Event().wait()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())