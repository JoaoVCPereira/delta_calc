import logging
import math
from datetime import datetime

import flet as ft
from core.calc_engine.calc_engine import BlackScholesEngine
from core.helper import Helper
from models.response import Response


class DesignEngine:
    def __init__(self, page: ft.Page, service, logger:logging.Logger):
        self.page = page
        self.service = service
        self.logger = logger
        self.helper = Helper(self.service,self.logger)
            
        self.selic = self.helper._get_selic()
        self.boleta_id = None
        self._setup_page()
        self._init_components()
        self._build_layout()

    def _setup_page(self):
        self.page.title = "Delta"
        self.page.window.width = 500
        self.page.window.height = 1080
        self.page.window.resizable = False
        self.page.bgcolor = self.service.bg_color
        self.page.padding = 20
        self.page.theme_mode = ft.ThemeMode.LIGHT

    def _create_text_field(self, label=None, width=None, expand=0, read_only=False, on_click=None, value=None, hint_text=None):
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            value=value,
            width=width,
            expand=expand,
            bgcolor=self.service.bg_field_color,
            border_color=self.service.border_color,
            border_radius=10,
            color=self.service.text_color,
            label_style=ft.TextStyle(color=self.service.text_color),
            hint_style=ft.TextStyle(color=self.service.text_color),
            read_only=read_only,
            on_click=on_click,
            text_align=ft.TextAlign.CENTER
        )

    def _abrir_calendario(self, e):
        self.date_picker.open = True
        self.page.update()

    def _init_components(self):
        # Top Section
        self.inp_ticket = self._create_text_field(label="TICKET")
        self.inp_preco_acao = self._create_text_field(label="Preco Acao",width=150)
        self.inp_preco_strike = self._create_text_field(label="Preco Strike",width=150)
        
        self.date_picker = ft.DatePicker(
            on_change=self._on_date_selected,
            first_date=datetime.now(),
        )
        self.page.overlay.append(self.date_picker)
        
        self.inp_vencimento = self._create_text_field(
            label="Selecione o vencimento", 
            read_only=True,
            on_click=self._abrir_calendario
        )
        
        self.inp_taxa_selic = self._create_text_field(label="Taxa Selic", width=200, value=self.selic)

        self.inp_preco_opcao = self._create_text_field(label="Preco opcao", width=150)
        
        self.radio_tipo = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="CALL", label="CALL", fill_color=self.service.border_color),
                ft.Radio(value="PUT", label="PUT", fill_color=self.service.border_color)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            value="CALL"
        )

        self.btn_calcular = ft.Container(
            content=ft.Text("CALCULAR VOLATILIDADE\nE DELTA", color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),
            bgcolor=self.service.button_color,
            width=200,
            height=60,
            border_radius=10,
            alignment=ft.Alignment.CENTER,
            on_click=self._process_calculation,
            ink=True
        )
        
        self.res_vol = self._create_text_field(label="Vol Imp", read_only=True,width=150)
        self.res_delta = self._create_text_field(label="Delta", read_only=True,width=150)

        self.tabela_historico = ft.Column(alignment=ft.MainAxisAlignment.CENTER, spacing=8)

        self.btn_add_boleta = ft.Container(
            content=ft.Text("ADICIONAR A BOLETA", color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),
            bgcolor=self.service.button_color,
            width=200,
            height=60,
            border_radius=10,
            alignment=ft.Alignment.CENTER,
            on_click=self._add_to_boleta,
            ink=True
        )
        self.btn_new_boleta = ft.Container(
            content=ft.Text("NOVA BOLETA", color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),
            bgcolor=self.service.button_color,
            width=120,
            height=30,
            border_radius=10,
            alignment=ft.Alignment.CENTER,
            on_click=self._new_boleta,
            ink=True
        )



    def _update_history_table(self):
        list_last_5_opcoes = self.helper.get_last_5_opcoes()
        
        borda_padrao = ft.Border(
            top=ft.BorderSide(1, self.service.border_color),
            right=ft.BorderSide(1, self.service.border_color),
            bottom=ft.BorderSide(1, self.service.border_color),
            left=ft.BorderSide(1, self.service.border_color)
        )
        
        def _criar_celula(texto):
            return ft.Container(
                content=ft.Text(str(texto), color=self.service.text_color, size=12, text_align=ft.TextAlign.CENTER),
                alignment=ft.Alignment.CENTER,
                bgcolor=self.service.bg_field_color,
                border=borda_padrao,
                border_radius=15,
                height=25,
                expand=1
            )
        
        historico_controls = [
            ft.Row([
                ft.Container(
                    content=ft.Text("ULTIMAS OPCOES", color=self.service.text_color, size=12),
                    alignment=ft.Alignment.CENTER,
                    width=450,
                    height=25,
                    bgcolor=self.service.bg_field_color,
                    border=borda_padrao,
                    border_radius=15
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Row([
                ft.Container(
                    padding=4,
                    width=450,
                    content=ft.Row([
                        _criar_celula("TICKET"),
                        _criar_celula("TIPO"),
                        _criar_celula("STRIKE"),
                        _criar_celula("PRICE"),
                        _criar_celula("DELTA")
                    ], spacing=8)
                )
            ], alignment=ft.MainAxisAlignment.CENTER)
        ]
        
        for op in list_last_5_opcoes:
            linha_dados = ft.Container(
                bgcolor=self.service.button_color,
                border_radius=18,
                padding=4,
                width=450,
                content=ft.Row([
                    _criar_celula(op.ticket),
                    _criar_celula(op.operation_type),
                    _criar_celula(op.strike_price),
                    _criar_celula(op.opcao_price),
                    _criar_celula(op.delta)
                ], spacing=8)
            )
            historico_controls.append(ft.Row([linha_dados], alignment=ft.MainAxisAlignment.CENTER))
        self.tabela_historico.controls.clear()
        self.tabela_historico.controls.extend(historico_controls)

    def _build_layout(self):
        self.page.add(
            ft.Column([
                ft.Row([self.inp_ticket], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.inp_preco_acao, self.inp_preco_strike], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.inp_vencimento], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.inp_taxa_selic], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Divider(height=30, color=self.service.border_color),

                ft.Row([
                    self.radio_tipo,
                    self.inp_preco_opcao
                ], alignment=ft.MainAxisAlignment.CENTER),
                
                ft.Container(height=10),
                ft.Row([self.btn_calcular,self.btn_add_boleta], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.btn_new_boleta], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=10),
                
                ft.Row([self.res_vol,self.res_delta], alignment=ft.MainAxisAlignment.CENTER),

                ft.Divider(height=30, color=self.service.border_color),

                self.tabela_historico
                
            ], spacing=15, scroll=ft.ScrollMode.AUTO)
        )
        
        self._update_history_table()

    def _on_date_selected(self, e):
        if self.date_picker.value:
            self.inp_vencimento.value = self.date_picker.value.strftime("%d/%m/%Y")
            self.inp_vencimento.update()

    def _show_error(self, message):
        self.res_vol.value = "ERRO"
        self.res_delta.value = "ERRO"        
        self.page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=ft.Colors.RED_800)
        self.page.snack_bar.open = True
        self.logger.error(f"[{self.service.name}]Error: {message}")
        self.page.update()

    def _add_to_boleta(self,e):
        self.boleta_id = self.helper._save_boleta(data_opcao=self.data_opcao,id_boleta=self.boleta_id)

    def _new_boleta(self,e):
        self.boleta_id = self.helper._new_boleta(data_opcao=self.data_opcao)
    
    def _process_calculation(self, e):
        try:
            S = float(self.inp_preco_acao.value.replace(',', '.'))
            K = float(self.inp_preco_strike.value.replace(',', '.'))
            r_percentual = float(self.inp_taxa_selic.value.replace(',', '.'))
            preco_mercado = float(self.inp_preco_opcao.value.replace(',', '.'))
            
            if not self.inp_vencimento.value:
                raise ValueError("Selecione a data de vencimento.")
                
            data_vencimento = datetime.strptime(self.inp_vencimento.value, "%d/%m/%Y").date()
            t_dias = BlackScholesEngine.get_business_days(data_vencimento)
            
            is_call = (self.radio_tipo.value == "CALL")

            r = r_percentual / 100.0
            t = t_dias / 252.0

            sigma = BlackScholesEngine.find_implied_volatility(preco_mercado, S, K, t, r, is_call)
            delta = BlackScholesEngine.calculate_delta(S, K, t, r, sigma, is_call)

            vol_percent = sigma * 100
            vol_arredondada = math.ceil(vol_percent * 100) / 100.0
            delta_arredondado = math.ceil(delta * 100) / 100.0

            self.res_vol.value = f"{vol_arredondada:.2f}%"
            self.res_delta.value = f"{delta_arredondado:.2f}"
            
            self.data_opcao = {
                "ticket": self.inp_ticket.value,
                "stockPrice": S,
                "strikePrice": K,
                "opcaoPrice": preco_mercado,
                "selic": r_percentual,
                "operationType": self.radio_tipo.value,
                "executionDate": self.inp_vencimento.value,
                "implicitVol": vol_arredondada, 
                "delta": delta_arredondado 
            }
            
            added_opcao = self.helper._save_opcao(data_opcao=self.data_opcao)
            self.logger.info(f"[{self.service.name}]{added_opcao.message}||{added_opcao.status}")
            
            # Recalcula a tabela
            self._update_history_table()
            
            # Atualiza o ecrã inteiro de uma só vez (resultados e tabela)
            self.page.update()

        except ValueError as ve:
            self._show_error(str(ve))
        except Exception as ex:
            self._show_error(f"Erro inesperado: {str(ex)}")