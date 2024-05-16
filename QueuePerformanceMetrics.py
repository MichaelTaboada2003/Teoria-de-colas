import math
import pandas as pd

class SistemaDeColas:
    def __init__(self, numero_de_servidores, tasa_de_llegada_por_servidor, tasa_de_servicio):
        self.numero_de_servidores = numero_de_servidores
        self.tasa_de_llegada_por_servidor = tasa_de_llegada_por_servidor
        self.tasa_de_servicio = tasa_de_servicio
        self.tasa_de_llegada_total = self.tasa_de_llegada_por_servidor * self.numero_de_servidores
        
    def calcular_rho(self):
        return self.tasa_de_llegada_total / (self.numero_de_servidores * self.tasa_de_servicio)

    def calcular_p0(self):
        rho = self.calcular_rho()
        if rho >= 1:
            return 0, "El sistema es inestable"
        
        suma_p0 = sum([(self.tasa_de_llegada_total / self.tasa_de_servicio)**n / math.factorial(n) for n in range(self.numero_de_servidores)])
        termino_final_p0 = (self.tasa_de_llegada_total / self.tasa_de_servicio)**self.numero_de_servidores / (math.factorial(self.numero_de_servidores) * (1 - rho))
        p0 = 1 / (suma_p0 + termino_final_p0)
        return p0, "El sistema es estable"

    def calcular_tiempo_espera(self, p0):
        numerador = (self.tasa_de_llegada_total / self.tasa_de_servicio)**self.numero_de_servidores * self.tasa_de_servicio
        denominador = math.factorial(self.numero_de_servidores - 1) * (self.numero_de_servidores * self.tasa_de_servicio - self.tasa_de_llegada_total)**2
        return numerador / denominador * p0 + 1 / self.tasa_de_servicio

    def calcular_probabilidad_espera(self, p0):
        term = (self.tasa_de_llegada_total / self.tasa_de_servicio)**self.numero_de_servidores
        factor = self.numero_de_servidores * self.tasa_de_servicio / (self.numero_de_servidores * self.tasa_de_servicio - self.tasa_de_llegada_total)
        return 1 / math.factorial(self.numero_de_servidores) * term * factor * p0
    
if __name__ == "__main__":
    sistema = SistemaDeColas(numero_de_servidores=10, tasa_de_llegada_por_servidor=200, tasa_de_servicio=250)
    resultados = pd.DataFrame(columns=["Tasa de Llegada", "P0", "Tiempo de Espera (W)", "Probabilidad de Espera (P_w)", "Estado del Sistema", "Rho"])    
    
    """
    Por definición ρ es la tasa de uso de cada servidor (porcentaje del tiempo que cada servidor es ocupado).
    
    Aumento de la tasa de llegada por servidor, desde 150 hasta 250 con incrementos de 10, lo que 
    implica un aumento de la tasa de llegada total del sistema (λ) de 1500 a 2500.
    
    Variamos la tasa de llegada del servidor, para analizar cuál es su comportamiento en el sistema.
    Principalmente para dictaminar en qué punto el sistema es inestable. Posteriormente, usamos la
    llegada total del sistema (λ) dentro de la cuál el sistema es inestable, para optimizar el sistema.
    
    El sistema es inestable cuando el valor de ρ es mayor o igual a 1. Lo que implica que el sistema
    no es capaz de procesar las solicitudes entrantes, y por lo tanto, se acumulan en la cola.
    
    ρ es igual a λ / (μ * c), donde λ es la tasa de llegada total, μ es la tasa de servicio 
    k es el número de servidores. Por lo cuál ρ es directamente proporcional a la tasa de llegada total.
    Eso quiere decir que a medida que aumenta la tasa de llegada total, ρ crece y el sistema se vuelve inestable.
    
    """
    
    for tasa in range(150, 251, 10):
        sistema.tasa_de_llegada_por_servidor = tasa
        sistema.tasa_de_llegada_total = tasa * sistema.numero_de_servidores
        p0, estado = sistema.calcular_p0()
        if estado == "El sistema es estable":
            w = sistema.calcular_tiempo_espera(p0)
            pw = sistema.calcular_probabilidad_espera(p0)
            rho = sistema.calcular_rho()
        else:
            w = pw = rho = None
        
        nuevo_registro = pd.DataFrame({
            "Tasa de Llegada": [tasa],
            "P0": [p0],
            "Tiempo de Espera (W)": [w],
            "Probabilidad de Espera (P_w)": [pw],
            "Estado del Sistema": [estado],
            "Rho": [rho]
        })
        resultados = pd.concat([resultados, nuevo_registro], ignore_index=True)

    print(resultados)














