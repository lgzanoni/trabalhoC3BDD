from conection.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_pets_por_protocolo(self):
        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db.pets.aggregate([{
                                                    "$lookup":{"from":"pets",
                                                               "localField":"carteirinha_pet",
                                                               "foreignField":"carteirinha_pet",
                                                               "as":"pet"
                                                              }
                                                   },
                                                   {
                                                    "$unwind": { "path": "$pet"}
                                                   },
                                                   {
                                                    "$lookup":{"from":"nome_donos",
                                                               "localField":"nome_dono",
                                                               "foreignField":"nome",
                                                               "as":"nome_dono"
                                                              }
                                                   },
                                                   {
                                                    "$unwind": { "path": "$nome_dono" }
                                                   },
                                                   {
                                                    "$lookup":{"from":"racas",
                                                               "localField":"nome_raca",
                                                               "foreignField":"nome_raca",
                                                               "as":"raca"
                                                              }
                                                   },
                                                   {
                                                    "$unwind": {"path": "$raca"}
                                                   },
                                                   {
                                                    "$lookup":{"from":'servicos',
                                                               "localField":"protocolo.codigo_servico",
                                                               "foreignField":"codigo_produto",
                                                               "as":"servico"
                                                              }
                                                   },
                                                   {
                                                    "$unwind": {"path": "$servico"}
                                                   },
                                                   {
                                                    "$project": {"carteirinha_pet": 1,
                                                                 "codigo_protocolo": "$item.codigo_protocolo",
                                                                 "nome_dono": "$nome_dono.nome",
                                                                 "raca": "$raca.nome_raca",
                                                                 "servico": "$produto.descricao_servico",
                                                                 "quantidade": "$item.quantidade",
                                                                 "valor_total": "$item.valor_total",
                                                                 "_id": 0
                                                                }
                                                   }])
        
        df_protocolos = pd.DataFrame(list(query_result))

        mongo.close()

        print(df_protocolos)
        input("Pressione Enter para Sair do Relatório de Pets")

    def get_relatorio_pets_por_raca(self):

        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db["pets"].aggregate([
                                                    {
                                                        '$group': {
                                                            '_id': '$nome_raca', 
                                                            'qtd_pets': {
                                                                '$sum': 1
                                                            }
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'nome_raca': '$_id', 
                                                            'qtd_pets': 1, 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'pets', 
                                                            'localField': 'nome_raca', 
                                                            'foreignField': 'nome_raca', 
                                                            'as': 'pet'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$pet'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'nome_raca': 1, 
                                                            'qtd_pets': 1, 
                                                            'pet': '$pet.carteirinha_pet', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'protocolos', 
                                                            'localField': 'pet', 
                                                            'foreignField': 'carteirinha_pet', 
                                                            'as': 'item'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$item'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'nome_raca': 1, 
                                                            'qtd_pets': 1, 
                                                            'quantidade': '$item.quantidade', 
                                                            'valor_total': '$item.valor_total', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$group': {
                                                            '_id': {
                                                                'nome_raca': '$nome_raca', 
                                                                'qtd_pets': '$qtd_pets'
                                                            }, 
                                                            'valor_total': '$valor_total'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$_id'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'nome_raca': '$_id.nome_raca', 
                                                            'qtd_pets': '$_id.qtd_pets', 
                                                            'valor_total': '$valor_total', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'racas', 
                                                            'localField': 'nome_raca', 
                                                            'foreignField': 'nome_raca', 
                                                            'as': 'raca'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$raca'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'porte': '$raca.porte', 
                                                            'qtd_pets': 1, 
                                                            'valor_total': 1, 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$sort': {
                                                            'porte': 1
                                                        }
                                                    }
                                                ])
        df_pets_raca = pd.DataFrame(list(query_result))

        mongo.close()

        print(df_pets_raca[["porte", "qtd_pets", "valor_total"]])
        input("Pressione Enter para Sair do Relatório de racas")

    def get_relatorio_produtos(self):

        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db["produtos"].find({}, 
                                                 {"codigo_produto": 1, 
                                                  "descricao_produto": 1, 
                                                  "_id": 0
                                                 }).sort("descricao_produto", ASCENDING)
        df_produto = pd.DataFrame(list(query_result))

        mongo.close()

        print(df_produto)
        input("Pressione Enter para Sair do Relatório de Produtos")

    def get_relatorio_nome_donos(self):

        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db["nome_donos"].find({}, 
                                                 {"nome": 1, 
                                                  "cpf": 1, 
                                                  "numero": 1, 
                                                  "_id": 0
                                                 }).sort("nome", ASCENDING)
        df_nome_dono = pd.DataFrame(list(query_result))

        mongo.close()

        print(df_nome_dono)
        input("Pressione Enter para Sair do Relatório de nome_donos")

    def get_relatorio_racas(self):

        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db["racas"].find({}, 
                                                     {"nome_raca": 1, 
                                                      "porte": 1, 
                                                      "cor": 1, 
                                                      "_id": 0
                                                     }).sort("nome_raca", ASCENDING)
        df_raca = pd.DataFrame(list(query_result))

        mongo.close()
        print(df_raca)
        input("Pressione Enter para Sair do Relatório de racas")

    def get_relatorio_pets(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db["pets"].aggregate([
                                                    {
                                                        '$lookup': {
                                                            'from': 'racas', 
                                                            'localField': 'nome_raca', 
                                                            'foreignField': 'nome_raca', 
                                                            'as': 'raca'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$raca'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'carteirinha_pet': 1, 
                                                            'nome': 1, 
                                                            'nome_raca': 1, 
                                                            'nome_dono': 1, 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'nome_donos', 
                                                            'localField': 'nome_dono', 
                                                            'foreignField': 'nome', 
                                                            'as': 'nome_dono'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$nome_dono'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'carteirinha_pet': 1, 
                                                            'nome': 1, 
                                                            'nome_raca': 1, 
                                                            'nome_dono': '$nome_dono.nome', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'protocolo', 
                                                            'localField': 'carteirinha_pet', 
                                                            'foreignField': 'carteirinha_pet', 
                                                            'as': 'protocolo'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$item', 'preserveNullAndEmptyArrays': True
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'carteirinha_pet': 1, 
                                                            'nome': 1, 
                                                            'nome_raca': 1, 
                                                            'nome_dono': 1, 
                                                            'protocolo': '$item.codigo_protocolo', 
                                                            'quantidade': '$item.quantidade', 
                                                            'valor_total': '$item.valor_total', 
                                                            'codigo_produto': '$item.codigo_produto', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'produtos', 
                                                            'localField': 'codigo_produto', 
                                                            'foreignField': 'codigo_produto', 
                                                            'as': 'produto'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$produto', 'preserveNullAndEmptyArrays': True
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'carteirinha_pet': 1, 
                                                            'nome': 1, 
                                                            'nome_raca': 1, 
                                                            'nome_dono': 1, 
                                                            'protocolo': 1, 
                                                            'quantidade': 1, 
                                                            'valor_total': 1, 
                                                            'valor_total': 1, 
                                                            'produto': '$produto.descricao_produto', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$sort': {
                                                            'nome_dono': 1,
                                                            'protocolo': 1
                                                        }
                                                    }
                                                ])
        df_pet = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_pet[["carteirinha_pet", "nome", "nome_dono", "nome_raca", "protocolo", "produto", "quantidade", "valor_total", "servico"]])
        input("Pressione Enter para Sair do Relatório de pets")
    
    def get_relatorio_protocolos(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db['protocolos'].aggregate([{
                                                            '$lookup':{'from':'produtos',
                                                                       'localField':'codigo_produto',
                                                                       'foreignField':'codigo_produto',
                                                                       'as':'produto'
                                                                      }
                                                           },
                                                           {
                                                            '$unwind':{"path": "$produto"}
                                                           },
                                                           {'$project':{'carteirinha_pet':1, 
                                                                        'codigo_protocolo':1,
                                                                    'codigo_produto':'$produto.codigo_produto',
                                                                    'descricao_produto':'$produto.descricao_produto',
                                                                    'quantidade':1,
                                                                    'valor_total':1,
                                                                    '_id':0
                                                                    }}
                                                          ])
        df_protocolo = pd.DataFrame(list(query_result))
        df_protocolo.codigo_protocolo = df_protocolo.codigo_protocolo.astype(int)
        df_protocolo.carteirinha_pet = df_protocolo.carteirinha_pet.astype(int)
        mongo.close()
        print(df_protocolo[["carteirinha_pet", "codigo_protocolo", "codigo_produto", "descricao_produto", "quantidade", "valor_total", "descricao_servico"]])
        input("Pressione Enter para Sair do Relatório de Itens de pets")