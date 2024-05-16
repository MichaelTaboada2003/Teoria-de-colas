import pandas as pd
from OptimizedSystem import SistemaDeColasOptimizado

if __name__ == "__main__":
    sistema = SistemaDeColasOptimizado(numero_de_servidores=10, tasa_de_llegada_por_servidor=250, tasa_de_servicio=250)
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
            "Número de Servidores": 10,
            "P0": [p0],
            "Tiempo de Espera (W)": [w],
            "Probabilidad de Espera (P_w)": [pw],
            "Estado del Sistema": [estado],
            "Rho": [rho]
        })
        resultados = pd.concat([resultados, nuevo_registro], ignore_index=True)
        
    for num_servidores in range(10, 21):
        sistema.actualizar_parametros(numero_de_servidores=num_servidores)
        p0, estado = sistema.calcular_p0()
        if estado == "El sistema es estable":
            w = sistema.calcular_tiempo_espera(p0)
            pw = sistema.calcular_probabilidad_espera(p0)
            rho = sistema.calcular_rho()
        else:
            w = pw = rho = None

        nuevo_registro = {
            "Tasa de Servicio": tasa_servicio,
            "Número de Servidores": num_servidores,
            "P0": p0,
            "Tiempo de Espera (W)": w,
            "Probabilidad de Espera (P_w)": pw,
            "Estado del Sistema": estado,
            "Rho": rho
        }
        resultados = pd.concat([resultados, pd.DataFrame([nuevo_registro])], ignore_index=True)

    print(resultados)
