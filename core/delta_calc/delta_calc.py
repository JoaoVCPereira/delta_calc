import logging
import tkinter as tk
import os
from tkinter import messagebox
import math
import ctypes
from datetime import date, timedelta
from tkcalendar import DateEntry
from utils import utils

class DeltaCalc:
    def __init__(self, master,service, logger:logging.Logger):
        self.master = master
        self.service = service
        self.logger = logger
        
        self._configurar_janela()
        self._construir_interface()

    def _configurar_janela(self):
        self.master.title("Delta")
        self.master.geometry("400x630")
        self.master.configure(bg=self.service.bg_color)
        self.master.resizable(False, False)
        try:
            meu_app_id = 'delta_calc.1_0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(meu_app_id)
        except Exception:
            pass
        try:
            raiz_projeto = utils.get_root_path()
            caminho_icone = os.path.join(raiz_projeto, 'models', 'delta_pro.ico')
            
            self.master.iconbitmap(os.path.abspath(caminho_icone))
        except Exception as e:
            self.logger.exception(f"Não foi possível carregar o ícone:")

    # --- MÉTODOS MATEMÁTICOS (Encapsulados) ---
    @staticmethod
    def _norm_cdf(x):
        return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

    @classmethod
    def _bs_price(cls, S, K, t, r, sigma, is_call):
        if sigma <= 0 or t <= 0:
            return max(0, S - K) if is_call else max(0, K - S)
            
        d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * t) / (sigma * math.sqrt(t))
        d2 = d1 - sigma * math.sqrt(t)
        
        if is_call:
            return S * cls._norm_cdf(d1) - K * math.exp(-r * t) * cls._norm_cdf(d2)
        else:
            return K * math.exp(-r * t) * cls._norm_cdf(-d2) - S * cls._norm_cdf(-d1)

    @classmethod
    def _encontrar_volatilidade_implicita(cls, preco_alvo, S, K, t, r, is_call):
        valor_intrinseco = max(0, S - K) if is_call else max(0, K - S)
        if preco_alvo < valor_intrinseco:
            raise ValueError("O preço de mercado informado é menor que o valor intrínseco da opção.")

        limite_inferior = 0.0001
        limite_superior = 5.0
        
        for _ in range(100):
            meio = (limite_inferior + limite_superior) / 2
            preco_calculado = cls._bs_price(S, K, t, r, meio, is_call)
            
            if preco_calculado > preco_alvo:
                limite_superior = meio
            else:
                limite_inferior = meio
                
            if (limite_superior - limite_inferior) < 1e-5:
                break
                
        return (limite_inferior + limite_superior) / 2

    @staticmethod
    def _calcular_dias_uteis(data_alvo):
        hoje = date.today()
        if data_alvo <= hoje:
            raise ValueError("A data de vencimento deve ser uma data no futuro.")
        
        dias_uteis = 0
        dia_atual = hoje
        while dia_atual < data_alvo:
            if dia_atual.weekday() < 5:
                dias_uteis += 1
            dia_atual += timedelta(days=1)
            
        return dias_uteis

    # --- MÉTODOS DA INTERFACE (Componentes) ---
    def _criar_linha_entrada(self, parent, texto, valor_padrao):
        frame = tk.Frame(parent, bg=self.service.bg_color)
        frame.pack(fill="x", pady=5)
        tk.Label(frame, text=texto, font=self.service.default_font, bg=self.service.bg_color, fg=self.service.text_color).pack(side="left")
        entry = tk.Entry(frame, font=self.service.default_font, width=12, relief="solid", bd=1, highlightbackground=self.service.border_color, highlightcolor=self.service.cian)
        entry.pack(side="right")
        entry.insert(0, valor_padrao)
        return entry

    def _criar_linha_resultado(self, parent, texto):
        frame = tk.Frame(parent, bg=self.service.bg_color)
        frame.pack(fill="x", pady=4)
        tk.Label(frame, text=texto, font=self.service.default_font, bg=self.service.bg_color, fg=self.service.text_color).pack(side="left")
        lbl_valor = tk.Label(frame, text="--", font=("Segoe UI", 11, "bold"), bg=self.service.bg_color)
        lbl_valor.pack(side="right")
        return lbl_valor

    def _construir_interface(self):
        self.main_frame = tk.Frame(self.master, bg=self.service.bg_color, padx=25, pady=25)
        self.main_frame.pack(fill="both", expand=True)

        # 1. Dados da Ação e Mercado
        tk.Label(self.main_frame, text="Dados da Ação e Mercado", font=self.service.title_font, bg=self.service.bg_color, fg=self.service.purple).pack(anchor="w", pady=(0, 15))

        self.entry_S = self._criar_linha_entrada(self.main_frame, "Preço Atual da Ação (R$):", "00.00")
        self.entry_K = self._criar_linha_entrada(self.main_frame, "Preço de Exercício / Strike (R$):", "00.00")

        # Calendário Interativo
        frame_cal = tk.Frame(self.main_frame, bg=self.service.bg_color)
        frame_cal.pack(fill="x", pady=5)
        tk.Label(frame_cal, text="Data de Vencimento:", font=self.service.default_font, bg=self.service.bg_color, fg=self.service.text_color).pack(side="left")

        self.cal_vencimento = DateEntry(
            frame_cal, width=10, background=self.service.purple, foreground='white', borderwidth=1,
            headersbackground=self.service.bg_color, headersforeground='white',
            selectbackground=self.service.cian, selectforeground='white',
            date_pattern='dd/MM/yyyy', font=self.service.default_font
        )
        self.cal_vencimento.pack(side="right")

        self.entry_r = self._criar_linha_entrada(self.main_frame, "Taxa de Juros Selic/DI (%):", "13.75")

        tk.Frame(self.main_frame, bg=self.service.border_color, height=1).pack(fill="x", pady=20)

        # 2. Dados da Opção
        tk.Label(self.main_frame, text="Dados da Opção (Sua Referência)", font=self.service.title_font, bg=self.service.bg_color, fg=self.service.purple).pack(anchor="w", pady=(0, 15))

        frame_tipo = tk.Frame(self.main_frame, bg=self.service.bg_color)
        frame_tipo.pack(fill="x", pady=5)
        tk.Label(frame_tipo, text="Tipo de Opção:", font=self.service.default_font, bg=self.service.bg_color, fg=self.service.text_color).pack(side="left")

        self.var_tipo = tk.StringVar(value="Call")
        tk.Radiobutton(frame_tipo, text="Call", variable=self.var_tipo, value="Call", font=self.service.default_font, bg=self.service.bg_color, activebackground=self.service.bg_color, selectcolor=self.service.bg_color, fg=self.service.text_color).pack(side="left", padx=(10, 0))
        tk.Radiobutton(frame_tipo, text="Put", variable=self.var_tipo, value="Put", font=self.service.default_font, bg=self.service.bg_color, activebackground=self.service.bg_color, selectcolor=self.service.bg_color, fg=self.service.text_color).pack(side="left")

        self.entry_preco_mercado = self._criar_linha_entrada(self.main_frame, "Preço da Opção no Mercado (R$):", "0.50")

        # Botão com Eventos
        self.btn_calcular = tk.Button(self.main_frame, text="Calcular Volatilidade e Delta", font=("Segoe UI", 11, "bold"), 
                                 bg=self.service.cian, fg="white", relief="flat", activebackground=self.service.purple, activeforeground="white", 
                                 cursor="hand2", command=self._calcular_tudo, pady=8)
        self.btn_calcular.pack(fill="x", pady=20)
        self.btn_calcular.bind("<Enter>", self._on_enter)
        self.btn_calcular.bind("<Leave>", self._on_leave)

        # 3. Resultados
        tk.Label(self.main_frame, text="Resultados Extraídos", font=self.service.title_font, bg=self.service.bg_color, fg=self.service.purple).pack(anchor="w", pady=(0, 5))

        self.lbl_info_dias = tk.Label(self.main_frame, text="", font=("Segoe UI", 8, "italic"), bg=self.service.bg_color, fg="#A0A0A0")
        self.lbl_info_dias.pack(anchor="w", pady=(0, 10))

        self.lbl_resultado_iv = self._criar_linha_resultado(self.main_frame, "Volatilidade Implícita:")
        self.lbl_resultado_call = self._criar_linha_resultado(self.main_frame, "Delta da Call:")
        self.lbl_resultado_put = self._criar_linha_resultado(self.main_frame, "Delta da Put:")

    # --- MÉTODOS DE AÇÃO ---
    def _on_enter(self, e):
        self.btn_calcular['background'] = self.service.purple

    def _on_leave(self, e):
        self.btn_calcular['background'] = self.service.cian

    def _calcular_tudo(self):
        try:
            S = float(self.entry_S.get().replace(',', '.'))
            K = float(self.entry_K.get().replace(',', '.'))
            r_percentual = float(self.entry_r.get().replace(',', '.'))
            preco_mercado = float(self.entry_preco_mercado.get().replace(',', '.'))
            
            data_vencimento = self.cal_vencimento.get_date()
            t_dias = self._calcular_dias_uteis(data_vencimento)
            is_call = (self.var_tipo.get() == "Call")

            if S <= 0 or K <= 0 or preco_mercado <= 0:
                messagebox.showwarning("Aviso", "Os preços e taxas devem ser maiores que zero.")
                return

            r = r_percentual / 100.0
            t = t_dias / 252.0

            # Cálculos instanciando os métodos da própria classe
            sigma = self._encontrar_volatilidade_implicita(preco_mercado, S, K, t, r, is_call)
            d1 = (math.log(S / K) + (r + (sigma ** 2) / 2) * t) / (sigma * math.sqrt(t))
            delta_call = self._norm_cdf(d1)
            delta_put = delta_call - 1

            # Atualização da Interface
            self.lbl_resultado_iv.config(text=f"{sigma * 100:.2f}%", fg=self.service.purple)
            self.lbl_resultado_call.config(text=f"{delta_call:.4f}  ({delta_call * 100:.2f}%)", fg="#00A859")
            self.lbl_resultado_put.config(text=f"{delta_put:.4f}  ({delta_put * 100:.2f}%)", fg="#FF3B30")
            
            self.lbl_info_dias.config(text=f"({t_dias} dias úteis até o vencimento)")

        except ValueError as ve:
            if "vencimento" in str(ve).lower() or "intrínseco" in str(ve).lower():
                messagebox.showwarning("Aviso de Mercado", str(ve))
            else:
                messagebox.showerror("Erro de Digitação", "Por favor, insira apenas números válidos nos campos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {str(e)}")