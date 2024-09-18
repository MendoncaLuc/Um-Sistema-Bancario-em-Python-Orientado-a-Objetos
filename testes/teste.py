import sys
import os
import unittest
# Adiciona a pasta raiz 'Projeto' ao sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from entities.Main import Conta, ContaCorrente, PessoaFisica, Historico, Saque, Deposito 

class TesteBanco(unittest.TestCase):

    def setUp(self):
        self.cliente = PessoaFisica("12345678900", "João Silva", "01/01/1980", "Rua Exemplo, 123")
        self.conta = Conta.nova_conta(self.cliente, "12345", "001")
        self.conta_corrente = ContaCorrente(1000, "54321", "002", self.cliente, Historico(), 500, 3)
        self.cliente.adicionar_conta(self.conta_corrente) 

    def test_saldo_inicial(self):
        self.assertEqual(self.conta.saldo, 0)
        self.assertEqual(self.conta_corrente.saldo, 1000)

    def test_deposito(self):
        self.conta.depositar(500)
        self.assertEqual(self.conta.saldo, 500)

        self.conta_corrente.depositar(200)
        self.assertEqual(self.conta_corrente.saldo, 1200)

    def test_saque(self):
        self.conta.depositar(500)
        self.assertTrue(self.conta.sacar(200))
        self.assertEqual(self.conta.saldo, 300)

        self.assertFalse(self.conta.sacar(1000))  # Saque maior que saldo
        self.assertEqual(self.conta.saldo, 300)

    def test_transacoes(self):
        deposito = Deposito(1000)
        saque = Saque(200)

        self.cliente.realizar_transacao(self.conta, deposito)
        self.cliente.realizar_transacao(self.conta, saque)

        historico = self.conta._historico.exibir()
        self.assertEqual(historico[0], "Depósito de 1000 realizado.")
        self.assertEqual(historico[1], "Saque de 200 realizado.")

    def test_limite_conta_corrente(self):
        # Testa saques dentro do limite de conta corrente
        self.assertTrue(self.conta_corrente.sacar(500))
        self.assertEqual(self.conta_corrente.saldo, 500)

        # Tentando sacar além do limite
        self.assertFalse(self.conta_corrente.sacar(2000))  # Saque maior que saldo e limite
        self.assertEqual(self.conta_corrente.saldo, 500)

    def test_adicionar_conta(self):
        self.assertIn(self.conta, self.cliente._contas)
        self.assertIn(self.conta_corrente, self.cliente._contas)


if __name__ == "__main__":
    unittest.main()