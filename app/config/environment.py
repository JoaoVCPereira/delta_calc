import os
from dotenv import load_dotenv
load_dotenv()

class Logging:
    logging_level_full = os.environ["LEVEL_FULL"]
    logging_path_full = os.environ["PATH_FULL"]

class DeltaCalc:
    name = os.environ["DELTA_CALC_NAME"]
    bg_color = "#D6A3FF"
    bg_field_color = "#E8CFFF"
    text_color = "#000000"
    button_color = "#9D4EDD"
    border_color = "#8E24AA"
    selic_url = "https://brasilapi.com.br/api/taxas/v1/"
    selic_tag = "Selic"


class PostgresDB:
    db_dialect: str = os.environ["DB_DIALECT"]
    db_host:str = os.environ["DB_HOST"]
    db_port:str = os.environ["DB_PORT"]
    db_username:str = os.environ["DB_USERNAME"]
    db_password:str = os.environ["DB_PASSWORD"]
    db_database:str = os.environ["DB_DATABASE"]

SERVICES = [DeltaCalc.name]