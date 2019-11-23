# -*- coding: utf-8 -*-

import re
import unicodedata
import math
class IndiceInvertido:

	def __init__(self, lista_documentos):
		self.tf = {}
		self.df = {}
		self.idf = {}
		self.nomes_documentos = lista_documentos
		self.arquivos_adequados = self.adequa_doc()
		self.palavra_pos = self.palavra_pos()
		self.indice_final = self.indice_invertido()
		#self.vectors = self.vectorize()
		#self.normas = self.norma_vetor(self.nomes_documentos)
		self.preenche_pontuacao()



	@staticmethod
	def removerAcentosECaracteresEspeciais(palavra):

	    # Unicode normalize transforma um caracter em seu equivalente em latin.
	    nfkd = unicodedata.normalize('NFKD', palavra)
	    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

	    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
	    return re.sub('[^a-zA-Z0-9 ]', '', palavraSemAcento)


	def adequa_doc(self):
		'''Adequa(separa as palavras, retira acentos e etc) as palavras da lista de documentos da instância atual.'''


		arquivos_adequados = {}
		aux_list = list()
		for file in self.nomes_documentos:
			pattern = re.compile('[\W_]+')
			try:
				arquivos_adequados[file] = open(file, 'r', encoding='utf-8').read().lower()
			except:
				raise ValueError("Arquivo não existe!")
			arquivos_adequados[file] = pattern.sub(' ',arquivos_adequados[file])
			arquivos_adequados[file] = self.removerAcentosECaracteresEspeciais(arquivos_adequados[file])
			aux_list.append(arquivos_adequados[file])
			re.sub(r'[\W_]+','', arquivos_adequados[file])
			arquivos_adequados[file] = arquivos_adequados[file].split()
			
		return arquivos_adequados

	def indexa_palavra(self, lista_palavras):
		'''Indexa uma lista de palavras, mapeando cada palavra a sua posição no seu respectivo documento.'''
		arquivo_indexado = {}
		for indice, palavra in enumerate(lista_palavras):
			if palavra in arquivo_indexado.keys():
				arquivo_indexado[palavra].append(indice)
			else:
				arquivo_indexado[palavra] = [indice]
		return arquivo_indexado

	def cria_indice(self, lista_documentos):
		'''Indexa um conjunto de arquivos, mandando cada arquivo para "indexa_palavra()" e juntando tudo num dicionário "dict_completo" '''
		'''Recebe um dicionário onde as chaves são os documentos e os valores são as palavras desse documento
		   e retorna um dicionário que tem como chaves o nome do documento e como valor a posição de cada palavra nesse documento'''
		dict_completo = {}
		for nome_documento in lista_documentos.keys():
			dict_completo[nome_documento] = self.indexa_palavra(lista_documentos[nome_documento])
			#print(lista_documentos[nome_documento])
		return dict_completo

	def indiceFinal(self):
		indice_final = {}
		indice_posicao = self.palavra_pos
		for filename in indice_posicao.keys():
			self.tf[filename] = {}
			for palavra in indice_posicao[filename].keys():
				self.tf[filename][palavra] = len(indice_posicao[filename][palavra])
				if palavra in self.df.keys():
					self.df[palavra] += 1
				else:
					self.df[palavra] = 1 
				if palavra in indice_final.keys():
					if filename in indice_final[palavra].keys():
						indice_final[palavra][filename].append(indice_posicao[filename][palavra][:])
					else:
						indice_final[palavra][filename] = indice_posicao[filename][palavra]
				else:
					indice_final[palavra] = {filename: indice_posicao[filename][palavra]}
		##Frequência de cada palavra em cada documento
		#print(self.tf)
		
		##Frequência de cada palavra levando em conta todo o dataset
		#print(self.df)
		return indice_final
	
	###Esta seria uma outra abordagem que seria criar o vetor para cada documentos considerando dimensão n, onde
	### seria a quantidade de palavras distintas daquele vetor, isto implicaria em vetores de documentos
	### de dimensionalidade diferentes

	### A abordagem que será utilizada será a de vetorizar o documentos levando em conta as palavras distintas de todo o banco de dados
	### e não a quantida de palavras distintas de cada documentos, isto vai implicar que todos os vetores de documentos terão a mesma dimensão

	#def vectorize(self):
	#	vectors = {}
	#	for filename in self.nomes_documentos:
	#		vectors[filename] = [len(self.palavra_pos[filename][palavra]) for palavra in self.palavra_pos[filename].keys()]
	#	return vectors


	def numero_documentos(self):
		return len(self.nomes_documentos)

	### Não vamos utilizar a norma nesse caso
	#def norma_vetor(self, docuentos):
	#	normas = {}
	#	for document in docuentos:
	#		normas[document] = pow(sum(map(lambda x: x**2, self.vectors[document])),.5)
	#	return normas

	
	def frequencia_palavra(self, palavra, documento):
		'''Retorna quantas vezes a "palavra" apareceu no "documento" '''
		return self.tf[documento][palavra] if palavra in self.tf[documento].keys() else 0

	def preenche_pontuacao(self): 
		'''Retorna as "pontuações da instância atual, df, tf e idf" '''
		for nome_documento in self.nomes_documentos:
			for palavra in self.vocabulario():
				self.tf[nome_documento][palavra] = self.frequencia_palavra(palavra, nome_documento)
				if palavra in self.df.keys():
					self.idf[palavra] = self.calcula_idf(self.numero_documentos(), self.df[palavra]) 
				else:
					self.idf[palavra] = 0
		return self.df, self.tf, self.idf

	def calcula_idf(self, N, Nx):
		if Nx != 0:
			return math.log(N/Nx)
		else:
		 	return 0

	def calcula_pontuacao(self, term, document):
		'''Faz o calculo do tfxidf'''
		return self.tf[document][term] * self.idf[term]

	def indice_invertido(self):
		#print(self.indiceFinal())
		return self.indiceFinal()

	def palavra_pos(self):
		'''Retorna uma lista de cada palavra da instância atual mapeada com a posição em que ela aparece no documento.'''
		return self.cria_indice(self.arquivos_adequados)

	def vocabulario(self):
		"""Retorna as chaves do índice invertido final que nada mais são do que as palavras distintas presentes no banco de dados."""
		return self.indice_final.keys()


x = IndiceInvertido(['d1.txt', 'd2.txt', 'd3.txt', 'd4.txt'])
y = IndiceInvertido(['doc1.txt', 'doc2.txt', 'doc3.txt'])

