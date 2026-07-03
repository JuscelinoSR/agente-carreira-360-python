# AGENTS.md — Instruções para Codex

## Papel do Codex

Você é o agente de desenvolvimento deste projeto Python.

Sua missão é evoluir o projeto **Agente Carreira 360** como um MVP simples, ético e organizado para geração de currículo, LinkedIn, posts e networking.

## Regras obrigatórias

1. Use Python puro sempre que possível.
2. Não instale dependências sem autorização.
3. Não crie automações abusivas.
4. Não publique nada em redes sociais.
5. Não invente dados profissionais.
6. Não exponha informações confidenciais.
7. Trabalhe em tarefas pequenas.
8. Não altere arquivos fora do escopo solicitado.
9. Mantenha o código simples e legível.
10. Gere saídas em Markdown dentro de `outputs/`.

## Padrão de código

- Usar funções pequenas.
- Usar `pathlib`.
- Usar `json` da biblioteca padrão.
- Validar se arquivos existem antes de ler.
- Criar pastas de saída automaticamente.
- Evitar código complexo.
- Usar nomes em português para facilitar entendimento.

## Formato de resposta ao concluir tarefas

```text
Concluído.

Arquivos alterados:
- caminho/do/arquivo.py

Resumo:
- O que foi feito em até 3 linhas.

Validação:
- Comando para testar.
```

## Não fazer sem autorização

- Não criar API externa.
- Não integrar LinkedIn, Instagram, TikTok, YouTube ou Facebook.
- Não usar banco de dados externo.
- Não instalar bibliotecas.
- Não criar login.
- Não salvar dados sensíveis.
