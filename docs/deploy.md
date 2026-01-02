# Deploy Render

1️⃣ Subir tudo para o Git

Código Django (manage.py, app, templates, static etc.)

Banco db.sqlite3 (já que você quer persistir dados)

⚠️ Normalmente não é recomendado versionar o banco, mas para portfólio/teste rápido isso funciona.

2️⃣ Criar serviço Django no Render

No painel do Render:

New → Web Service

Conectar ao GitHub (seu repositório)

Runtime: Python 3.x (mesma versão que você usou)

Build Command:

pip install -r requirements.txt


Start Command:

gunicorn nome_do_projeto.wsgi:application


Substitua nome_do_projeto pelo nome da sua pasta do Django que contém wsgi.py.

3️⃣ Certifique-se que o banco está incluído

SQLite vai ficar no mesmo diretório que o projeto.

No Django settings.py você já deve ter:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

4️⃣ Static files

Para o Tailwind (ou CSS/JS custom) funcionar no Render:

python manage.py collectstatic


No Render, configure o diretório static para servir esses arquivos.

5️⃣ Limitação

Render reinicia o contêiner: se você não usar Persistent Disk, o banco pode ser apagado se reiniciar o serviço.

Para portfólio/teste isso normalmente não é um problema.

✅ Resumo:
Sim, se o db.sqlite3 está no Git e você configurar o Render corretamente, basta rodar e ele funciona.
O único “risco” é que se o contêiner reiniciar, você pode perder os dados se não usar armazenamento persistente.