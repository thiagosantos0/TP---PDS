import indice_invertido
import re
import unicodedata

class Consulta:

	def __init__(self, nomes_documento):
		self.nomes_documento = nomes_documento
		self.indice = indice_invertido.IndiceInvertido(self.nomes_documento)
		self.indice_invertido_final = self.indice.indice_final
		self.regularindice = self.indice.palavra_pos


	@staticmethod
	def removerAcentosECaracteresEspeciais(palavra):
	    nfkd = unicodedata.normalize('NFKD', palavra)
	    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

	    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
	    return re.sub('[^a-zA-Z0-9 ]', '', palavraSemAcento)

	def consulta_uma_palavra(self, palavra):
		pattern = re.compile('[\W_]+')
		palavra = pattern.sub(' ',palavra)
		palavra = self.removerAcentosECaracteresEspeciais(palavra).lower()
		if palavra in self.indice_invertido_final.keys():
			return self.resultadosConsultas([nome_documento for nome_documento in self.indice_invertido_final[palavra].keys()], palavra)
		else:
			return []

	def consulta_simples(self, consulta):
		pattern = re.compile('[\W_]+')
		consulta = pattern.sub(' ',consulta)
		resultado_consulta = []
		for palavra in consulta.split():
			palavra = self.removerAcentosECaracteresEspeciais(palavra)
			resultado_consulta += self.consulta_uma_palavra(palavra)
		return self.resultadosConsultas(list(set(resultado_consulta)), consulta)

	
	def consulta_exata(self, consulta):
		pattern = re.compile('[\W_]+')
		consulta = pattern.sub(' ',consulta)
		lista_lista_posicoes, resultado_consulta = [],[]
		for palavra in consulta.split():
			palavra = self.removerAcentosECaracteresEspeciais(palavra)
			lista_lista_posicoes.append(self.consulta_uma_palavra(palavra))
		interseccao = set(lista_lista_posicoes[0]).intersection(*lista_lista_posicoes)
		#print(interseccao)
		for nome_documento in interseccao:
			posicoes_palavras = []

			for palavra in consulta.split():
				palavra = self.removerAcentosECaracteresEspeciais(palavra).lower()
				posicoes_palavras.append(self.indice_invertido_final[palavra][nome_documento][:])

			#A quantidade de posições equivale a quantidade de palavras, coisa que necessito para verificar a interseccção
			j = len(posicoes_palavras)
			for i in range(len(posicoes_palavras)):
				for ind in range(len(posicoes_palavras[i])):
					posicoes_palavras[i][ind] += j
				j = j - 1				
			if set(posicoes_palavras[0]).intersection(*posicoes_palavras):
				resultado_consulta.append(nome_documento)
		print(resultado_consulta)
		print(consulta)

		return self.resultadosConsultas(resultado_consulta, consulta)

	def vetorizar(self, documentos):
		vetores_documentos = {}
		for doc in documentos:
			docVec = [0]*len(self.indice.vocabulario())
			for ind, term in enumerate(self.indice.vocabulario()):
				docVec[ind] = self.indice.calcula_pontuacao(term, doc)
			vetores_documentos[doc] = docVec
		#print(vetores_documentos)
		return vetores_documentos


	
	def vetorizar_consulta(self, consulta):
		pattern = re.compile('[\W_]+')
		consulta = pattern.sub(' ',consulta)
		consulta = self.removerAcentosECaracteresEspeciais(consulta)
		consulta_lista = consulta.split()
		consulta_vetor = [0]*len(consulta_lista)
		indice = 0
		for ind, palavra in enumerate(consulta_lista):
			consulta_vetor[indice] = self.frequencia_consulta(palavra, consulta)
			indice += 1

		consulta_idf = [self.indice.idf[palavra] for palavra in self.indice.vocabulario()]
		##Isso aqui é a norma, mas não vou usar isso mais
		magnitude = pow(sum(map(lambda x: x**2, consulta_vetor)),.5)
		frequencia = self.frequencia_dataset(self.indice.vocabulario(), consulta)
		tf = [x for x in frequencia]
		final = [tf[i]*consulta_idf[i] for i in range(len(self.indice.vocabulario()))]
		#print(len([x for x in consulta_idf if x != 0]) - len(consulta_idf))
		return final

	def frequencia_consulta(self, term, consulta):
		'''Calcula a frequencia de cada palavra da colsulta, retorna quantas vezes a a palavra consultada apareceu na consulta como um todo.'''
		cont = 0
		#print(consulta)
		#print(consulta.split())
		term = self.removerAcentosECaracteresEspeciais(term).lower()
		for palavra in consulta.split():
			palavra = self.removerAcentosECaracteresEspeciais(palavra).lower()
			if palavra == term:
				cont = cont + 1
		return cont


	##tf
	def frequencia_dataset(self, vocabulario, palavra):
		'''Retorna uma lista de tamanho n, onde n é a quantidade de palavras distintas, isto é, a quantidade de palavras no vocabulário. Esta lista vai ter 
		conter '1' na posição que a palavra aparece no vocabulário.'''
		lista_retorno = [0]*len(vocabulario)
		
		for elemento in vocabulario:
			elemento = self.removerAcentosECaracteresEspeciais(elemento).lower()

		for i,elemento in enumerate(vocabulario):
			lista_retorno[i] = self.frequencia_consulta(elemento, palavra)
			#print(self.frequencia_consulta(term, query))
		return lista_retorno

	

	def produto_interno(self, documento1, documento2):
		'''Realiza o produto interno entre dois vetores. No caso aqui serão dois vetores de documentos'''
		if len(documento1) != len(documento2):
			return 0
		#print(documento1)
		#print(documento2)
		#print(sum([x*y for x,y in zip(documento1, documento2)]))
		return sum([x*y for x,y in zip(documento1, documento2)])

	def resultadosConsultas(self, resultDocs, query):
		'''Retorna o resultado final da busca, uma lista com os documentos colocados em ordem decrescente tendo como métrica a proximidade com a consulta.'''
		vetores = self.vetorizar(resultDocs)
		##vetores de documentos que foram processados e enviados para o output.
		#print(vetores)
		vetores_consulta = self.vetorizar_consulta(query)
		##Vetor da consulta também de tamanho n, onde n é o tamanho do vocabulário
		#print(vetores_consulta)
		##Lista com a pontuação (proximidade) dos documentos da consulta, através da similaridade cosseno.
		resultados = [[self.produto_interno(vetores[result], vetores_consulta), result] for result in resultDocs]
		#print([[self.produto_interno(vetores[result], vetores_consulta), result] for result in resultDocs])
		#print(resultados)
 		##Colocando os documentos em ordem decrescente, do que tem maior proximidade com a consulta para o menor.
		resultados.sort(key=lambda x: x[0], reverse=True)
		
		##Tentativa falha de criar um vetor "apresentação" que apresentasse documentos com a mesma pontuação em apenas umas lista
		##No caso do teste que esta no pdf do trabalho ficaria ['d4.txt', 'd1.txt', 'd3.txt, d4.txt']
		
		#apresentacao = resultados.copy()
		#for i in range(0, len(resultados) - 1):
		#	if apresentacao[i][0] == apresentacao[i+1][0]:
		#		apresentacao[i][1] = apresentacao[i][1] + ", " + apresentacao[i+1][1]
		#		apresentacao.pop()
		
		#print(resultados)
		resultados = [x[1] for x in resultados]
		return resultados



q = Consulta(['d1.txt', 'd2.txt', 'd3.txt', 'd4.txt'])
teste = Consulta(['10003', '10004', '10005', '10006', '10009', '10010', '10011', '10013', '10014', '10015', '10018', '10019', '10021', '10022', '10024', '10026', '10027', '10028', '10029', '10030', '10032', '10033', '10034'])




teste1 = teste.consulta_simples("From")
print(teste1)