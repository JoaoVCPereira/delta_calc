import os
from dotenv import load_dotenv
load_dotenv()

class Logging:
    logging_level_full = os.environ["LEVEL_FULL"]
    logging_path_full = os.environ["PATH_FULL"]

class DeltaCalc:
    name = os.environ["DELTA_CALC_NAME"]
    cron = os.environ["DELTA_CALC_CRON"]
    bg_color = "#00304D"
    text_color = "#FDFDFD"
    purple = "#5C38FF"
    cian = "#7A5DFF"
    border_color = "#464646"
    default_font = ("Segoe UI", 10)
    title_font = ("Segoe UI", 12, "bold")
    selic_url = "https://brasilapi.com.br/api/taxas/v1/"
    selic_tag = "Selic"

