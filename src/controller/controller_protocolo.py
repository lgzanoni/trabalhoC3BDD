import pandas as pd
from bson import ObjectId

from reports.relatorios import Relatorio

from model.protocolo import Protocolo
from model.produtos import Produto
from model.pet import Pet

from controller.controller_produto import Controller_Produto
from controller.controller_pets import Controller_Pet

from conection.mongo_queries import MongoQueries

class Controller_Protocolo:
    def __init__(self):
        self.ctrl_produto = Controller_Produto()
        self.ctrl_pet = Controller_Pet()
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()
        
    def inserir_protocolo(self) -> Protocolo:

        self.mongo.connect()
        

        self.relatorio.get_relatorio_pets()
        carteirinha_pet = int(str(input("Digite o número de carteirinha do Pet: ")))
        pet = self.valida_pet(carteirinha_pet)
        if pet == None:
            return None

        self.relatorio.get_relatorio_produtos()
        codigo_produto = int(str(input("Digite o código do Produto: ")))
        produto = self.valida_produto(codigo_produto)
        if produto == None:
            return None

        self.relatorio.get_relatorio_servicos()
        codigo_servico = int(str(input("Digite o código do Servico: ")))
        servico = self.valida_produto(codigo_servico)
        if servico == None:
            return None


        quantidade = float(input(f"Informe a quantidade servicos/itens do protocolo: "))

        valor_total = float(input(f"Informe o valor total do protocolo: "))

        proximo_protocolo = self.mongo.db["protocolos"].aggregate([
                                                    {
                                                        '$group': {
                                                            '_id': '$protocolos', 
                                                            'proximo_protocolo': {
                                                                '$max': '$codigo_protocolo'
                                                            }
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'proximo_protocolo': {
                                                                '$sum': [
                                                                    '$proximo_protocolo', 1
                                                                ]
                                                            }, 
                                                            '_id': 0
                                                        }
                                                    }
                                                ])

        proximo_protocolo = int(list(proximo_protocolo)[0]['proximo_protocolo'])

        data = dict(codigo_protocolo=proximo_protocolo, valor_total=valor_total, quantidade=quantidade, carteirinha_pet=int(pet.get_carteirinha_pet()), codigo_produto=int(produto.get_codigo()))

        id_protocolo = self.mongo.db["protocolos"].insert_one(data)

        df_protocolo = self.recupera_protocolo(id_protocolo.inserted_id)

        novo_protocolo = Protocolo(df_protocolo.codigo_protocolo.values[0], df_protocolo.quantidade.values[0], df_protocolo.valor_total.values[0], pet, produto)

        print(novo_protocolo.to_string())
        self.mongo.close()

        return novo_protocolo

    def atualizar_protocolo(self) -> Protocolo:

        self.mongo.connect()


        codigo_protocolo = int(input("Código do Protocolo que irá alterar: "))        


        if not self.verifica_existencia_protocolo(codigo_protocolo):

            self.relatorio.get_relatorio_pets()
            carteirinha_pet = int(str(input("Digite o número do Pet: ")))
            pet = self.valida_pet(carteirinha_pet)
            if pet == None:
                return None

            self.relatorio.get_relatorio_produtos()
            codigo_produto = int(str(input("Digite o código do Produto: ")))
            produto = self.valida_produto(codigo_produto)
            if produto == None:
                return None


            quantidade = float(input(f"Informe a quantidade de itens do produto {produto.get_descricao()}: "))

            valor_total = float(input(f"Informe o valor unitário do produto {produto.get_descricao()}: "))


            self.mongo.db["itens_pet"].update_one({"codigo_protocolo": codigo_protocolo},
                                                     {"$set": {"quantidade": quantidade,
                                                               "valor_total":  valor_total,
                                                               "carteirinha_pet": int(pet.get_carteirinha_pet()),
                                                               "codigo_produto": int(produto.get_codigo())
                                                          }
                                                     })

            df_protocolo = self.recupera_protocolo_codigo(codigo_protocolo)

            protocolo_atualizado = Protocolo(df_protocolo.codigo_protocolo.values[0], df_protocolo.quantidade.values[0], df_protocolo.valor_total.values[0], pet, produto)
            print(protocolo_atualizado.to_string())
            self.mongo.close()
            return protocolo_atualizado
        else:
            self.mongo.close()
            print(f"O código {codigo_protocolo} não existe.")
            return None

    def excluir_protocolo(self):

        self.mongo.connect()


        codigo_protocolo = int(input("Código do Item de Pet que irá excluir: "))        


        if not self.verifica_existencia_protocolo(codigo_protocolo):            

            df_protocolo = self.recupera_protocolo_codigo(codigo_protocolo)
            pet = self.valida_pet(int(df_protocolo.carteirinha_pet.values[0]))
            produto = self.valida_produto(int(df_protocolo.codigo_produto.values[0]))
            
            opcao_excluir = input(f"Tem certeza que deseja excluir o item de pet {codigo_protocolo} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                self.mongo.db["itens_pet"].delete_one({"codigo_protocolo": codigo_protocolo})
                protocolo_excluido = Protocolo(df_protocolo.codigo_protocolo.values[0], 
                                                  df_protocolo.quantidade.values[0], 
                                                  df_protocolo.valor_total.values[0], 
                                                  pet, 
                                                  produto)
                self.mongo.close()

                print("Item do Pet Removido com Sucesso!")
                print(protocolo_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O código {codigo_protocolo} não existe.")

    def verifica_existencia_protocolo(self, codigo:int=None) -> bool:

        df_pet = self.recupera_protocolo_codigo(codigo=codigo)
        return df_pet.empty

    def recupera_protocolo(self, _id:ObjectId=None) -> bool:

        df_pet = pd.DataFrame(list(self.mongo.db["itens_pet"].find({"_id": _id}, {"codigo_protocolo":1, "quantidade": 1, "valor_total": 1, "carteirinha_pet": 1, "codigo_produto": 1, "_id": 0})))
        return df_pet

    def recupera_protocolo_codigo(self, codigo:int=None) -> bool:

        df_pet = pd.DataFrame(list(self.mongo.db["itens_pet"].find({"codigo_protocolo": codigo}, {"codigo_protocolo":1, 
                                                                                                          "quantidade": 1, 
                                                                                                          "valor_total": 1, 
                                                                                                          "carteirinha_pet": 1, 
                                                                                                          "codigo_produto": 1, 
                                                                                                          "_id": 0})))
        return df_pet

    def valida_pet(self, carteirinha_pet:int=None) -> Pet:
        if self.ctrl_pet.verifica_existencia_pet(carteirinha_pet, external=True):
            print(f"O pet {carteirinha_pet} informado não existe na base.")
            return None
        else:

            df_pet = self.ctrl_pet.recupera_pet_codigo(carteirinha_pet, external=True)
            cliente = self.ctrl_pet.valida_cliente(df_pet.cpf.values[0])
            fornecedor = self.ctrl_pet.valida_fornecedor(df_pet.cnpj.values[0])
            pet = Pet(df_pet.carteirinha_pet.values[0], df_pet.data_pet.values[0], cliente, fornecedor)
            return pet

    def valida_produto(self, codigo_produto:int=None) -> Produto:
        if self.ctrl_produto.verifica_existencia_produto(codigo_produto, external=True):
            print(f"O produto {codigo_produto} informado não existe na base.")
            return None
        else:

            df_produto = self.ctrl_produto.recupera_produto_codigo(codigo_produto, external=True)

            produto = Produto(df_produto.codigo_produto.values[0], df_produto.descricao_produto.values[0])
            return produto