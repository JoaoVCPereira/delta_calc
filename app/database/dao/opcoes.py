import logging
from datetime import datetime

from database.models.opcoes import Opcoes as OpcoesModel
from schemas.opcoes import OpcoesDB as OpcoesDB
from models.response import Response
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import Session
from config.enums import DBOperationType

class OpcoesDAO:
    def __init__(self,logger: logging.Logger, service_name:str,db_session: Session):
        self.logger = logger
        self.db = db_session
        self.service_name = service_name
    
    def submit(self, data: OpcoesModel,operation_type:DBOperationType)-> tuple[Response,OpcoesModel]:
        response: Response = Response(status=False,error=False)
        try:
            if DBOperationType.CREATE == operation_type:
                self.db.add(data)
            elif DBOperationType.UPDATE == operation_type:
                data = self.db.merge(data)
            elif DBOperationType.DELETE == operation_type:
                self.db.delete(data)
            self.db.commit()
            if DBOperationType.CREATE == operation_type:
                message = f'Added: {data.ticket}'
            elif DBOperationType.UPDATE == operation_type:
                message = f'Updated: {data.ticket}'
            elif DBOperationType.DELETE == operation_type:
                message = f'Deleted: {data.ticket}'
            self.logger.info(f'[{self.service_name.upper()}][CREATE_CLIENT_DAO] {message}')
            response.status = True
        
        except Exception as e:
            self.db.rollback()
            self.logger.warning(f'[{self.service_name.upper()}][CREATE_CLIENT_DAO] Rolled back: {data.ticket} - Error: {str(e)}')
            
        return response, data
    
    def create(self, data_db: OpcoesDB) -> tuple[Response,OpcoesDB]:
        data:OpcoesModel = OpcoesModel().from_schema(data_db)
        operation_type = DBOperationType.CREATE
        response, data = self.submit(data,operation_type)
        insert_data: OpcoesDB = data.to_schema()
        return response, insert_data

    def update(self, data_db: OpcoesDB) -> tuple[Response, OpcoesDB]:
        data = OpcoesModel().from_schema(data_db)
        operation_type = DBOperationType.UPDATE
        data_to_update = self.db.query(OpcoesModel).filter(OpcoesModel.opcao_id == data.opcao_id).first()
        response,data = self.submit(data_to_update.from_schema(data_db),operation_type)
        insert_data: OpcoesDB = data.to_schema()
        return response,insert_data
    
    def delete(self,data_db:OpcoesDB) -> tuple[Response,OpcoesDB]:
        data = OpcoesModel().from_schema(data_db)
        operation_type = DBOperationType.DELETE
        data_to_delete = self.db.query(OpcoesModel).filter(OpcoesModel.documento == data.documento).first()
        response,data = self.submit(data_to_delete,operation_type)
        insert_data:OpcoesDB = data.to_schema()
        return response,insert_data

    def get_last_5_opcoes(self):
        data_query = self.db.query(OpcoesModel).all()[-5:]
        return data_query
