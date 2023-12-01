import pandas as pd
from model.raca import Raca
from conection.mongo_queries import MongoQueries

class Controller_Raca:
    def __init__(self):
        self.mongo = MongoQueries()
        
    def inserir_raca(self) -> Raca:
        self.mongo.connect()

        nome_raca = input("Nome da Raca (Novo): ")

        if self.verifica_existencia_raca(nome_raca):
            porte = input("Porte (Novo): ")
            cor = input("Cor (Novo): ")
            self.mongo.db["racas"].insert_one({"nome_raca": nome_raca, "porte": porte, "cor": cor})
            df_raca = self.recupera_raca(nome_raca)
            novo_raca = Raca(df_raca.nome_raca.values[0], df_raca.porte.values[0], df_raca.cor.values[0])
            print(novo_raca.to_string())
            self.mongo.close()
            return novo_raca
        else:
            self.mongo.close()
            print(f"Essa raca já está cadastrado.")
            return None

    def atualizar_raca(self) -> Raca:
        self.mongo.connect()

        nome_raca = int(input("Digite a raca que deseja alterar: "))

        if not self.verifica_existencia_raca(nome_raca):
            porte = input("Porte (Novo): ")
            cor = input("Cor (Novo): ")            
            self.mongo.db["racas"].update_one({"nome_raca": nome_raca, "porte": porte, "cor": cor})
            df_raca = self.recupera_raca(nome_raca)
            raca_atualizado = Raca(df_raca.nome_raca.values[0], df_raca.porte.values[0], df_raca.cor.values[0])
            print(raca_atualizado.to_string())
            self.mongo.close()
            return raca_atualizado
        else:
            self.mongo.close()
            print(f"A raca solicitada nao existe no sistema!")
            return None

    def excluir_raca(self):
        self.mongo.connect()

        nome_raca = int(input("Digite o nome da raca que irá excluir: "))        

        if not self.verifica_existencia_raca(nome_raca):            
            df_raca = self.recupera_raca(nome_raca)
            self.mongo.db["racas"].delete_one({"nome_raca":f"{nome_raca}"})
            raca_excluido = Raca(df_raca.nome_raca.values[0], df_raca.porte.values[0], df_raca.cor.values[0])
            self.mongo.close()
            print("Raca Removida com Sucesso!")
            print(raca_excluido.to_string())
        else:
            self.mongo.close()
            print(f"A raca solicitada nao existe no sistema!")

    def verifica_existencia_raca(self, nome_raca:str=None, external:bool=False) -> bool:
        if external:
            self.mongo.connect()

        df_raca = pd.DataFrame(self.mongo.db["racas"].find({"nome_raca":f"{nome_raca}"}, {"nome_raca": 1, "porte": 1, "cor": 1, "_id": 0}))

        if external:
            self.mongo.close()

        return df_raca.empty

    def recupera_raca(self, nome_raca:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_cliente = pd.DataFrame(list(self.mongo.db["racas"].find({"nome_raca":f"{nome_raca}"}, {"nome_raca": 1, "porte": 1, "cor": 1, "_id": 0})))

        if external:
            self.mongo.close()

        return df_cliente