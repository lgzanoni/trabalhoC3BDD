from model.clientes import Cliente
from model.raca import Raca

class Pet:
    def __init__(self, 
                 carteirinha_pet:int=None,
                 nome:str=None,
                 cliente:Cliente= None,
                 idade:int= None,
                 raca:Raca=None
                 ):
        self.set_carteirinha_pet(carteirinha_pet)
        self.set_nome(nome)
        self.set_cliente(cliente)
        self.set_idade(idade)
        self.set_raca(raca)


    def set_carteirinha_pet(self, carteirinha_pet:int):
        self.carteirinha_pet = carteirinha_pet

    def set_nome(self, nome:str):
        self.nome = nome

    def set_cliente(self, cliente:Cliente):
        self.cliente = cliente

    def set_idade(self, idade:int):
        self.idade = idade

    def set_raca(self, raca:Raca):
        self.raca = raca

    def get_carteirinha_pet(self) -> int:
        return self.carteirinha_pet

    def get_nome(self) -> str:
        return self.nome

    def get_cliente(self) -> Cliente:
        return self.cliente

    def get_idade(self) -> int:
        return self.idade

    def get_raca(self) -> Raca:
        return self.raca

    def to_string(self) -> str:
        return f"Pet: {self.get_carteirinha_pet()} | Nome: {self.get_nome()} | Dono: {self.get_cliente().get_nome()} | Idade: {self.get_idade()} | Raca: {self.get_raca().get_nome_raca()}" 