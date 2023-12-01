from model.pet import Pet
from model.produtos import Produto
from model.servicos import Servico

class Protocolo:
    def __init__(self, 
                 codigo_protocolo:int=None,
                 quantidade:float=None,
                 valor_total:float=None,
                 pet:Pet=None,
                 produto:Produto=None,
                 servico:Servico=None
                 ):
        self.set_codigo_protocolo(codigo_protocolo)
        self.set_quantidade(quantidade)
        self.set_valor_total(valor_total)
        self.set_pet(pet)
        self.set_produto(produto)
        self.set_servico(servico)

    def set_codigo_protocolo(self, codigo_protocolo:int):
        self.codigo_protocolo = codigo_protocolo

    def set_quantidade(self, quantidade:float):
        self.quantidade = quantidade

    def set_valor_total(self, valor_total:float):
        self.valor_total = valor_total
    
    def set_pet(self, pet:Pet):
        self.pet = pet

    def set_produto(self, produto:Produto):
        self.produto = produto

    def set_servico(self, servico:Servico):
        self.servico = servico

    def get_codigo_protocolo(self) -> int:
        return self.codigo_protocolo

    def get_quantidade(self) -> float:
        return self.quantidade

    def get_valor_total(self) -> float:
        return self.valor_total
    
    def get_pet(self) -> Pet:
        return self.pet

    def get_produto(self) -> Produto:
        return self.produto

    def get_servico(self) -> Servico:
        return self.servico

    def to_string(self):
        return f"Codigo de Protocolo: {self.get_codigo_protocolo()} | Quantidade de servicos: {self.get_quantidade()} | Vlr. Total: {self.get_produto().get_valor() + self.get_servico().get_valor()} | Produtos: {self.get_produto().get_descricao()} | Servicos: {self.get_servico().get_descricao()}"