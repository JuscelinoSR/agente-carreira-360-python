from utils import carregar_json, salvar_markdown


def criar_texto_post(tema, rede, objetivo):
    return f"""## {tema} — {rede}

**Objetivo:** {objetivo}

Estou em uma fase de evolução profissional, buscando transformar experiências reais em aprendizado, posicionamento e crescimento.

Tenho entendido que desenvolvimento profissional não acontece apenas com intenção, mas com prática, constância e organização.

Cada experiência pode gerar aprendizado. Cada aprendizado pode se transformar em oportunidade.

**Chamada para ação:** Como você tem organizado sua evolução profissional?
"""


def gerar_posts():
    temas = carregar_json("temas-conteudo.json", [])
    linhas = ["# Posts da Semana", ""]

    if not temas:
        linhas.append("[PREENCHER]")
        return "\n".join(linhas)

    for item in temas:
        dia = item.get("dia", "[PREENCHER]")
        tema = item.get("tema", "[PREENCHER]")
        rede = item.get("rede", "[PREENCHER]")
        objetivo = item.get("objetivo", "[PREENCHER]")

        linhas.append(f"# {dia}")
        linhas.append("")
        linhas.append(criar_texto_post(tema, rede, objetivo))
        linhas.append("")

    return "\n".join(linhas)


if __name__ == "__main__":
    conteudo = gerar_posts()
    caminho = salvar_markdown("posts-semana.md", conteudo)
    print(f"Posts gerados em: {caminho}")
