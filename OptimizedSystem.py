import math
import pandas as pd

class SistemaDeColasOptimizado:
    
    """
    
    tasa promedio de llegada (λ): “se define como la cantidad de clientes que llegan en un 
    tiempo al sistema.”
    
    La tasa de llegada total, es la tasa de llegada por servidor multiplicada por el número de servidores,
    con esto, se obtiene la tasa de llegada total al sistema, lo cuál sería la tasa de llegada promedio (λ).
    (No es lo mismo la tasa de llegada por servidor a la tasa de llegada promedio)
    
    En este caso se tiene un sistema con 10 servidores, cada uno con una tasa de llegada de 250 
    clientes por segundo. Por lo tanto, la tasa de llegada total al sistema es de 2500 clientes por segundo 
    (λ = 2500). Esta tasa de llegada, es la vuelve al sistema inestable y por lo tanto, se necesita optimizar.

    """
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
    
if __name__ == "__main__":
    sistema_servidores = SistemaDeColasOptimizado(numero_de_servidores=10, tasa_de_llegada_por_servidor=250, tasa_de_servicio=250)
    sistema_tasa_servicio = SistemaDeColasOptimizado(numero_de_servidores=10, tasa_de_llegada_por_servidor=250, tasa_de_servicio=250)
    
    resultado_aumento_servidores = pd.DataFrame()
    resultado_aumento_tasa_servicio = pd.DataFrame()
    resultado_aumento_servidores_tasa_servicio = pd.DataFrame()
    
    """
    
    Aumento de la tasa de servicio, desde 250 hasta 350 con incrementos de 10.
    
    """
    
    for tasa_servicio in range(250, 351, 10):  
        sistema_tasa_servicio.tasa_de_servicio = tasa_servicio
        p0, estado = sistema_tasa_servicio.calcular_p0()
        if estado == "El sistema es estable":
            w = sistema_tasa_servicio.calcular_tiempo_espera(p0)
            pw = sistema_tasa_servicio.calcular_probabilidad_espera(p0)
            rho = sistema_tasa_servicio.calcular_rho()
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
        resultado_aumento_tasa_servicio = pd.concat([resultado_aumento_tasa_servicio, nuevo_registro], ignore_index=True)
        
        """
        
        Aumento de la tasa de servicio y el número de servidores, desde 10 hasta 20 con incrementos de 1.
        
        """
        
    for num_servidores in range(10, 21):
        sistema_servidores.actualizar_parametros(numero_de_servidores=num_servidores)
        p0, estado = sistema_servidores.calcular_p0()
        if estado == "El sistema es estable":
            w = sistema_servidores.calcular_tiempo_espera(p0)
            pw = sistema_servidores.calcular_probabilidad_espera(p0)
            rho = sistema_servidores.calcular_rho()
        else:
            w = pw = rho = None

        nuevo_registro = {
            "Número de Servidores": [num_servidores],
            "P0": [p0],
            "Tiempo de Espera (W)": [w],
            "Probabilidad de Espera (P_w)": [pw],
            "Estado del Sistema": [estado],
            "Rho": [rho]
        }
        resultado_aumento_servidores = pd.concat([resultado_aumento_servidores, pd.DataFrame(nuevo_registro)], ignore_index=True)


    print(resultado_aumento_servidores)
    print(resultado_aumento_tasa_servicio)
    