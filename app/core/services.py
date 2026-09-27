import gc
import logging
import flet as ft

from core.design_engine.design_engine import DesignEngine

class DeltaCalcService:
    def __init__(self, service):
        self.service = service
        self.logger = logging.getLogger(service.name)
    
    def run(self):
        try:
            self.logger.info(f'[{self.service.name}] Starting...')
            
            def main(page: ft.Page):
                app = DesignEngine(page, self.service, self.logger)
            
            ft.run(main)
            
            self.logger.info(f'[{self.service.name}] Finished...')
        except Exception as e:
            self.logger.error(f'[{self.service.name}] Error...\n{str(e)}')
        finally:
            gc.collect()