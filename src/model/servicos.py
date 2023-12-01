class Servico:
    def __init__(self, 
                 codigo_servico:int=None, 
                 descricao:str=None,
                 valor:float=None
                 ):
        self.set_codigo_servico(codigo_servico)
        self.set_descricao(descricao)
        self.set_valor(valor)

    def set_codigo_servico(self, codigo_servico:int):
        self.codigo_servico = codigo_servico

    def set_descricao(self, descricao:str):
        self.descricao = descricao

    def set_valor(self, valor:float):
        self.valor = valor

    def get_codigo_servico(self) -> int:
        return self.codigo_servico

    def get_descricao(self) -> str:
        return self.descricao

    def get_valor(self) -> float:
        return self.valor

    def to_string(self) -> str:
        return f"Codigo_servico: {self.get_codigo_servico()} | Descrição: {self.get_descricao()}"