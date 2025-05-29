
import textwrap
from datetime import datetime

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

class Conta:
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    def __init__(self, usuario):
        self.saldo = 0
        self.limite = 500
        self.extrato = []
        self.numero_saques = 0
        self.usuario = usuario
        self.numero_conta = Conta.gerar_numero_conta()

    @staticmethod
    def gerar_numero_conta():
        if not hasattr(Conta, "_contador"):
            Conta._contador = 0
        Conta._contador += 1
        return Conta._contador

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato.append((datetime.now(), f"Depósito: R$ {valor:.2f}"))
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def sacar(self, valor):
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= Conta.LIMITE_SAQUES

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        elif valor > 0:
            self.saldo -= valor
            self.extrato.append((datetime.now(), f"Saque: R$ {valor:.2f}"))
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        if not self.extrato:
            print("Não foram realizadas movimentações.")
        else:
            for data, transacao in self.extrato:
                print(f"{data.strftime('%d/%m/%Y %H:%M:%S')} - {transacao}")
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print("==========================================")

class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []

    def criar_usuario(self):
        cpf = input("Informe o CPF (somente número): ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            print("\n@@@ Já existe usuário com esse CPF! @@@")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        self.usuarios.append(Usuario(nome, data_nascimento, cpf, endereco))
        print("=== Usuário criado com sucesso! ===")

    def filtrar_usuario(self, cpf):
        usuarios_filtrados = [usuario for usuario in self.usuarios if usuario.cpf == cpf]
        return usuarios_filtrados[0] if usuarios_filtrados else None

    def criar_conta(self):
        cpf = input("Informe o CPF do usuário: ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            conta = Conta(usuario)
            self.contas.append(conta)
            print("\n=== Conta criada com sucesso! ===")
        else:
            print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

    def listar_contas(self):
        for conta in self.contas:
            linha = f"""\
                Agência: {conta.AGENCIA}
                C/C: {conta.numero_conta}
                Titular: {conta.usuario.nome}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def main():
    banco = Banco()

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in banco.contas if c.numero_conta == numero_conta), None)

            if conta:
                conta.depositar(valor)
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in banco.contas if c.numero_conta == numero_conta), None)

            if conta:
                conta.sacar(valor)
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "e":
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in banco.contas if c.numero_conta == numero_conta), None)

            if conta:
                conta.exibir_extrato()
            else:
                print("\n@@@ Conta não encontrada! @@@")

        elif opcao == "nu":
            banco.criar_usuario()

        elif opcao == "nc":
            banco.criar_conta()

        elif opcao == "lc":
            banco.listar_contas()

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

if __name__ == "__main__":
    main()
