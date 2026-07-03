from utils import carregar_json, salvar_markdown


def gerar_networking():
    vagas = carregar_json("vagas-alvo.json", [])
    perfil = carregar_json("perfil-profissional.json", {})

    nome = perfil.get("nome", "Juscelino")
    linhas = ["# Mensagens de Networking", ""]

    linhas.append("## Mensagem geral para recrutadores")
    linhas.append("")
    linhas.append(
        "Olá, tudo bem? Vi seu perfil e achei interessante sua atuação na área de recrutamento e carreira. "
        "Estou em uma fase de evolução profissional, conectando minha experiência em gestão comercial, operação, indicadores e atendimento com dados, tecnologia e IA aplicada ao trabalho. "
        "Gostaria de me conectar para acompanhar seus conteúdos e trocar aprendizados."
    )
    linhas.append("")

    if vagas:
        linhas.append("## Mensagens por área de interesse")
        linhas.append("")
        for vaga in vagas:
            titulo = vaga.get("titulo", "[PREENCHER]")
            area = vaga.get("area", "[PREENCHER]")
            linhas.append(f"### {titulo}")
            linhas.append("")
            linhas.append(
                f"Olá, tudo bem? Tenho acompanhado conteúdos e oportunidades na área de {area}. "
                "Minha experiência envolve gestão comercial, operação, atendimento, indicadores e melhoria contínua, e estou buscando evoluir profissionalmente nessa direção. "
                "Gostaria de me conectar para acompanhar sua atuação e trocar aprendizados."
            )
            linhas.append("")

    return "\n".join(linhas)


if __name__ == "__main__":
    conteudo = gerar_networking()
    caminho = salvar_markdown("mensagens-networking.md", conteudo)
    print(f"Mensagens de networking geradas em: {caminho}")
