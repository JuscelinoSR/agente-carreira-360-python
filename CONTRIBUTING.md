# Como contribuir

Obrigado pelo interesse em melhorar o Agente Carreira 360.

## Antes de começar

1. Leia `AGENTS.md` e o código de conduta.
2. Não inclua dados profissionais inventados, informações pessoais, senhas ou tokens.
3. Abra uma issue para mudanças grandes antes de implementá-las.

## Fluxo recomendado

1. Crie uma branch a partir de `main`.
2. Faça uma alteração pequena e focada.
3. Execute `python -m unittest discover -s tests -v`.
4. Confirme que `python mvp/app.py` continua funcionando.
5. Abra um Pull Request explicando o motivo, o impacto e a validação realizada.

## Padrão do projeto

- Use Python da biblioteca padrão sempre que possível.
- Prefira funções pequenas e nomes claros em português.
- Use `pathlib` para caminhos e UTF-8 para arquivos.
- Gere conteúdo somente a partir de informações confirmadas.
- Mantenha revisão humana antes de qualquer publicação externa.
