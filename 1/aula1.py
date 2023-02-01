#Exercicio 1.1
def comprimento(lista):
	pass

#Exercicio 1.2
def soma(lista):
	pass

#Exercicio 1.3
def existe(lista, elem):
	pass

#Exercicio 1.4
def concat(l1, l2):
	pass

#Exercicio 1.5
def inverte(lista):
	pass

#Exercicio 1.6
def capicua(lista):
	pass

#Exercicio 1.7
def concat_listas(lista):
	# break condition
	if lista == []:
		return []

	return lista[0] + concat_listas(lista[1:])

#Exercicio 1.8
def substitui(lista, original, novo):
	pass

#Exercicio 1.9
def fusao_ordenada(lista1, lista2):
	# break conditions
	if lista1 == []:
		return lista2
	elif lista2 == []:
		return lista1
	
	# recursive calls
	if lista1[0] < lista2[0]:
		return [lista1[0]] + fusao_ordenada(lista1[1:], lista2)
	else:
		return [lista2[0]] + fusao_ordenada(lista1, lista2[1:])

#Exercicio 1.10
def lista_subconjuntos(lista):
	pass


#Exercicio 2.1
def separar(lista):
	# break condition
	if lista == []:
		return [], []
	temp = separar(lista[1:])
	return [lista[0][0]] + temp[0], [lista[0][1]] + temp[1]

#Exercicio 2.2
def remove_e_conta(lista, elem):
	pass

#Exercicio 3.1
def cabeca(lista):
	pass

#Exercicio 3.2
def cauda(lista):
	pass

#Exercicio 3.3
def juntar(l1, l2):
    pass

#Exercicio 3.4
def menor(lista):
	pass

#Exercicio 3.6
def max_min(lista):
	pass
