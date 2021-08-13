# -*- coding: utf-8 -*-

# Se implementa un algoritmo genético que comienza con una población 
# base de cadenas generadas aleatoriamente, itera sobre un cierto número de generaciones 
# mientras implementa la "selección natural", e imprime la cadena más ajustada.

# Los parámetros de la simulación pueden cambiarse modificando una de las muchas 
# variables globales. Para cambiar la cadena "más ajustada", modifique OPTIMAL. 
# POP_SIZE controla el tamaño de cada generación, y GENERATIONS es la cantidad de  
# generaciones que la simulación recorrerá antes de devolver la cadena más apta más apto.


import random

# -------------------------------------------------------------------------------------
# Variables Globales
# Configuración de la cadena óptima y las variables de entrada del AG.
# -------------------------------------------------------------------------------------

CADENA      = "Tomas Echeverri Restrepo"
TAMANO_GEN    = len(CADENA )
POBLACION_IN    = 50
GENERACIONES = 6000

# -------------------------------------------------------------------------------------
# Funciones de ayuda
# Se utilizan como apoyo, pero no son funciones directas específicas de AG. functions.
# -------------------------------------------------------------------------------------

  # Elige un elemento al azar de entre los ítems, donde ítems es una lista de tuplas 
  # de la forma (ítem, peso). la forma (elemento, peso). El peso determina la probabilidad 
  # de elegir su elemento respectivo

def peso_escogido (items):
  peso_total = sum((item[1] for item in items))
  n = random.uniform(0, peso_total)
  for item, peso in items:
    if n < peso:
      return item
    n = n - peso
  return item

  # Devuelve un carácter aleatorio entre ASCII 32 y 126 (es decir, espacios, símbolos, 
  # letras y dígitos). Todos los caracteres devueltos serán agradablemente imprimibles.

def caracter_aleatorio():
  return chr(int(random.randrange(32, 126, 1)))

  # Devuelve una lista de individuos POP_SIZE, cada uno generado aleatoriamente 
  # mediante la iteración de DNA_SIZE veces para generar una cadena de caracteres 
  # aleatorios con random_char().
def poblacion_aleatoria():
  pop = []
  for i in range(POBLACION_IN):
    dna = ""
    for c in range(TAMANO_GEN):
      dna += caracter_aleatorio()
    pop.append(dna)
  return pop

# -------------------------------------------------------------------------------------
# Funciones AG.
# Construye la logica del AG.
# -------------------------------------------------------------------------------------

  # Para cada gen en el ADN, esta función calcula la diferencia entre él y el carácter 
  # en la misma posición en la cadena OPTIMAL. Estos valores se suman y se devuelven.
def fitness(dna):
  fitness = 0
  for c in range(TAMANO_GEN):
    fitness += abs(ord(dna[c]) - ord(CADENA [c]))
  return fitness


  # Para cada gen del ADN, hay una probabilidad de 1/mutation_chance de que se cambie 
  # por un carácter aleatorio. Esto garantiza la diversidad en la población y asegura 
  # que es difícil quedarse atascado en mínimos locales.

def mutacion(dna):
  salida_dna = ""
  probabilidad_mutacion = 100
  for c in range(TAMANO_GEN):
    if int(random.random()*probabilidad_mutacion) == 1:
      salida_dna += caracter_aleatorio()
    else:
      salida_dna += dna[c]
  return salida_dna


  # Corta el ADN1 y el ADN2 en dos partes en un índice aleatorio dentro de su longitud 
  # y los fusiona. Ambos mantienen su sublista inicial hasta el índice de cruce pero sus 
  # extremos se intercambian.
def cruce (dna1, dna2):
  pos = int(random.random()*TAMANO_GEN)
  return (dna1[:pos]+dna2[pos:], dna2[:pos]+dna1[pos:])


# Programa principal
# Generar una población y simular GENERACIONES generaciones.

if __name__ == "__main__":
  # Genera la población inicial. Esto creará una lista de cadenas POP_SIZE,
  # cada una inicializada con una secuencia de caracteres aleatorios.
  poblacion = poblacion_aleatoria()

  #  Simula todas las generaciones.
  for generacion in range(GENERACIONES):
    print ("Generacion %s... Gen aleatorio : '%s'" % (generacion, poblacion[0]))
    peso_poblacion = []

    # Añade individuos y sus respectivos niveles de aptitud a la lista de población
    # ponderada. Esto se utilizará para sacar individuos a través de ciertas probabilidades
    # durante la fase de selección. A continuación, restablecer la lista de la población para
    # que podamos repoblar después de la selección.
    for individual in poblacion:
      fitness_val = fitness(individual)

      # Generar el par (individuo,aptitud), teniendo en cuenta si vamos a dividir 
      # accidentalmente por cero.
      if fitness_val == 0:
        tupla = (individual, 1.0)
      else:
        tupla = (individual, 1.0/fitness_val)

      peso_poblacion.append(tupla )

    poblacion = []

    # Selecciona dos individuos al azar, basándose en sus probabilidades de aptitud, 
    # cruza sus genes en un punto aleatorio, los muta y los añade de nuevo a la población 
    # para la siguiente iteración.
    for i in range( int(POBLACION_IN / 2) ):
      # Seleccion
      ind1 = peso_escogido (peso_poblacion)
      ind2 = peso_escogido (peso_poblacion)

      # Cruce
      ind1, ind2 = cruce (ind1, ind2)

      # Mutar y volver a añadir a la población.
      poblacion.append(mutacion(ind1))
      poblacion.append(mutacion(ind2))

  # Muestra la cadena mejor clasificada después de que se hayan iterado todas las 
  # generaciones. Esta será la cadena más cercana a la cadena ÓPTIMA, lo que significa 
  # que tendrá el menor valor de aptitud. Finalmente, salir del programa.
  cadena_ajustada = poblacion[0]
  fitness_minimo = fitness(poblacion[0])

  for individual in poblacion:
    ind_fitness = fitness(individual)
    if ind_fitness <= fitness_minimo:
      cadena_ajustada = individual
      fitness_minimo = ind_fitness

  print ("CADENA MAS AJUSTADA: %s" % cadena_ajustada)

  exit(0)