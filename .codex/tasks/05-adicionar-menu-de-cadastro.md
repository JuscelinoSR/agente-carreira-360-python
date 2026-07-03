# Tarefa 05 — Adicionar menu de cadastro de dados

## Objetivo

Melhorar o MVP do Agente Carreira 360 criando funções no menu para adicionar novos dados sem editar JSON manualmente.

## Arquivos permitidos

- `mvp/app.py`
- `scripts/utils.py`
- `scripts/adicionar_dados.py`

## Funcionalidades desejadas

Criar opções no menu para:

1. Adicionar novo curso
2. Adicionar nova formação
3. Adicionar nova conquista
4. Adicionar nova experiência
5. Adicionar nova competência

## Regras

- Use Python puro.
- Não instale dependências.
- Não altere a estrutura do projeto.
- Não invente informações.
- Salve os dados nos arquivos JSON corretos dentro de `data/`.
- Mantenha o código simples e fácil de entender.
- Se faltar alguma informação, salve como `[PREENCHER]`.
- Não altere arquivos fora da lista permitida.

## Critério de pronto

A tarefa estará pronta quando:

- O menu principal mostrar as novas opções.
- O usuário conseguir adicionar curso, formação, conquista, experiência e competência pelo terminal.
- Os dados forem salvos corretamente nos arquivos JSON.
- O projeto continuar executando com:

```bash
python mvp/app.py
```

## Como validar

Depois de concluir, testar:

```bash
python mvp/app.py
```

E verificar se aparecem opções parecidas com:

```text
7. Adicionar novo curso
8. Adicionar nova formação
9. Adicionar nova conquista
10. Adicionar nova experiência
11. Adicionar nova competência
```
