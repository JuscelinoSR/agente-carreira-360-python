from utils import carregar_json, salvar_markdown, lista_markdown


def gerar_linkedin():
    perfil = carregar_json("perfil-profissional.json", {})
    competencias = carregar_json("competencias.json", [])
    projetos = carregar_json("projetos.json", [])

    nome = perfil.get("nome", "[PREENCHER]")
    titulo = perfil.get("titulo_profissional", "[PREENCHER]")
    resumo = perfil.get("resumo_profissional", "[PREENCHER]")
    posicionamento = perfil.get("posicionamento", "[PREENCHER]")

    linhas = [
        f"# LinkedIn — {nome}",
        "",
        "## Título sugerido",
        "",
        f"{titulo} | Análise de Dados | Indicadores | IA aplicada ao trabalho",
        "",
        "## Sobre",
        "",
        resumo,
        "",
        posicionamento,
        "",
        "Atualmente busco fortalecer minha presença profissional, ampliar conexões estratégicas e evoluir em áreas ligadas à gestão, dados, automação, inteligência artificial e trabalho remoto.",
        "",
        "## Competências principais",
        "",
        lista_markdown(competencias[:12]),
        "",
        "## Projetos em destaque",
        ""
    ]

    if projetos:
        for projeto in projetos:
            linhas.append(f"- **{projeto.get('nome', '[PREENCHER]')}**: {projeto.get('descricao', '[PREENCHER]')}")
    else:
        linhas.append("- [PREENCHER]")

    return "\n".join(linhas)


if __name__ == "__main__":
    conteudo = gerar_linkedin()
    caminho = salvar_markdown("linkedin-resumo-juscelino.md", conteudo)
    print(f"Resumo de LinkedIn gerado em: {caminho}")
