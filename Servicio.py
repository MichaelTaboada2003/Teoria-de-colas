import math
import pandas as pd

class SistemaDeColas:
    def __init__(self, numero_de_servidores, tasa_de_llegada_por_servidor, tasa_de_servicio):
        self.numero_de_servidores = numero_de_servidores
        self.tasa_de_llegada_por_servidor = tasa_de_llegada_por_servidor
        self.tasa_de_servicio = tasa_de_servicio
        self.tasa_de_llegada_total = 2500


    def actualizar_parametros(self, numero_de_servidores=None):
        self.numero_de_servidores = numero_de_servidores
        
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

sistema = SistemaDeColas(numero_de_servidores=10, tasa_de_llegada_por_servidor=250, tasa_de_servicio=250)
resultados = pd.DataFrame()

for tasa_servicio in range(250, 351, 10):  
    sistema.tasa_de_servicio = tasa_servicio
    p0, estado = sistema.calcular_p0()
    if estado == "El sistema es estable":
        w = sistema.calcular_tiempo_espera(p0)
        pw = sistema.calcular_probabilidad_espera(p0)
        rho = sistema.calcular_rho()
    else:
        w = pw = rho = None

    nuevo_registro = pd.DataFrame({
        "Tasa de Servicio": [tasa_servicio],
        "P0": [p0],
        "Tiempo de Espera (W)": [w],
        "Probabilidad de Espera (P_w)": [pw],
        "Estado del Sistema": [estado],
        "Rho": [rho]
    })
    resultados = pd.concat([resultados, nuevo_registro], ignore_index=True)

print(resultados)