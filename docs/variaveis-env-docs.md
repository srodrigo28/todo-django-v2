## Usandos variaveis de ambiente
> * Para usar um arquivo .env e carregar variáveis de ambiente 
> * Exemplo: (como senhas, chaves API, URL do Supabase etc.) 
> * Forma segura no Python, você precisa instalar uma biblioteca extra. 
> * A mais comum e recomendada é o python-dotenv.

##  Por quê?

## O Python padrão os.getenv()

mas não carrega automaticamente de um arquivo .env.
Hardcodar valores sensíveis no código (como você mostrou) é ruim prática de segurança — nunca faça isso, especialmente com chaves do Supabase!

## Exemplo
meu_projeto/
├── .env           (Arquivo de dados/configuração)
└── main.py        (Arquivo de lógica/código)

### .env - Este arquivo guarda seus segredos e configurações
EMAIL_DEFAULT=maria@gmail.com
PASSWORD=123123

### main.py
```
import os
from dotenv import load_dotenv

# O comando abaixo lê o arquivo .env e disponibiliza os dados para o sistema
load_dotenv()

def enviar_notificacao():
    # Buscando os dados do arquivo .env usando os.getenv
    email_destino = os.getenv("EMAIL_DEFAULT")
    sennha = os.getenv("PASSWORD")

    if email_destino:
        print(f"--- {nome_projeto} ---")
        print(f"Enviando alerta para: {email_destino}")
    else:
        print("Erro: EMAIL_DEFAULT não encontrado no arquivo .env")

if __name__ == "__main__":
    enviar_notificacao()
```
