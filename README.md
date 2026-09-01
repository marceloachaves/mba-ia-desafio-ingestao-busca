# Desafio MBA Engenharia de Software com IA - Full Cycle

## Como executar o programa
###  Criar e ativar o ambiente virtual e instalar as dependências
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Subir o banco de dados
```
docker compose up -d
```

### Executar a ingestão do PDF
```
python src/ingest.py
```
### Executar o chat
```
python src/chat.py
```

---  

Obs: O chat pode ser terminado com um dos três comandos: **"sair", "exit", "quit"**
