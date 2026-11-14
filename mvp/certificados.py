"""Coleta de avisos de credencial e revisão editorial local."""

import argparse
import base64
from contextlib import closing
from datetime import datetime, timezone
from email.utils import parseaddr
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sqlite3
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

PASTA = Path(__file__).resolve().parents[1] / "outputs" / "private"
CONSULTA = '{subject:certificado subject:certificate subject:credencial}'


class TextoHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.partes = []
        self.ignorar = False

    def handle_starttag(self, tag, attrs):
        if tag in {"style", "script"}:
            self.ignorar = True

    def handle_endtag(self, tag):
        if tag in {"style", "script"}:
            self.ignorar = False

    def handle_data(self, data):
        if not self.ignorar:
            self.partes.append(data)


def texto_email(parte):
    for filho in parte.get("parts", []):
        yield from texto_email(filho)
    tipo = parte.get("mimeType")
    dados = parte.get("body", {}).get("data")
    if tipo not in {"text/html", "text/plain"} or not dados or parte.get("filename"):
        return
    texto = base64.urlsafe_b64decode(dados + "=" * (-len(dados) % 4)).decode(
        "utf-8", errors="replace"
    )
    if tipo == "text/html":
        leitor = TextoHTML()
        leitor.feed(texto)
        texto = " ".join(leitor.partes)
    yield " ".join(texto.split())


def classificar(remetente, assunto, texto):
    """Extrai apenas fatos de modelos reconhecidos. Os demais ficam pendentes."""
    remetente = parseaddr(remetente)[1].casefold()
    if remetente == "noreply@dio.me":
        padrao = (
            r"conquistar seu certificado em [oa] "
            r"(curso|projeto|módulo|mentoria|formação|bootcamp) "
            r"(.+?)\s*\.\s*Uma nova habilidade"
        )
        achado = re.search(padrao, texto, re.I)
        if achado:
            tipo, titulo = achado.groups()
            titulo = titulo.strip()
            if len(titulo) <= 240 and not re.search(r"https?://|[@<>]", titulo):
                return "emitido", "DIO", "DIO", tipo.lower(), titulo
        prefixo = "Certificado de conclusão - "
        if assunto.startswith(prefixo) and "parabéns por finalizar o curso" in texto.casefold():
            return "emitido", "DIO", "DIO", "curso", assunto[len(prefixo):].strip()
    if remetente.endswith("@t.learn.coursera.org"):
        nome = "Introduction to Generative AI"
        if nome in texto and "Google Cloud" in texto and re.search(
            r"concluiu o curso|completed the course", texto, re.I
        ) and re.search(r"emitir seu certificado|issue your certificate", texto, re.I):
            return "emitido", "Google Cloud", "Coursera", "curso", nome
    if remetente.endswith("@dio.me") and re.search(r"workshop|imersão", assunto + " " + texto, re.I):
        return "emissão a verificar", "", "", "", ""
    if re.search(r"inscreva-se|inscrições abertas|acesse grátis|oferta", assunto, re.I):
        return "oferta", "", "", "", ""
    return "a verificar", "", "", "", ""


def abrir_fila(pasta=PASTA):
    pasta.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(pasta / "certificados.sqlite3")
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript("""
        CREATE TABLE IF NOT EXISTS credenciais (
            id INTEGER PRIMARY KEY, chave TEXT NOT NULL UNIQUE,
            emissor TEXT NOT NULL, plataforma TEXT NOT NULL, tipo TEXT NOT NULL,
            titulo TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS avisos (
            id TEXT PRIMARY KEY, recebido TEXT NOT NULL, classificacao TEXT NOT NULL,
            credencial INTEGER REFERENCES credenciais(id)
        );
        CREATE TABLE IF NOT EXISTS rascunhos (
            id INTEGER PRIMARY KEY, credenciais TEXT NOT NULL,
            texto TEXT NOT NULL, estado TEXT NOT NULL DEFAULT 'em revisão'
        );
    """)
    return db


def registrar(db, mensagem):
    identificador = mensagem["id"]
    if db.execute("SELECT 1 FROM avisos WHERE id = ?", (identificador,)).fetchone():
        return
    parte = mensagem["payload"]
    cab = {h["name"].lower(): h["value"] for h in parte.get("headers", [])}
    recebido = datetime.fromtimestamp(int(mensagem["internalDate"]) / 1000, timezone.utc)
    estado, emissor, plataforma, tipo, titulo = classificar(
        cab.get("from", ""), cab.get("subject", ""), " ".join(texto_email(parte))
    )
    credencial = None
    with db:
        if estado == "emitido":
            # Sem ID público confirmado, consolida avisos do mesmo título e mês.
            try:
                data_local = recebido.astimezone(ZoneInfo("America/Sao_Paulo"))
            except ZoneInfoNotFoundError:
                data_local = recebido
            chave = unicodedata.normalize(
                "NFKC", "|".join((emissor, tipo, titulo, data_local.strftime("%Y-%m")))
            ).casefold()
            db.execute(
                "INSERT OR IGNORE INTO credenciais (chave, emissor, plataforma, tipo, titulo) "
                "VALUES (?, ?, ?, ?, ?)", (chave, emissor, plataforma, tipo, titulo)
            )
            credencial = db.execute(
                "SELECT id FROM credenciais WHERE chave = ?", (chave,)
            ).fetchone()["id"]
        db.execute(
            "INSERT OR IGNORE INTO avisos VALUES (?, ?, ?, ?)",
            (identificador, recebido.isoformat(), estado, credencial)
        )


def ler_json(url, dados=None, token=None):
    corpo = urlencode(dados).encode() if dados else None
    cab = {"Authorization": f"Bearer {token}"} if token else {}
    with urlopen(Request(url, data=corpo, headers=cab), timeout=30) as resposta:
        return json.load(resposta)


def sincronizar(db, dias):
    token = os.getenv("CARREIRA_GMAIL_ACCESS_TOKEN")
    if not token:
        nomes = ("CLIENT_ID", "CLIENT_SECRET", "REFRESH_TOKEN")
        creds = {nome.lower(): os.getenv("CARREIRA_GMAIL_" + nome) for nome in nomes}
        if not all(creds.values()):
            raise ValueError("Configure o OAuth Gmail de leitura conforme docs/certificados.md.")
        token = ler_json(
            "https://oauth2.googleapis.com/token", dict(creds, grant_type="refresh_token")
        )["access_token"]
    endpoint = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
    params = {"q": f"newer_than:{dias}d {CONSULTA}", "maxResults": 100}
    while True:
        pagina = ler_json(endpoint + "?" + urlencode(params), token=token)
        for item in pagina.get("messages", []):
            uid = item["id"]
            if db.execute("SELECT 1 FROM avisos WHERE id = ?", (uid,)).fetchone():
                continue
            registrar(db, ler_json(f"{endpoint}/{quote(uid, safe='')}?format=full", token=token))
        proxima = pagina.get("nextPageToken")
        if not proxima:
            return
        params["pageToken"] = proxima


def listar(db):
    for linha in db.execute("SELECT * FROM credenciais ORDER BY id"):
        print(f"{linha['id']} · {linha['titulo']} · {linha['emissor']}")
    for linha in db.execute("SELECT * FROM rascunhos ORDER BY id"):
        print(f"Rascunho {linha['id']} · {linha['estado']}")
    for linha in db.execute("SELECT classificacao, COUNT(*) AS n FROM avisos GROUP BY 1"):
        print(f"{linha['classificacao']}: {linha['n']} aviso(s)")


def ficha(db, uid):
    item = db.execute("SELECT * FROM credenciais WHERE id = ?", (uid,)).fetchone()
    if not item:
        raise ValueError("Credencial não encontrada.")
    texto = (
        f"# {item['titulo']}\n\n"
        f"- Emissor: {item['emissor']}\n- Plataforma: {item['plataforma']}\n"
        f"- Tipo: {item['tipo']}\n- Data de emissão e URL pública: a confirmar\n"
    )
    caminho = PASTA / f"credencial-{uid}.md"
    caminho.write_text(texto, encoding="utf-8")
    print(caminho)
    for aviso in db.execute("SELECT id, recebido FROM avisos WHERE credencial = ?", (uid,)):
        print(f"{aviso['recebido']} · https://mail.google.com/mail/u/0/#all/{aviso['id']}")


def validar_texto(texto):
    if not texto.strip() or len(texto) > 3000:
        raise ValueError("Informe um texto de 1 a 3000 caracteres.")
    if re.search(r"https?://|www\.|@|\bBRK\b|\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", texto, re.I):
        raise ValueError("Retire links, e-mails, CPF e menções à BRK antes de continuar.")


def criar_rascunho(db, ids, nota):
    titulos = []
    for uid in sorted(set(ids)):
        linha = db.execute(
            "SELECT titulo, emissor FROM credenciais WHERE id = ?", (uid,)
        ).fetchone()
        if not linha:
            raise ValueError("Credencial não encontrada.")
        titulos.append(f"**{linha['titulo']}** ({linha['emissor']})")
    texto = f"Concluí {', '.join(titulos)}.\n\n{nota.strip()}"
    validar_texto(texto)
    chaves = json.dumps(sorted(set(ids)))
    with db:
        db.execute("BEGIN IMMEDIATE")
        existente = db.execute(
            "SELECT id FROM rascunhos WHERE credenciais = ? AND estado != 'descartado'",
            (chaves,)
        ).fetchone()
        if existente:
            return existente["id"]
        return db.execute(
            "INSERT INTO rascunhos (credenciais, texto) VALUES (?, ?)", (chaves, texto)
        ).lastrowid


def revisar(db, uid, acao, arquivo=None):
    with db:
        db.execute("BEGIN IMMEDIATE")
        item = db.execute("SELECT * FROM rascunhos WHERE id = ?", (uid,)).fetchone()
        if not item:
            raise ValueError("Rascunho não encontrado.")
        if acao == "ver":
            print(item["texto"])
            return
        transicoes = {
            "editar": ("em revisão", "em revisão"),
            "aprovar": ("em revisão", "aprovado"),
            "descartar": ("em revisão", "descartado"),
            "publicado": ("aprovado", "publicado"),
        }
        origem, destino = transicoes[acao]
        if item["estado"] != origem:
            raise ValueError(f"Ação indisponível no estado {item['estado']}.")
        texto = arquivo.read_text(encoding="utf-8") if acao == "editar" else item["texto"]
        if acao in {"editar", "aprovar"}:
            validar_texto(texto)
        if acao == "aprovar":
            (PASTA / f"post-{uid}.md").write_text(texto, encoding="utf-8")
        db.execute(
            "UPDATE rascunhos SET estado = ?, texto = ? WHERE id = ?",
            (destino, texto, uid)
        )
        print(destino)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    comandos = parser.add_subparsers(dest="comando", required=True)
    sync = comandos.add_parser("sincronizar")
    sync.add_argument("--dias", type=int, default=7)
    comandos.add_parser("listar")
    cred = comandos.add_parser("ficha")
    cred.add_argument("id", type=int)
    novo = comandos.add_parser("rascunho")
    novo.add_argument("ids", nargs="+", type=int)
    novo.add_argument("--nota", required=True, help="Aprendizado ou aplicação de uso público.")
    rev = comandos.add_parser("revisar")
    rev.add_argument("id", type=int)
    rev.add_argument("acao", choices=["ver", "editar", "aprovar", "descartar", "publicado"])
    rev.add_argument("--arquivo", type=Path)
    args = parser.parse_args()
    try:
        with closing(abrir_fila()) as db:
            if args.comando == "sincronizar":
                if args.dias < 1:
                    raise ValueError("--dias deve ser positivo.")
                sincronizar(db, args.dias)
                listar(db)
            elif args.comando == "listar":
                listar(db)
            elif args.comando == "ficha":
                ficha(db, args.id)
            elif args.comando == "rascunho":
                if not args.nota.strip():
                    raise ValueError("Informe um aprendizado ou aplicação para o post.")
                print(f"Rascunho {criar_rascunho(db, args.ids, args.nota)}")
            else:
                if args.acao == "editar" and not args.arquivo:
                    raise ValueError("Informe --arquivo para editar.")
                revisar(db, args.id, args.acao, args.arquivo)
    except HTTPError as erro:
        parser.exit(1, f"Falha no Gmail (HTTP {erro.code}). Verifique o OAuth e tente novamente.\n")
    except URLError:
        parser.exit(1, "Falha de conexão com o Gmail. Tente novamente.\n")
    except (ValueError, OSError, sqlite3.Error) as erro:
        parser.exit(1, f"{erro}\n")


if __name__ == "__main__":
    main()
