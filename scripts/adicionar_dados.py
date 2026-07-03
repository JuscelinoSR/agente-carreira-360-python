import sys

from utils import carregar_json, salvar_json


PREENCHER = "[PREENCHER]"


def perguntar(rotulo: str) -> str:
    return input(f"{rotulo}: ").strip() or PREENCHER


def perguntar_lista(rotulo: str) -> list[str]:
    resposta = input(f"{rotulo} (separe por ponto e vírgula): ").strip()
    if not resposta:
        return [PREENCHER]
    return [item.strip() for item in resposta.split(";") if item.strip()]


def perguntar_booleano(rotulo: str):
    resposta = input(f"{rotulo} (s/n): ").strip().lower()
    if resposta == "s":
        return True
    if resposta == "n":
        return False
    return PREENCHER


def adicionar_em_lista(nome_arquivo: str, item) -> None:
    dados = carregar_json(nome_arquivo, [])
    if not isinstance(dados, list):
        print(f"Erro: {nome_arquivo} não contém uma lista válida.")
        return
    dados.append(item)
    caminho = salvar_json(nome_arquivo, dados)
    print(f"Dados salvos em: {caminho}")


def adicionar_curso() -> None:
    adicionar_em_lista(
        "cursos.json",
        {
            "nome": perguntar("Nome do curso"),
            "instituicao": perguntar("Instituição"),
            "status": perguntar("Status"),
            "observacao": perguntar("Observação"),
        },
    )


def adicionar_formacao() -> None:
    adicionar_em_lista(
        "formacao.json",
        {
            "curso": perguntar("Curso"),
            "instituicao": perguntar("Instituição"),
            "status": perguntar("Status"),
            "inicio": perguntar("Ano de início"),
        },
    )


def adicionar_conquista() -> None:
    adicionar_em_lista(
        "conquistas.json",
        {
            "titulo": perguntar("Título"),
            "descricao": perguntar("Descrição"),
            "status": perguntar("Status"),
            "pode_usar_em_curriculo": perguntar_booleano("Pode usar no currículo?"),
            "pode_usar_em_redes_sociais": perguntar_booleano(
                "Pode usar nas redes sociais?"
            ),
        },
    )


def adicionar_experiencia() -> None:
    adicionar_em_lista(
        "experiencias.json",
        {
            "cargo": perguntar("Cargo"),
            "empresa": perguntar("Empresa"),
            "periodo": perguntar("Período"),
            "descricao": perguntar_lista("Atividades"),
        },
    )


def adicionar_competencia() -> None:
    adicionar_em_lista("competencias.json", perguntar("Competência"))


ACOES = {
    "curso": adicionar_curso,
    "formacao": adicionar_formacao,
    "conquista": adicionar_conquista,
    "experiencia": adicionar_experiencia,
    "competencia": adicionar_competencia,
}


def main() -> None:
    tipo = sys.argv[1] if len(sys.argv) > 1 else ""
    acao = ACOES.get(tipo)
    if acao is None:
        print("Tipo inválido. Use: curso, formacao, conquista, experiencia ou competencia.")
        return
    acao()


if __name__ == "__main__":
    main()
