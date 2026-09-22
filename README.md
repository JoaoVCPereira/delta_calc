# Calculadora Delta Pro

Aplicativo em Python com interface gráfica (GUI) desenvolvido para calcular a Volatilidade Implícita e o Delta de opções financeiras utilizando o modelo de Black-Scholes. O projeto adota uma arquitetura modular baseada em serviços e configurações centralizadas.

## Funcionalidades

* **Cálculo de Volatilidade Implícita e Delta:** Realiza a engenharia reversa a partir do preço de mercado da opção e fornece os valores exatos de Delta para opções Call e Put.


* **Interface Gráfica Interativa:** Construída com `tkinter` e `tkcalendar`, permite a seleção da data de vencimento via calendário e o cálculo automático de dias úteis. A identidade visual, incluindo cores e fontes, é gerida pela classe de configuração `DeltaCalc`.


* **Integração com Windows:** Utiliza a biblioteca `ctypes` para definir um AppUserModelID exclusivo (`delta_calc.1_0`), garantindo que o sistema operacional identifique o programa como um aplicativo independente para a exibição de ícones.



## Estrutura do Projeto

O projeto está organizado nas seguintes pastas e arquivos principais:

* **`.venv/`**: Ambiente virtual contendo as dependências do projeto.
    * **`config/`**:
    * `environment.py`: Centraliza as variáveis de ambiente (carregadas via `python-dotenv`) e as configurações visuais da aplicação (cores, fontes) na classe `DeltaCalc`.

* **`core/`**:
    * `delta_calc/delta_calc.py`: Contém a classe `DeltaCalc`, responsável pelas funções matemáticas de Black-Scholes e pela construção da interface gráfica (GUI).


    * `services.py`: Contém a classe `DeltaCalcService`, que gerencia a inicialização e o ciclo de vida da interface gráfica, além de registrar logs de atividade.


* **`log/`**: Diretório destinado ao armazenamento dos arquivos de log `log.log`.


* **`models/`**: Contém o arquivo de ícone da aplicação (`delta_pro.ico`) e o arquivo `response.py` com mensagens padrão.


* **`utils/`**:
    * `utils.py`: Funções utilitárias auxiliares, como a obtenção do diretório raiz (`get_root_path`), manipulação de datas e leitura/escrita de arquivos JSON.


    * `log_utils.py`: Configura o sistema de logging da aplicação, definindo formatos e níveis de log baseados nas configurações de ambiente.


* **`main.py`**: O ponto de entrada da aplicação. Configura o logger e inicializa o serviço `DeltaCalcService`.


* **`delta_calc.bat`**: Script de inicialização em lote que executa a aplicação utilizando o interpretador Python (`pythonw.exe`) diretamente do ambiente virtual, sem abrir a janela do console.


* **`requirements.txt`**: Lista as dependências do projeto, incluindo `python-dotenv` e `tkcalendar`.


* **`.env`**: Ficheiro com as variáveis de ambiente necessárias para a configuração.



## Configuração e Inicialização

1. **Instalação de Dependências:** Certifique-se de que o ambiente virtual está ativo e instale os pacotes listados em `requirements.txt`.


2. **Variáveis de Ambiente:** Configure o arquivo `.env` na raiz do projeto com as chaves necessárias, como `LEVEL_FULL`, `PATH_FULL`, `DELTA_CALC_NAME`, e `DELTA_CALC_CRON`.


3. **Execução:** Para iniciar a aplicação, utilize o ficheiro de lote `delta_calc.bat`. Este script ativará o executável correto do ambiente virtual e iniciará o fluxo a partir do `main.py`.