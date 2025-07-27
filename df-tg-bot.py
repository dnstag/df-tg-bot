from telegram.ext import ApplicationBuilder
from config import Config
from pota import POTA
from dlbota import DLBOTA

cfg = Config()

def main():
    app = ApplicationBuilder().token(cfg.token).build()
    pota = POTA(app)
    dlbota = DLBOTA(app)
    app.run_polling()

if __name__ == '__main__':
    main()