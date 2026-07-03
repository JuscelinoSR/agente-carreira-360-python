from utils import carregar_json, salvar_markdown, lista_markdown


def gerar_curriculo():
    perfil = carregar_json("perfil-profissional.json", {})
    experiencias = carregar_json("experiencias.json", [])
    formacao = carregar_json("formacao.json", [])
    cursos = carregar_json("cursos.json", [])
    competencias = carregar_json("competencias.json", [])
    projetos = carregar_json("projetos.json", [])

    nome = perfil.get("nome", "[PREENCHER]")
    titulo = perfil.get("titulo_profissional", "[PREENCHER]")
    resumo = perfil.get("resumo_profissional", "[PREENCHER]")
    localizacao = perfil.get("localizacao", "[PREENCHER]")
    email = perfil.get("email") or "[PREENCHER]"
    linkedin = perfil.get("linkedin") or "[PREENCHER]"
    github = perfil.get("github") or "[PREENCHER]"

    linhas = [
        f"# {nome}",
        "",
        f"**{titulo}**",
        "",
        f"Localização: {localizacao}",
        f"E-mail: {email}",
        f"LinkedIn: {linkedin}",
        f"GitHub: {github}",
        "",
        "## Resumo profissional",
        "",
        resumo,
        "",
        "## Experiência profissional",
        ""
    ]

    if experiencias:
        for exp in experiencias:
            linhas.append(f"### {exp.get('cargo', '[PREENCHER]')} — {exp.get('empresa', '[PREENCHER]')}")
            linhas.append(f"**Período:** {exp.get('periodo', '[PREENCHER]')}")
            linhas.append("")
            linhas.append(lista_markdown(exp.get("descricao", [])))
            linhas.append("")
    else:
        linhas.append("[PREENCHER]")
        linhas.append("")

    linhas.extend(["## Formação", ""])
    if formacao:
        for item in formacao:
            linhas.append(f"- {item.get('curso', '[PREENCHER]')} — {item.get('instituicao', '[PREENCHER]')} ({item.get('status', '[PREENCHER]')})")
    else:
        linhas.append("- [PREENCHER]")

    linhas.extend(["", "## Cursos e certificações", ""])
    if cursos:
        for curso in cursos:
            linhas.append(f"- {curso.get('nome', '[PREENCHER]')} — {curso.get('instituicao', '[PREENCHER]')} ({curso.get('status', '[PREENCHER]')})")
    else:
        linhas.append("- [PREENCHER]")

    linhas.extend(["", "## Competências", "", lista_markdown(competencias), ""])

    linhas.extend(["## Projetos", ""])
    if projetos:
        for projeto in projetos:
            linhas.append(f"### {projeto.get('nome', '[PREENCHER]')}")
            linhas.append(projeto.get("descricao", "[PREENCHER]"))
            tecnologias = projeto.get("tecnologias", [])
            if tecnologias:
                linhas.append(f"**Tecnologias:** {', '.join(tecnologias)}")
            linhas.append(f"**Status:** {projeto.get('status', '[PREENCHER]')}")
            linhas.append("")
    else:
        linhas.append("[PREENCHER]")

    return "\n".join(linhas)


if __name__ == "__main__":
    conteudo = gerar_curriculo()
    caminho = salvar_markdown("curriculo-juscelino.md", conteudo)
    print(f"Currículo gerado em: {caminho}")
