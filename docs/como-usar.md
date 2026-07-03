# Como usar o projeto em Python

## 1. Atualizar dados

Edite os arquivos da pasta `data/`.

Principais arquivos:

- `perfil-profissional.json`
- `experiencias.json`
- `formacao.json`
- `competencias.json`
- `cursos.json`
- `projetos.json`
- `vagas-alvo.json`

## 2. Executar o menu

```bash
python mvp/app.py
```

## 3. Ver resultados

Os arquivos gerados ficam em:

```text
outputs/
```

## 4. Analisar vaga

Cole a descrição da vaga no arquivo:

```text
jobs/vagas-analisadas/vaga-exemplo.txt
```

Depois execute:

```bash
python scripts/analisar_vaga.py
```
