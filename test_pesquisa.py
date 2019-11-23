import pesquisa
import re
import unicodedata
import unittest
import math 
import numpy as np

class TestConsulta(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		pass

	@classmethod
	def tearDownClass(cls):
		pass


	def setUp(self):
		self.consulta_1 = pesquisa.Consulta(['d1.txt', 'd2.txt', 'd3.txt', 'd4.txt'])
		self.consulta_2 = pesquisa.Consulta(['doc1.txt', 'doc2.txt', 'doc3.txt'])


	def tearDown(self):
		pass


	def test_consulta_uma_palavra(self):


		self.assertEqual(self.consulta_1.consulta_uma_palavra("teste"), [])
		self.assertEqual(self.consulta_1.consulta_uma_palavra("a"), ['d1.txt', 'd2.txt', 'd3.txt'])


		self.assertTrue(type(self.consulta_1.consulta_uma_palavra("a")) == list)

		with self.assertRaises(TypeError, msg="Não foi passado uma string"):
			self.consulta_1.consulta_uma_palavra(1)


	def test_consulta_simples(self):
		
		self.assertEqual(self.consulta_2.consulta_simples("teste teste"), ['doc2.txt', 'doc1.txt'])


		self.assertTrue(type(self.consulta_1.consulta_simples("a")) == list)

		with self.assertRaises(TypeError, msg="Não foi passado uma string"):
			self.assertEqual(self.consulta_2.consulta_simples(0))
			

	def test_produto_interno(self):
		vetor1 = np.array([1, 2, 3])
		vetor2 = np.array([1, 5, 7])
		vetor3 = np.zeros(3)

		self.assertEqual(self.consulta_1.produto_interno(vetor1, vetor2), 32)
		self.assertEqual(self.consulta_1.produto_interno(vetor3, vetor1), 0)



	def resultadosConsultas(self):
		##Verificando se ela esta retornando os resultados de forma esperada

		teste = self.resultadosConsultas(['doc1.txt', 'doc2.txt'], ['doc2.txt', 'doc1.txt'])

if __name__ == '__main__':
	unittest.main()