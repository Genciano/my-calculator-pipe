# Base da imagem Python 3.9
FROM python:3.9

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para o diretório de trabalho
COPY . .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 3000 conforme sua solicitação anterior
EXPOSE 3000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]