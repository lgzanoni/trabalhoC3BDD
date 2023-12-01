class Raca:
    def __init__(self, 
                 nome_raca:str=None, 
                 porte:str=None, 
                 cor:str=None
                 ):
        self.set_nome_raca(nome_raca)
        self.set_porte(porte)
        self.set_cor(cor)

    def set_nome_raca(self, nome_raca:str):
        self.nome_raca = nome_raca

    def get_nome_raca(self) -> str:
        return self.nome_raca

    def set_porte(self, porte:str):
        self.porte = porte

    def get_nome_porte(self) -> str:
        return self.porte

    def set_cor(self, cor:str):
        self.cor = cor

    def get_nome_cor(self) -> str:
        return self.cor


    def to_string(self) -> str:
        return f"Raca: {self.get_nome_raca()} | Porte: {self.get_nome_porte()} | Cor: {self.get_nome_raca()}"