class Produto:
    def __init__(self, 
                 codigo_produto:int=None, 
                 descricao:str=None,
                 valor:float=None
                 ):
        self.set_codigo_produto(codigo_produto)
        self.set_descricao(descricao)
        self.set_valor(valor)

    def set_codigo_produto(self, codigo_produto:int):
        self.codigo_produto = codigo_produto

    def set_descricao(self, descricao:str):
        self.descricao = descricao

    def set_valor(self, valor:float):
        self.valor = valor

    def get_codigo_produto(self) -> int:
        return self.codigo_produto

    def get_descricao(self) -> str:
        return self.descricao

    def get_valor(self) -> float:
        return self.valor

    def to_string(self) -> str:
        return f"Codigo_produto: {self.get_codigo_produto()} | Descrição: {self.get_descricao()}"