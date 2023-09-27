# Minha API  

Disciplina **Desenvolvimento Back End Avançado e Arquitetura de Software** 

## Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t meu-app-api .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -p 8000:8000 meu-app-api
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:8000/#/](http://localhost:8000/#/) no navegador.

