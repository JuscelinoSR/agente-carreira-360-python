# Agente Carreira 360 — Python

MVP em Python para gestão de carreira, currículo, LinkedIn, conteúdo profissional e networking estratégico.

## Objetivo

Criar uma ferramenta simples em Python para ajudar Juscelino Silva Rodrigues a organizar informações profissionais reais e gerar:

- Currículo em Markdown
- Resumo para LinkedIn
- Posts para redes sociais
- Mensagens de networking
- Análise básica de vagas
- Palavras-chave para recrutadores

## Tecnologias

- Python 3
- JSON
- Markdown
- Execução via terminal
- Sem dependências externas na versão inicial

## Como executar

No terminal, dentro da pasta do projeto:

```bash
python mvp/app.py
```

Ou execute scripts individuais:

```bash
python scripts/gerar_curriculo.py
python scripts/gerar_linkedin.py
python scripts/gerar_posts.py
python scripts/gerar_networking.py
python scripts/analisar_vaga.py
```

## Estrutura

```text
agente-carreira-360-python/
├── AGENTS.md
├── README.md
├── PROJECT_BRIEF.md
├── TOKEN_SAVING_GUIDE.md
├── requirements.txt
├── data/
├── scripts/
├── mvp/
├── outputs/
├── jobs/
├── docs/
├── prompts/
├── templates/
├── tests/
└── roadmap/
```

## Fluxo principal

1. Atualize os arquivos JSON em `data/`.
2. Execute `python mvp/app.py`.
3. Escolha o que deseja gerar.
4. Os arquivos serão salvos em `outputs/`.

## Importante

O projeto não publica automaticamente em redes sociais. Ele apenas gera rascunhos para revisão humana.

## Privacidade e segurança

- Nunca salve senhas, tokens, documentos pessoais ou chaves de API no repositório.
- Use variáveis de ambiente e mantenha o arquivo `.env` somente na máquina local.
- Os diretórios `data/` e `outputs/` fazem parte do repositório público. Revise seu conteúdo antes de cada commit.
- Relate vulnerabilidades conforme as orientações de [SECURITY.md](SECURITY.md), sem abrir detalhes sensíveis em uma issue pública.

## Contribuição

Leia [CONTRIBUTING.md](CONTRIBUTING.md) e [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) antes de enviar alterações.

## Licença

Este repositório ainda não possui uma licença de código aberto. Até que uma licença seja escolhida, nenhum direito de reutilização é concedido automaticamente.

## Autor

Juscelino Silva Rodrigues
