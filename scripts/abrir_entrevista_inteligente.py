from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import webbrowser

ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web" / "entrevista-inteligente"
HOST = "127.0.0.1"
PORT = 8000


def abrir_entrevista_inteligente() -> None:
    if not WEB_DIR.exists():
        print(f"Pasta da Entrevista Inteligente não encontrada: {WEB_DIR}")
        return

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    url = f"http://{HOST}:{PORT}"
    print("Entrevista Inteligente iniciada.")
    print(f"Acesse pelo navegador: {url}")
    print("Para encerrar, pressione Ctrl+C no terminal.")

    webbrowser.open(url)
    servidor = ThreadingHTTPServer((HOST, PORT), Handler)
    servidor.serve_forever()


if __name__ == "__main__":
    abrir_entrevista_inteligente()
