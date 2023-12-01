from bson import ObjectId
import pandas as pd
from model.produtos import Produto
from conection.mongo_queries import MongoQueries

class Controller_Produto:
    def __init__(self):
        self.mongo = MongoQueries()
        
    def inserir_produto(self) -> Produto:
        self.mongo.connect()
        
        descricao_novo_produto = input("Descrição (Novo): ")
        valor_novo_produto = input("Valor (Novo): ")
        proximo_produto = self.mongo.db["produtos"].aggregate([
                                                    {
                                                        '$group': {
                                                            '_id': '$produtos', 
                                                            'proximo_produto': {
                                                                '$max': '$codigo_produto'
                                                            }
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'proximo_produto': {
                                                                '$sum': [
                                                                    '$proximo_produto', 1
                                                                ]
                                                            }, 
                                                            '_id': 0
                                                        }
                                                    }
                                                ])

        proximo_produto = int(list(proximo_produto)[0]['proximo_produto'])
        
        id_produto = self.mongo.db["produtos"].insert_one({"codigo_produto": proximo_produto, "descricao_": descricao_novo_produto, "valor": valor_novo_produto})
        df_produto = self.recupera_produto(id_produto.inserted_id)
        novo_produto = Produto(df_produto.codigo_produto.values[0], df_produto.descricao.values[0],df_produto.valor.values[0])
        print(novo_produto.to_string())
        self.mongo.close()
        return novo_produto

    def atualizar_produto(self) -> Produto:
        self.mongo.connect()

        codigo_produto = int(input("Código do Produto que irá alterar: "))        

        if not self.verifica_existencia_produto(codigo_produto):
            nova_descricao_produto = input("Descrição (Novo): ")
            valor_novo_produto = input("Valor (Novo): ")
            self.mongo.db["produtos"].update_one({"codigo_produto": codigo_produto}, {"$set": {"descricao_produto": nova_descricao_produto, "valor": valor_novo_produto}})
            df_produto = self.recupera_produto_codigo(codigo_produto)
            produto_atualizado = Produto(df_produto.codigo_produto.values[0], df_produto.descricao.values[0],df_produto.valor.values[0])
            print(produto_atualizado.to_string())
            self.mongo.close()
            return produto_atualizado
        else:
            self.mongo.close()
            print(f"O produto de código {codigo_produto} não existe.")
            return None

    def excluir_produto(self):
        self.mongo.connect()

        codigo_produto = int(input("Código do Produto que irá excluir: "))        

        if not self.verifica_existencia_produto(codigo_produto):            
            df_produto = self.recupera_produto_codigo(codigo_produto)
            self.mongo.db["produtos"].delete_one({"codigo_produto": codigo_produto})
            produto_excluido = Produto(df_produto.codigo_produto.values[0], df_produto.descricao.values[0],df_produto.valor.values[0])
            print("Produto Removido com Sucesso!")
            print(produto_excluido.to_string())
            self.mongo.close()
        else:
            self.mongo.close()
            print(f"O produto de código {codigo_produto} não existe.")

    def verifica_existencia_produto(self, codigo:int=None, external: bool = False) -> bool:
        if external:
            self.mongo.connect()

        df_produto = pd.DataFrame(self.mongo.db["produtos"].find({"codigo_produto":codigo}, {"codigo_produto": 1, "descricao": 1, "_id": 0}))

        if external:
            self.mongo.close()

        return df_produto.empty

    def recupera_produto(self, _id:ObjectId=None) -> pd.DataFrame:
        df_produto = pd.DataFrame(list(self.mongo.db["produtos"].find({"_id":_id}, {"codigo_produto": 1, "descricao": 1, "valor": 1, "_id": 0})))
        return df_produto

    def recupera_produto_codigo(self, codigo:int=None, external: bool = False) -> pd.DataFrame:
        if external:
            self.mongo.connect()

        df_produto = pd.DataFrame(list(self.mongo.db["produtos"].find({"codigo_produto":codigo}, {"codigo_produto": 1, "descricao": 1, "_id": 0})))

        if external:
            self.mongo.close()

        return df_produto