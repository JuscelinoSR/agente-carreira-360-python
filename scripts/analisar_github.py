import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from utils import salvar_markdown


USUARIO_PADRAO = "JuscelinoSR"
API_GITHUB = "https://api.github.com"


def consultar_api(caminho: str):
    requisicao = Request(
        f"{API_GITHUB}{caminho}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Agente-Carreira-360",
        },
    )
    with urlopen(requisicao, timeout=15) as resposta:
        return json.load(resposta)


def listar_linguagens(repositorios: list[dict]) -> list[str]:
    return sorted(
        {repositorio["language"] for repositorio in repositorios if repositorio["language"]}
    )


def criar_resumo(perfil: dict, repositorios: list[dict]) -> str:
    linguagens = listar_linguagens(repositorios)
    linhas_repositorios = []
    for repositorio in repositorios:
        descricao = repositorio["description"] or "[PREENCHER]"
        linguagem = repositorio["language"] or "[PREENCHER]"
        linhas_repositorios.append(
            f"- [{repositorio['name']}]({repositorio['html_url']}) — "
            f"{descricao} | Linguagem: {linguagem}"
        )

    nome = perfil["name"] or "[PREENCHER]"
    bio = perfil["bio"] or "[PREENCHER]"
    lista_linguagens = ", ".join(linguagens) if linguagens else "[PREENCHER]"
    lista_repositorios = "\n".join(linhas_repositorios) or "- [PREENCHER]"

    return f"""# Resumo público do GitHub

## Perfil

- Nome: {nome}
- Usuário: [{perfil['login']}]({perfil['html_url']})
- Bio: {bio}
- Repositórios públicos: {perfil['public_repos']}
- Seguidores: {perfil['followers']}

## Linguagens encontradas

{lista_linguagens}

## Repositórios públicos

{lista_repositorios}

> Dados públicos consultados pela API do GitHub. Revise antes de usar no currículo.
"""


def main() -> None:
    usuario = os.getenv("GITHUB_USUARIO", USUARIO_PADRAO).strip() or USUARIO_PADRAO
    try:
        perfil = consultar_api(f"/users/{usuario}")
        repositorios = consultar_api(
            f"/users/{usuario}/repos?sort=updated&direction=desc&per_page=100"
        )
    except HTTPError as erro:
        print(f"GitHub respondeu com erro HTTP {erro.code}.")
        return
    except URLError as erro:
        print(f"Não foi possível conectar ao GitHub: {erro.reason}")
        return

    caminho = salvar_markdown("github-resumo.md", criar_resumo(perfil, repositorios))
    print(f"Resumo do GitHub atualizado em: {caminho}")


if __name__ == "__main__":
    main()
