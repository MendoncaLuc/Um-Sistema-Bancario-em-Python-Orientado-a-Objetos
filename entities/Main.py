from abc import ABC, abstractmethod

class Conta:

    def __init__(self, saldo, numero, agencia, cliente, historico):
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = historico

    @property
    def saldo(self):
        return self._saldo

    def sacar(self, valor):
        if valor > 0 and self._saldo >= valor:
            self._saldo -= valor
            print(f"Saque de {valor} realizado com sucesso.")
            return True
        else:
            print("Saque não realizado. Saldo insuficiente.")
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Depósito de {valor} realizado com sucesso.")
            return True
        else:
            print("Depósito não realizado. Valor inválido.")
            return False

    @classmethod
    def nova_conta(cls, cliente, numero, agencia):
        nova_conta = cls(0, numero, agencia, cliente, Historico())
        cliente.adicionar_conta(nova_conta)
        return nova_conta


class ContaCorrente(Conta):

    def __init__(self, saldo, numero, agencia, cliente, historico, limite, limite_saques):
        super().__init__(saldo, numero, agencia, cliente, historico)
        self._limite = limite
        self._limite_saques = limite_saques


class Transacao(ABC):

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):

    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        if conta.sacar(self._valor):
            return f"Saque de {self._valor} realizado."
        else:
            return "Saque não realizado."


class Deposito(Transacao):

    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        if conta.depositar(self._valor):
            return f"Depósito de {self._valor} realizado."
        else:
            return "Depósito não realizado."


class Historico:

    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

    def exibir(self):
        return self._transacoes


class Cliente:

    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        resultado = transacao.registrar(conta)
        conta._historico.adicionar_transacao(resultado)

    def adicionar_conta(self, conta):
        self._contas.append(conta)
        print("Conta adicionada ao cliente.")


class PessoaFisica(Cliente):

    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
