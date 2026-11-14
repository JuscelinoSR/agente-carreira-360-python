# Piloto editorial de certificados

O comando roda com Python 3.10+ e biblioteca padrão. Ative a Gmail API no projeto Google Cloud e autorize a conta com o escopo `https://www.googleapis.com/auth/gmail.readonly`. Forneça um token de acesso em `CARREIRA_GMAIL_ACCESS_TOKEN` ou configure `CARREIRA_GMAIL_CLIENT_ID`, `CARREIRA_GMAIL_CLIENT_SECRET` e `CARREIRA_GMAIL_REFRESH_TOKEN` para renovação. Mantenha os valores fora dos arquivos versionados. O conector do ChatGPT é uma sessão independente.

```sh
python mvp/certificados.py sincronizar --dias 7
python mvp/certificados.py listar
python mvp/certificados.py ficha 1
python mvp/certificados.py rascunho 1 2 --nota "Quero testar formas de consolidar avisos repetidos em um fluxo de trabalho em Python."
python mvp/certificados.py revisar 1 ver
python mvp/certificados.py revisar 1 editar --arquivo meu-rascunho.md
python mvp/certificados.py revisar 1 aprovar
python mvp/certificados.py revisar 1 publicado
```

Use os IDs mostrados no terminal. A sincronização pode ser chamada pelo agendador do sistema a cada 15 minutos após configurar o OAuth. A fila local usa SQLite e gera fichas e posts aprovados em `outputs/private/`. A confirmação de recebimento do e-mail não preenche a data oficial de emissão. Verifique a credencial diretamente para completar a data e a URL pública.

A triagem inicial usa regras para os modelos reconhecidos de e-mails da DIO e para o certificado de IA generativa da Google Cloud pela Coursera. As demais mensagens ficam pendentes ou são classificadas como oferta. A data de recebimento e o ID do Gmail ficam na fila local para revisão. O corpo integral e os links da mensagem não são armazenados.

Cadastre nas notas somente aprendizados e exemplos de uso público. A verificação automática cobre padrões básicos de privacidade. Antes de aprovar, confira também nomes de clientes, endereços, números internos e outras informações cuja sensibilidade depende do contexto. Copie o Markdown aprovado e publique no LinkedIn por sua conta. O comando `publicado` só registra essa ação na fila.
