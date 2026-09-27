import math
from datetime import date, timedelta

class BlackScholesEngine:
    @staticmethod
    def _norm_cdf(x):
        return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

    @classmethod
    def calculate_price(cls, S, K, t, r, sigma, is_call):
        if sigma <= 0 or t <= 0:
            return max(0, S - K) if is_call else max(0, K - S)
            
        d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * t) / (sigma * math.sqrt(t))
        d2 = d1 - sigma * math.sqrt(t)
        
        if is_call:
            return S * cls._norm_cdf(d1) - K * math.exp(-r * t) * cls._norm_cdf(d2)
        else:
            return K * math.exp(-r * t) * cls._norm_cdf(-d2) - S * cls._norm_cdf(-d1)

    @classmethod
    def find_implied_volatility(cls, target_price, S, K, t, r, is_call):
        valor_intrinseco = max(0, S - K) if is_call else max(0, K - S)
        
        # Trava de segurança com mensagem explicativa
        if target_price < valor_intrinseco:
            tipo = "CALL" if is_call else "PUT"
            raise ValueError(f"Para uma {tipo}, o prêmio (R$ {target_price}) não pode ser menor que o valor intrínseco (R$ {valor_intrinseco:.2f}).")

        limite_inferior = 0.0001
        limite_superior = 10.0 # Teto aumentado para 1000% para cobrir PUTs muito OTM
        
        for _ in range(100):
            meio = (limite_inferior + limite_superior) / 2
            preco_calculado = cls.calculate_price(S, K, t, r, meio, is_call)
            
            if preco_calculado > target_price:
                limite_superior = meio
            else:
                limite_inferior = meio
                
            if (limite_superior - limite_inferior) < 1e-5:
                break
                
        return (limite_inferior + limite_superior) / 2

    @classmethod
    def calculate_delta(cls, S, K, t, r, sigma, is_call):
        if sigma <= 0 or t <= 0:
            return 0.0
            
        d1 = (math.log(S / K) + (r + (sigma ** 2) / 2) * t) / (sigma * math.sqrt(t))
        delta_call = cls._norm_cdf(d1)
        
        return delta_call if is_call else (delta_call - 1)

    @staticmethod
    def get_business_days(target_date):
        hoje = date.today()
        if target_date <= hoje:
            raise ValueError("A data de vencimento deve ser no futuro.")
        
        dias_uteis = 0
        dia_atual = hoje
        while dia_atual < target_date:
            if dia_atual.weekday() < 5:  # Segunda a Sexta
                dias_uteis += 1
            dia_atual += timedelta(days=1)
            
        return dias_uteis