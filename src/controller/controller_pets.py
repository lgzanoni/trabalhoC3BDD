import pandas as pd
from bson import ObjectId

from reports.relatorios import Relatorio

from model.pet import Pet
from model.clientes import Cliente
from model.raca import Raca

from controller.controller_cliente import Controller_Cliente
from controller.controller_racas import Controller_Raca

from conection.mongo_queries import MongoQueries
from datetime import datetime

class Controller_Pet:
    def __init__(self):
        self.ctrl_cliente = Controller_Cliente()
        self.ctrl_raca = Controller_Raca()
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()
        
    def inserir_pet(self) -> Pet:
        self.mongo.connect()
        
        self.relatorio.get_relatorio_clientes()
        nome = str(input("Digite o nome do Dono: "))
        cliente = self.valida_cliente(nome)
        if cliente == None:
            return None

        self.relatorio.get_relatorio_racaes()
        nome_raca = str(input("Informe a raca do Pet: "))
        raca = self.valida_raca(nome_raca)
        if raca == None:
            return None

        nome_pet = input("Digite o nome do Pet: ")

        idade = input("Digite a idade do Pet: ")

        proximo_pet = self.mongo.db["pets"].aggregate([
                                                            {
                                                                '$group': {
                                                                    '_id': '$pets', 
                                                                    'proximo_pet': {
                                                                        '$max': '$carteirinha_pet'
                                                                    }
                                                                }
                                                            }, {
                                                                '$project': {
                                                                    'proximo_pet': {
                                                                        '$sum': [
                                                                            '$proximo_pet', 1
                                                                        ]
                                                                    }, 
                                                                    '_id': 0
                                                                }
                                                            }
                                                        ])

        proximo_pet = int(list(proximo_pet)[0]['proximo_pet'])
        data = dict(carteirinha_pet=proximo_pet, nome=nome_pet, idade=idade , nome_dono=cliente.get_nome(), nome_raca=raca.get_nome_raca())
        id_pet = self.mongo.db["pets"].insert_one(data)
        df_pet = self.recupera_pet(id_pet.inserted_id)
        novo_pet = Pet(df_pet.carteirinha_pet.values[0], df_pet.nome.values[0], df_pet.idade.values[0] ,cliente, raca)
        print(novo_pet.to_string())
        self.mongo.close()
        return novo_pet

    def atualizar_pet(self) -> Pet:
        self.mongo.connect()

        carteirinha_pet = int(input("Digite o numero de carteirinha que irá alterar: "))        

        if not self.verifica_existencia_pet(carteirinha_pet):

            self.relatorio.get_relatorio_clientes()
            nome = str(input("Digite o nome do Dono: "))
            cliente = self.valida_cliente(nome)
            if cliente == None:
                return None

            self.relatorio.get_relatorio_racaes()
            nome_raca = str(input("Informe a raca do Pet: "))
            raca = self.valida_raca(nome_raca)
            if raca == None:
                return None

            nome_pet = input("Digite o nome do Pet: ")

            idade = input("Digite a idade do Pet: ")

            self.mongo.db["pets"].update_one({"carteirinha_pet": carteirinha_pet}, 
                                                {"$set": {"nome_raca": f'{raca.get_nome_raca()}',
                                                          "nome_dono":  f'{cliente.get_nome()}',
                                                          "nome": nome_pet,
                                                          "idade": idade
                                                          }
                                                })
            df_pet = self.recupera_pet_codigo(carteirinha_pet)
            pet_atualizado = Pet(df_pet.carteirinha_pet.values[0], df_pet.nome.values[0], df_pet.idade.values[0] ,cliente, raca)
            print(pet_atualizado.to_string())
            self.mongo.close()
            return pet_atualizado
        else:
            self.mongo.close()
            print(f"Nao existe um animal vinculado com a carteirinha: {carteirinha_pet}")
            return None

    def excluir_pet(self):
        self.mongo.connect()

        carteirinha_pet = int(input("Carteirinha do Pet que irá excluir: "))        

        if not self.verifica_existencia_pet(carteirinha_pet):            
            df_pet = self.recupera_pet_codigo(carteirinha_pet)
            cliente = self.valida_cliente(df_pet.nome_dono.values[0])
            raca = self.valida_raca(df_pet.nome_raca.values[0])
            
            opcao_excluir = input(f"Tem certeza que deseja excluir o pet {carteirinha_pet} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                print("Atenção, caso o pet possua protocolos, também serão excluídos!")
                opcao_excluir = input(f"Tem certeza que deseja excluir o pet {carteirinha_pet} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    self.mongo.db["protocolos_pet"].delete_one({"carteirinha_pet": carteirinha_pet})
                    print("Protocolos relacionados ao pet removidos com sucesso!")
                    self.mongo.db["pets"].delete_one({"carteirinha_pet": carteirinha_pet})
                    pet_excluido = Pet(df_pet.carteirinha_pet.values[0], df_pet.nome.values[0], df_pet.idade.values[0] ,cliente, raca)
                    self.mongo.close()
                    print("Pet Removido com Sucesso!")
                    print(pet_excluido.to_string())
        else:
            self.mongo.close()
            print(f"Nao existe um animal vinculado com a carteirinha: {carteirinha_pet}")

    def verifica_existencia_pet(self, carteirinha_pet:int=None, external: bool = False) -> bool:
        df_pet = self.recupera_pet_codigo(carteirinha_pet=carteirinha_pet, external=external)
        return df_pet.empty

    def recupera_pet(self, _id:ObjectId=None) -> bool:
        df_pet = pd.DataFrame(list(self.mongo.db["pets"].find({"_id":_id}, {"carteirinha_pet": 1, "nome": 1, "idade": 1 , "nome_dono": 1, "nome_raca": 1, "_id": 0})))
        return df_pet

    def recupera_pet_codigo(self, carteirinha_pet:int=None, external: bool = False) -> bool:
        if external:
            self.mongo.connect()

        df_pet = pd.DataFrame(list(self.mongo.db["pets"].find({"codigo_pet": carteirinha_pet}, {"carteirinha_pet": 1, "nome": 1, "idade": 1 , "nome_dono": 1, "nome_raca": 1, "_id": 0})))

        if external:
            self.mongo.close()

        return df_pet

    def valida_cliente(self, nome:str=None) -> Cliente:
        if self.ctrl_cliente.verifica_existencia_cliente(nome=nome, external=True):
            print(f"O Cliente {nome} informado não existe na base.")
            return None
        else:
            df_cliente = self.ctrl_cliente.recupera_cliente(nome=nome, external=True)
            cliente = Cliente(df_cliente.nome.values[0], df_cliente.cpf.values[0], df_cliente.numero.values[0])
            return cliente

    def valida_raca(self, raca:str=None) -> Raca:
        if self.ctrl_raca.verifica_existencia_raca(raca, external=True):
            print(f"A raca {raca} informada não existe na base.")
            return None
        else:
            df_raca = self.ctrl_raca.recupera_raca(raca, external=True)
            raca = Raca(df_raca.nome_raca.values[0], df_raca.porte.values[0], df_raca.cor.values[0])
            return raca