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

Pré-requisito: Python 3 instalado, com o comando `python` disponível no terminal.

Clone o projeto e entre na pasta:

```bash
git clone https://github.com/JuscelinoSR/agente-carreira-360-python.git
cd agente-carreira-360-python
```

A versão inicial usa a biblioteca padrão do Python. No terminal, dentro da pasta do projeto:

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

## Exemplo de uso

Para gerar um currículo:

1. Revise os dados em `data/`, mantendo apenas informações profissionais reais.
2. Execute `python mvp/app.py`.
3. Escolha **1. Gerar currículo**.
4. Revise o arquivo Markdown gerado em `outputs/` antes de compartilhar.

O menu também permite cadastrar cursos, formação, conquistas, experiências e competências, além de atualizar um resumo local do GitHub.

## Como contribuir

Consulte [CONTRIBUTING.md](CONTRIBUTING.md). Priorize melhorias pequenas, Python puro e exemplos com dados fictícios.

## Importante

O projeto não publica automaticamente em redes sociais. Ele apenas gera rascunhos para revisão humana.

## Autor

Juscelino Silva Rodrigues
