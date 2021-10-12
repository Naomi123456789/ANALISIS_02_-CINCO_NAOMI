import csv
import pandas as pd


lista_datos =[]
with open("logistics.csv", "r") as  archivo:
    lector =csv. DictReader(archivo)

    for registro in lector:
        lista_datos.append(registro)

#RUTAS DE IMPORTACIÓN Y EXPORTACIÓN
def rutas_exportacion_importacion (direccion):
    contador = 0
    rutas_contadas = []
    rutas_conteo = []

    for ruta in lista_datos:
        if ruta["direction"] == direccion:
            ruta_actual = [ruta["origin"], ruta["destination"]]
            #print(ruta_actual)
            if ruta_actual not in rutas_contadas:
                for ruta_bd in lista_datos:
                    if ruta_actual == [ruta_bd["origin"], ruta_bd["destination"]]:
                        contador += 1

                rutas_contadas.append(ruta_actual)
                rutas_conteo.append([ruta["origin"], ruta["destination"], contador])
                contador = 0

    rutas_conteo.sort(reverse = True, key = lambda x:x[2])
    return rutas_conteo



conteo_exportaciones = rutas_exportacion_importacion("Exports")
conteo_importanciones = rutas_exportacion_importacion("Imports")
print(conteo_exportaciones)
print(conteo_importanciones)


#MEDIO DE TRANSPORTE UTILIZADO
lista_datos_pd = pd.read_csv("logistics.csv")

species_counts = lista_datos_pd.groupby('transport_mode').count()
print(species_counts)

df = pd.DataFrame(lista_datos_pd)
print(df.groupby(by=['transport_mode']).sum().groupby(level=[0]).cumsum())



# VALOR TOTAL DE IMPORTACIONES Y EXPORTACIONES

def valor_movimiento(direccion):
	contados = []
	valores_paises = []

	for viaje in lista_datos:
		actual = [direccion, viaje["origin"]] #["Exports", "Mexico"]
		valor = 0
		operaciones = 0

		if actual in contados:
			continue

		for movimiento in lista_datos:
			if actual == [movimiento["direction"], movimiento["origin"]]:
				valor += int(movimiento["total_value"])
				operaciones += 1
		
		contados.append(actual)
		valores_paises.append([direccion, viaje["origin"], valor, operaciones])
	
	valores_paises.sort(reverse = True, key = lambda x:x[2])
	return valores_paises



valores_paises = valor_movimiento("Exports")


def porcentaje_pais(lista_paises, porcentaje = 0.8):
	valor_total = 0
	for pais in lista_paises:
		valor_total += pais[2]
	
	paises = []
	porcentajes_calculados = []
	valor_actual = 0

	for pais in lista_paises:
		valor_actual += pais[2]
		porcentaje_actual = round(valor_actual/valor_total, 3)
		paises.append(pais)
		porcentajes_calculados.append(porcentaje_actual)

		if porcentaje_actual <= porcentaje:
			continue
		else:
			if porcentaje_actual - porcentaje <= porcentajes_calculados[-2] - porcentaje:
				break
			else:
				paises.pop(-1)
				porcentajes_calculados.pop(-1)
				break
	
	return paises


paises_80 = porcentaje_pais(valor_movimiento("Exports"))


for pais in paises_80:
	print(pais)



