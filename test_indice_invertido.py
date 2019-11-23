# -*- coding: utf-8 -*-
import unittest
import indice_invertido
##Indice invertido
import re
import unicodedata
import math


class TestIndiceInvertido(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		pass

	@classmethod
	def tearDownClass(cls):
		pass

	#Esta função roda antes de qualquer teste
	def setUp(self):
		self.indice_1 = indice_invertido.IndiceInvertido(['d1.txt', 'd2.txt', 'd3.txt', 'd4.txt'])
		self.indice_2 = indice_invertido.IndiceInvertido(['doc1.txt', 'doc2.txt', 'doc3.txt'])

	#Esta função roda depois de qualquer teste
	def tearDown(self):
		pass


	def test_adequa_doc(self):
		self.assertEqual(self.indice_1.adequa_doc(), {'d1.txt': ['a', 'a', 'a', 'b'], 'd2.txt': ['a', 'a', 'c'], 'd3.txt': ['a', 'a'], 'd4.txt': ['b', 'b']})


	def test_indexa_palavra(self):
		entrada_valida = ['a', 'a', 'a', 'b']
		saida_esperada  = {'a': [0, 1, 2], 'b': [3]}
		self.assertEqual(self.indice_1.indexa_palavra(entrada_valida), saida_esperada)
		self.assertEqual(self.indice_1.indexa_palavra([]), {})

		with self.assertRaises(TypeError, msg="Não ocorreu um erro de tipo."):
			self.indice_1.indexa_palavra(1)


	def test_cria_indice(self):
		lista_palavras = ['a', 'a', 'a', 'b']
		string = "a, a, a, b"
		##Verificando se a função realmente retorna um dicionário
		retorno_cria_indice = self.indice_1.indexa_palavra(lista_palavras)
		self.assertEqual(self.indice_1.indexa_palavra(lista_palavras), {'a': [0, 1, 2], 'b': [3]})
		self.assertEqual(self.indice_1.indexa_palavra([]), {})
		self.assertTrue(type(retorno_cria_indice) == dict, msg="A função cria_indice não esta retornado um dicionário")
		##Se ocorrer um erro de tipo o teste passa.
		with self.assertRaises(AttributeError, msg="Não ocorreu um erro de Atributo"):
			self.indice_1.cria_indice(1)


	def test_indice_final(self):
		retorno_indice_final = self.indice_1.indiceFinal()
		self.assertEqual(self.indice_1.indiceFinal(), {'a': {'d1.txt': [0, 1, 2], 'd2.txt': [0, 1], 'd3.txt': [0, 1]}, 'b': {'d1.txt': [3], 'd4.txt': [0, 1]}, 'c': {'d2.txt': [2]}})
		self.assertTrue(type(retorno_indice_final) == dict, msg="O tipo retornado pelo indice final nao é um dicionario")


	def test_numero_documentos(self):
		teste1 = self.indice_1.numero_documentos()
		teste2 = self.indice_2.numero_documentos()
		self.assertEqual(teste1, 4)
		self.assertEqual(teste2, 3)
		self.assertTrue(type(teste1) == int, msg="Não esta retornando um inteiro.")


	def test_frequencia_palavras(self):
		
		retorno_frequencia = self.indice_2.frequencia_palavra('teste', 'doc1.txt')

		self.assertEqual(self.indice_1.frequencia_palavra("A", "d1.txt"), 0)
		##Isso ocorre porque estamos transformando todas as letras da entrada em letras minusculas
		self.assertEqual(self.indice_1.frequencia_palavra("a", 'd1.txt'), 3)

		self.assertEqual(self.indice_2.frequencia_palavra("teste", "doc1.txt"), 4)

		##A função não pode ficar sem retornar algo
		self.assertIsNotNone(retorno_frequencia)

		self.assertTrue(type(retorno_frequencia) == int, msg="O tipo de retorno da função não foi inteiro")
	
		self.assertEqual(self.indice_1.frequencia_palavra(1, 'd1.txt'), 0)



	def test_preenche_pontuacao(self):
		valor_esperado = ({'a': 3, 'b': 2, 'c': 1}, {'d1.txt': {'a': 3, 'b': 1, 'c': 0}, 'd2.txt': {'a': 2, 'c': 1, 'b': 0}, 'd3.txt': {'a': 2, 'b': 0, 'c': 0}, 'd4.txt': {'b': 2, 'a': 0, 'c': 0}}, {'a': 0.28768207245178085, 'b': 0.6931471805599453, 'c': 1.3862943611198906})
		valor_obtido = self.indice_1.preenche_pontuacao()

		self.assertEqual(valor_esperado, valor_obtido)
		##Retorna uma tupla com df, tf e idf
		self.assertTrue(type(valor_obtido) == tuple, msg="Não retornou um dicionario")


	def test_calcula_pontuacao(self):
		entrada1 = "a"
		entrada2 = "b"

		entrada3 = "teste"

		self.assertEqual(self.indice_1.calcula_pontuacao(entrada1, "d1.txt"), 0.8630462173553426)
		self.assertEqual(self.indice_1.calcula_pontuacao(entrada2, "d1.txt"), 0.6931471805599453)

		self.assertTrue(type(self.indice_1.calcula_pontuacao(entrada1, "d1.txt") == float))

		self.assertEqual(self.indice_2.calcula_pontuacao(entrada3, "doc1.txt"), 1.6218604324326575)

		with self.assertRaises(TypeError, msg="Não ocorreu um erro de Atributo"):
			self.indice_1.calcula_pontuacao([])

		with self.assertRaises(KeyError, msg="Não ocorreu um 'keyrror' "):
			self.indice_1.calcula_pontuacao(dict, 'd1.txt')



	def test_indice_invertido(self):
		#Basta conferir se ele esta retornando o indice final corretamente
		retorno_indice = self.indice_1.indiceFinal()

		self.assertEqual(retorno_indice, {'a': {'d1.txt': [0, 1, 2], 'd2.txt': [0, 1], 'd3.txt': [0, 1]}, 'b': {'d1.txt': [3], 'd4.txt': [0, 1]}, 'c': {'d2.txt': [2]}})
		self.assertTrue(type(retorno_indice) == dict)


if __name__ == '__main__':
	unittest.main()