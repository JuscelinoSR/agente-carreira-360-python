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

## Autor

Juscelino Silva Rodrigues
