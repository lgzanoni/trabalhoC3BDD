from bson import ObjectId
import pandas as pd
from model.servicos import servico
from conection.mongo_queries import MongoQueries

class Controller_Servico:
    def __init__(self):
        self.mongo = MongoQueries()
        
    def inserir_servico(self) -> servico:
        self.mongo.connect()
        
        descricao_novo_servico = input("Descrição (Novo): ")
        valor_novo_servico = input("Valor (Novo): ")
        proximo_servico = self.mongo.db["servicos"].aggregate([
                                                    {
                                                        '$group': {
                                                            '_id': '$servicos', 
                                                            'proximo_servico': {
                                                                '$max': '$codigo_servico'
                                                            }
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'proximo_servico': {
                                                                '$sum': [
                                                                    '$proximo_servico', 1
                                                                ]
                                                            }, 
                                                            '_id': 0
                                                        }
                                                    }
                                                ])

        proximo_servico = int(list(proximo_servico)[0]['proximo_servico'])
        
        id_servico = self.mongo.db["servicos"].insert_one({"codigo_servico": proximo_servico, "descricao_": descricao_novo_servico, "valor": valor_novo_servico})
        df_servico = self.recupera_servico(id_servico.inserted_id)
        novo_servico = servico(df_servico.codigo_servico.values[0], df_servico.descricao.values[0],df_servico.valor.values[0])
        print(novo_servico.to_string())
        self.mongo.close()
        return novo_servico

    def atualizar_servico(self) -> servico:
        self.mongo.connect()

        codigo_servico = int(input("Código do servico que irá alterar: "))        

        if not self.verifica_existencia_servico(codigo_servico):
            nova_descricao_servico = input("Descrição (Novo): ")
            valor_novo_servico = input("Valor (Novo): ")
            self.mongo.db["servicos"].update_one({"codigo_servico": codigo_servico}, {"$set": {"descricao_servico": nova_descricao_servico, "valor": valor_novo_servico}})
            df_servico = self.recupera_servico_codigo(codigo_servico)
            servico_atualizado = servico(df_servico.codigo_servico.values[0], df_servico.descricao.values[0],df_servico.valor.values[0])
            print(servico_atualizado.to_string())
            self.mongo.close()
            return servico_atualizado
        else:
            self.mongo.close()
            print(f"O servico de código {codigo_servico} não existe.")
            return None

    def excluir_servico(self):
        self.mongo.connect()

        codigo_servico = int(input("Código do servico que irá excluir: "))        

        if not self.verifica_existencia_servico(codigo_servico):            
            df_servico = self.recupera_servico_codigo(codigo_servico)
            self.mongo.db["servicos"].delete_one({"codigo_servico": codigo_servico})
            servico_excluido = servico(df_servico.codigo_servico.values[0], df_servico.descricao.values[0],df_servico.valor.values[0])
            print("servico Removido com Sucesso!")
            print(servico_excluido.to_string())
            self.mongo.close()
        else:
            self.mongo.close()
            print(f"O servico de código {codigo_servico} não existe.")

    def verifica_existencia_servico(self, codigo:int=None, external: bool = False) -> bool:
        if external:
            self.mongo.connect()

        df_servico = pd.DataFrame(self.mongo.db["servicos"].find({"codigo_servico":codigo}, {"codigo_servico": 1, "descricao": 1, "_id": 0}))

        if external:
            self.mongo.close()

        return df_servico.empty

    def recupera_servico(self, _id:ObjectId=None) -> pd.DataFrame:
        df_servico = pd.DataFrame(list(self.mongo.db["servicos"].find({"_id":_id}, {"codigo_servico": 1, "descricao": 1, "valor": 1, "_id": 0})))
        return df_servico

    def recupera_servico_codigo(self, codigo:int=None, external: bool = False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_servico = pd.DataFrame(list(self.mongo.db["servicos"].find({"codigo_servico":codigo}, {"codigo_servico": 1, "descricao": 1, "_id": 0})))

        if external:
            self.mongo.close()

        return df_servico