from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUTS_DIR = ROOT / "outputs"
JOBS_DIR = ROOT / "jobs"


def garantir_pasta(caminho: Path) -> None:
    caminho.mkdir(parents=True, exist_ok=True)


def carregar_json(nome_arquivo: str, padrao=None):
    caminho = DATA_DIR / nome_arquivo
    if padrao is None:
        padrao = []

    if not caminho.exists():
        return padrao

    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        print(f"Erro: o arquivo {caminho} não é um JSON válido.")
        return padrao


def salvar_json(nome_arquivo: str, dados) -> Path:
    garantir_pasta(DATA_DIR)
    caminho = DATA_DIR / nome_arquivo
    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")
    return caminho


def salvar_markdown(nome_arquivo: str, conteudo: str) -> Path:
    garantir_pasta(OUTPUTS_DIR)
    caminho = OUTPUTS_DIR / nome_arquivo
    caminho.write_text(conteudo.strip() + "\n", encoding="utf-8")
    return caminho


def lista_markdown(itens):
    if not itens:
        return "- [PREENCHER]"
    return "\n".join(f"- {item}" for item in itens)


def bloco_lista(titulo, itens):
    return f"## {titulo}\n\n{lista_markdown(itens)}\n"
