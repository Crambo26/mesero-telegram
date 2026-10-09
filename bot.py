
import os
import re
import logging
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Las imágenes se configurarán después.
# Por ahora el bot confirma que reconoce las bebidas.
BEBIDAS = {
    "refresco": ["refresco", "refrescos", "gaseosa", "gaseosas"],
    "cafe": ["café", "cafe", "cafecito"],
}

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    mensaje = update.message.text.lower()
    mensaje = mensaje.replace("á", "a")

    for bebida, palabras in BEBIDAS.items():
        patron = r"\b(" + "|".join(map(re.escape, palabras)) + r")\b"
        patron = patron.replace("á", "a")

        if re.search(patron, mensaje):
            await update.message.reply_text(
                f"¡Marchando un {bebida}! ☕🥤 "
                "Pronto te serviré con una imagen."
            )
            return

async def iniciar():
    token = os.environ["TELEGRAM_TOKEN"]
    app = Application.builder().token(token).build()
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, responder)
    )
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    logging.info("Mesero virtual iniciado.")
    await __import__("asyncio").Event().wait()

if __name__ == "__main__":
    import asyncio
    asyncio.run(iniciar())
