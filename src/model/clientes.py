class Cliente:
    def __init__(self, 
                 nome:str=None,
                 CPF:str=None, 
                 numero:int=None
                ):
        self.set_nome(nome)
        self.set_CPF(CPF)
        self.set_numero(numero)

    def set_CPF(self, CPF:str):
        self.CPF = CPF

    def set_nome(self, nome:str):
        self.nome = nome

    def set_numero(self, numero:int):
        self.numero = numero

    def get_CPF(self) -> str:
        return self.CPF

    def get_numero(self) -> int:
        return self.numero

    def get_nome(self) -> str:
        return self.nome

    def to_string(self) -> str:
        return f"Nome: {self.get_nome()} | CPF: {self.get_CPF()} | Numero: {self.get_numero()}"