# Entrevista Inteligente — Workflow Mobile-First

A **Entrevista Inteligente** é uma nova área do Agente Carreira 360 para construir o perfil profissional por meio de uma conversa guiada em formato de chatbot.

## Objetivo

Permitir que o usuário responda perguntas simples pelo celular, especialmente iPhone, e transforme experiências formais e informais em um resumo profissional, habilidades extraídas e um currículo inicial em Markdown.

## Como executar localmente

Na raiz do projeto, execute:

```bash
python scripts/abrir_entrevista_inteligente.py
```

Depois acesse no navegador:

```text
http://127.0.0.1:8000
```

## Estrutura adicionada

```text
web/entrevista-inteligente/
├── index.html
├── styles.css
└── app.js

scripts/
└── abrir_entrevista_inteligente.py
```

## Funcionalidades implementadas

- Layout mobile-first e responsivo.
- Interface otimizada para iPhone.
- Chat central com perguntas guiadas.
- Registro das respostas do usuário.
- Extração automática de habilidades por palavras-chave.
- Reconhecimento de experiências formais e informais.
- Painel de resumo do perfil.
- Progresso de preenchimento.
- Botão para gerar currículo em Markdown.
- Botão para editar manualmente o resumo profissional.
- Persistência local no navegador usando `localStorage`.

## Experiências reconhecidas

O sistema considera experiências como:

- Trabalho registrado.
- Projetos pessoais.
- Igreja.
- Eventos.
- Voluntariado.
- Liderança informal.
- Atendimento ao público.
- Operação de som.
- Organização de equipes.
- Comunicação.
- Resolução de problemas.

## Observação técnica

Esta entrega não remove funcionalidades existentes do MVP em terminal. A área mobile foi adicionada como módulo separado em `web/entrevista-inteligente`, com um servidor local simples em Python para facilitar o uso durante o desenvolvimento.

## Próximos passos sugeridos

- Integrar as respostas da entrevista aos arquivos JSON da pasta `data/`.
- Permitir importar o currículo gerado para `outputs/` automaticamente.
- Criar modo multiusuário futuramente.
- Adicionar testes automatizados para a extração de habilidades.
- Evoluir para backend Flask, FastAPI ou Streamlit quando o projeto precisar de persistência real.
