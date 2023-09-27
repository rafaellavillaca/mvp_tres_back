from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, jsonify
from urllib.parse import unquote
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from model import Session, Monitor
from schemas.quote import QuoteSchema
from schemas.fun_fact import FunFactSchema
from logger import logger
from schemas import *
import requests
from flask_cors import CORS


info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)

CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
monitor_tag = Tag(name="Monitor", description="Adição, visualização e remoção de monitor à base")
quote_tag = Tag(name="Quote", description="API Quote")
fun_fact_tag = Tag(name="Fun_Fact", description="API Fun_Fact")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.put('/monitor', tags=[monitor_tag],
          responses={"200": MonitorViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_monitor(form: MonitorSchema):
    """Adiciona um novo Monitor à base de dados

    Retorna uma representação dos monitores.
    """

    monitor = Monitor(
        nome=form.nome,
        email=form.email,
        habilidade=form.habilidade,
        disponibilidade = form.disponibilidade)


    logger.debug(f"Adicionando Monitor com email: '{monitor.email}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando monitor
        session.add(monitor)
        # efetivando o camando de adição de novo Monitor na tabela
        session.commit()
        logger.debug(f"Adicionado monitor email: '{monitor.email}'")
        return apresenta_monitor(monitor), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Monitor com o mesmo email já salvo na base :/"
        logger.warning(f"Erro ao adicionar Monitor '{monitor.email}', {error_msg}")
        print(e)
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo Monitor :/"
        logger.warning(f"Erro ao adicionar monitor '{monitor.email}', {error_msg}")
        print(e)
        return {"message": error_msg}, 400

@app.get('/monitores', tags=[monitor_tag],
         responses={"200": ListagemMonitoresSchema, "404": ErrorSchema})
def get_monitores():
    """Lista todos os Monitores cadastrados

    Retorna uma representação da listagem de monitores.
    """
    logger.debug(f"Coletando monitores ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    monitores = session.query(Monitor).all()

    if not monitores:
        # se não há monitores cadastrados
        return {"monitores": []}, 200
    else:
        logger.debug(f"%d monitores encontrados" % len(monitores))
        # retorna a representação de monitor
        print(monitores)
        return apresenta_monitores(monitores), 200

@app.delete('/monitor', tags=[monitor_tag],
            responses={"200": MonitorDelSchema, "404": ErrorSchema})
def del_monitor(query: MonitorBuscaSchema):
    """Deleta um Monitor a partir do nome de monitor informado

    Retorna uma mensagem de confirmação da remoção.
    """
    monitor_email = unquote(unquote(query.email))
    print(monitor_email)
    logger.debug(f"Deletando dados sobre monitor #{monitor_email}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Monitor).filter(Monitor.email == monitor_email).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado monitor #{monitor_email}")
        return {"message": "monitor removido", "email": monitor_email}
    else:
        # se o monitor não foi encontrado
        error_msg = "Monitor não encontrado na base :/"
        logger.warning(f"Erro ao deletar monitor #'{monitor_email}', {error_msg}")
        return {"message": error_msg}, 404

@app.post('/quote',tags=[quote_tag],
          responses={"200": QuoteSchema,"404": ErrorSchema})
def post_quote():
    try:
        # API externa
        api_url = 'http://api.forismatic.com/api/1.0/'

        # determinando parametros da api externa
        params = {
            'method': 'getQuote',
            'lang': 'en',
            'format': 'json',
        }

        # fazendo o request usando metodo post
        response = requests.post(api_url, data=params)

        if response.status_code == 200:
            data = response.json()
            quote = data['quoteText']
            author = data['quoteAuthor']
            return jsonify({'quote': quote, 'author': author})
        else:
            return jsonify({'error': 'Failed to fetch data from Forismatic API'})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.get('/fun_fact',tags=[fun_fact_tag],
          responses={"200": FunFactSchema,"404": ErrorSchema})
def get_fun_fact():
    try:
        # API externa
        api_url = 'https://uselessfacts.jsph.pl/api/v2/facts/random?language=en'


        # fazendo o request usando metodo get
        response = requests.get(api_url)

        if response.status_code == 200:
            
            data = response.json()
            print(response.text)
            funfact = data['text']
            # print(data)
            return jsonify({'text': funfact})
        else:
            return jsonify({'error': 'Failed to fetch data API'})

    except Exception as e:
        return jsonify({'error': str(e)})



