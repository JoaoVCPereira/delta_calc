import json
import logging
from datetime import datetime

import requests
from config.environment import PostgresDB as db
from database.connection_factory import Connection
from database.dao.boletas import BoletasDAO
from database.dao.opcoes import OpcoesDAO
from database.models.boletas import Boletas as BoletasModel
from database.models.opcoes import Opcoes as OpcoesModel
from models.response import Response
from schemas.boletas import BoletasDB as BoletasSchema
from schemas.opcoes import OpcoesDB as OpcoesSchema


class Helper:
    def __init__(self,service,logger:logging.Logger):
        self.service=service
        self.logger = logger

        self.table_opcoes = "opcoes"
        self.table_boletas = "boletas"

    def _get_selic(self):
        selic = "0"
        resp = json.loads(requests.get(self.service.selic_url).content)
        for data in resp:
            if data.get('nome')==self.service.selic_tag:
                selic = str(data.get('valor'))
        return selic

    def _save_opcao(self,data_opcao:dict)->Response:
        response_db = Response()
        self.logger.info(json.dumps(data_opcao,indent=2,ensure_ascii=False))
        if not isinstance(data_opcao.get("executionDate"),datetime):
            execution_date=datetime.strptime(data_opcao.get("executionDate"),"%d/%m/%Y")
            data_opcao["executionDate"]=execution_date
        opcao_schema = OpcoesSchema(
            ticket=data_opcao.get("ticket"),
            stock_price=data_opcao.get("stockPrice"),
            strike_price=data_opcao.get("strikePrice"),
            opcao_price=data_opcao.get("opcaoPrice"),
            selic=data_opcao.get("selic"),
            operation_type=data_opcao.get("operationType"),
            execution_date=data_opcao.get("executionDate"),
            implicit_vol=data_opcao.get("implicitVol"),
            delta=data_opcao.get("delta")
        )
        with Connection(db,self.table_opcoes) as conn:
            with conn.open_session() as session:
                opcoes_dao:OpcoesDAO = OpcoesDAO(self.logger,self.service.name,session)                
                response_db,data = opcoes_dao.create(data_db=opcao_schema)
                self.logger.info(f"[{self.service.name}]Response DB: {response_db.message} | Data: {data.opcao_id}")
        return response_db

    def get_last_5_opcoes(self):
        with Connection(db,self.table_opcoes) as conn:
            with conn.open_session() as session:
                opcoes_dao:OpcoesDAO = OpcoesDAO(self.logger,self.service.name,session)                
                data = opcoes_dao.get_last_5_opcoes()
                self.logger.info(f"[{self.service.name}]Data: {data.opcao_id}")
        return data