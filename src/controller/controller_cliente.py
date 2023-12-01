import pandas as pd
from model.clientes import Cliente
from conection.mongo_queries import MongoQueries

class Controller_Cliente:
    def __init__(self):
        self.mongo = MongoQueries()
        
    def inserir_cliente(self) -> Cliente:

        self.mongo.connect()


        nome = input("Nome (Novo): ")

        if self.verifica_existencia_cliente(nome):

            cpf = input("CPF (Novo): ")
            numero = input("Numero (Novo): ")

            self.mongo.db["clientes"].insert_one({"nome": nome, "cpf": cpf, "numero":numero})
            df_cliente = self.recupera_cliente(cpf)
            novo_cliente = Cliente(df_cliente.nome.values[0], df_cliente.cpf.values[0], df_cliente.numero.values[0])

            print(novo_cliente.to_string())
            self.mongo.close()

            return novo_cliente
        else:
            self.mongo.close()
            print(f"O cliente ja esta cadastrado!.")
            return None

    def atualizar_cliente(self) -> Cliente:
        self.mongo.connect()

        nome = input("Nome do cliente que deseja alterar os dados: ")

        if not self.verifica_existencia_cliente(nome):
            novo_cpf = input("Cpf (Novo): ")
            novo_numero = input("Numero (Novo): ")

            self.mongo.db["clientes"].update_one({"Nome": f"{nome}"}, {"$set": {"Cpf": novo_cpf}}, {"$set": {"Numero": novo_numero}})
            df_cliente = self.recupera_cliente(nome)
            cliente_atualizado = Cliente(df_cliente.cpf.values[0], df_cliente.nome.values[0], df_cliente.numero.values[0])
            print(cliente_atualizado.to_string())
            self.mongo.close()

            return cliente_atualizado
        else:
            self.mongo.close()
            print(f"O cliente não existe!")
            return None

    def excluir_cliente(self):
        self.mongo.connect()


        nome = input("Digite o nome Cliente que deseja excluir: ")


        if not self.verifica_existencia_cliente(nome):

            df_cliente = self.recupera_cliente(nome)

            self.mongo.db["clientes"].delete_one({"Nome":f"{nome}"})

            cliente_excluido = Cliente(df_cliente.cpf.values[0], df_cliente.nome.values[0], df_cliente.numero.values[0])
            self.mongo.close()

            print("Cliente Removido com Sucesso!")
            print(cliente_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O cliente não existe!")

    def verifica_existencia_cliente(self, nome:str=None, external:bool=False) -> bool:
        if external:

            self.mongo.connect()

        df_cliente = pd.DataFrame(self.mongo.db["clientes"].find({"nome":f"{nome}"}, {"nome": 1, "cpf": 1, "numero": 1 ,"_id": 0}))

        if external:

            self.mongo.close()

        return df_cliente.empty

    def recupera_cliente(self, nome:str=None, external:bool=False) -> pd.DataFrame:
        if external:

            self.mongo.connect()

        df_cliente = pd.DataFrame(list(self.mongo.db["clientes"].find({"nome":f"{nome}"}, {"nome": 1, "cpf": 1, "numero": 1 ,"_id": 0})))
        
        if external:
            self.mongo.close()

        return df_cliente