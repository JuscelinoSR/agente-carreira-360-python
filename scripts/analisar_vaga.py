from pathlib import Path
from utils import carregar_json, salvar_markdown, JOBS_DIR, garantir_pasta


def analisar_texto_vaga(texto_vaga: str):
    competencias = carregar_json("competencias.json", [])
    vagas_alvo = carregar_json("vagas-alvo.json", [])

    texto_lower = texto_vaga.lower()
    palavras_encontradas = []

    for comp in competencias:
        if comp.lower() in texto_lower:
            palavras_encontradas.append(comp)

    for vaga in vagas_alvo:
        for palavra in vaga.get("palavras_chave", []):
            if palavra.lower() in texto_lower and palavra not in palavras_encontradas:
                palavras_encontradas.append(palavra)

    linhas = [
        "# Análise de Vaga",
        "",
        "## Palavras-chave encontradas",
        ""
    ]

    if palavras_encontradas:
        for palavra in palavras_encontradas:
            linhas.append(f"- {palavra}")
    else:
        linhas.append("- Nenhuma palavra-chave exata encontrada. Revisar manualmente.")

    linhas.extend([
        "",
        "## Pontos fortes possíveis",
        "",
        "- Experiência em gestão comercial, operação, atendimento e indicadores.",
        "- Vivência prática com análise, organização de processos e melhoria contínua.",
        "- Interesse em dados, IA, automação e trabalho remoto.",
        "",
        "## Lacunas para revisar",
        "",
        "- Verificar se a vaga exige ferramentas específicas.",
        "- Verificar se a vaga exige inglês, certificações ou experiência remota.",
        "- Adaptar currículo com palavras-chave reais da vaga.",
        "",
        "## Próxima ação",
        "",
        "Adaptar o currículo e criar uma mensagem de candidatura específica para esta vaga."
    ])

    return "\n".join(linhas)


def main():
    garantir_pasta(JOBS_DIR / "vagas-analisadas")
    caminho_vaga = JOBS_DIR / "vagas-analisadas" / "vaga-exemplo.txt"

    if not caminho_vaga.exists():
        caminho_vaga.write_text(
            "Cole aqui a descrição da vaga que deseja analisar.",
            encoding="utf-8"
        )
        print(f"Arquivo criado: {caminho_vaga}")
        print("Cole a descrição da vaga nesse arquivo e execute o script novamente.")
        return

    texto_vaga = caminho_vaga.read_text(encoding="utf-8")
    conteudo = analisar_texto_vaga(texto_vaga)
    caminho = salvar_markdown("analise-vaga.md", conteudo)
    print(f"Análise de vaga gerada em: {caminho}")


if __name__ == "__main__":
    main()
