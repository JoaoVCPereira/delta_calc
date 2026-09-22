import gc
import logging
import tkinter as tk

from core.delta_calc.delta_calc import DeltaCalc

class DeltaCalcService:
    def __init__(self, service):
        self.service = service
        self.logger = logging.getLogger(service.name)
    
    def run(self):
        try:
            self.logger.info(f'[{self.service.name}] Starting...')
            root = tk.Tk()
            service = DeltaCalc(root,self.service,self.logger)
            root.mainloop()
            self.logger.info(f'[{self.service.name}] Finished...')
        except Exception as e:
            self.logger.error(f'[{self.service.name}] Error...\n{str(e)}')
        gc.collect()