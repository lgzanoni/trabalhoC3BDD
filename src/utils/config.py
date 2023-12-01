MENU_PRINCIPAL = """Menu Principal
1 - Relatórios
2 - Inserir Registros
3 - Atualizar Registros
4 - Remover Registros
5 - Sair
"""

MENU_RELATORIOS = """Relatórios
1 - Relatório de Pets por Fornecedores
2 - Relatório de Pets
3 - Relatório de Produtos
4 - Relatório de Servicos
4 - Relatório de Clientes
5 - Relatório de Racas
6 - Relatório de Protocolos
0 - Sair
"""

MENU_ENTIDADES = """Entidades
1 - PETS
2 - CLIENTES
3 - RACAS
4 - PROTOCOLO
5 - SERVICOS
6 - PRODUTOS
"""

def query_count(collection_name):
   from conection.mongo_queries import MongoQueries
   import pandas as pd

   mongo = MongoQueries()
   mongo.connect()

   my_collection = mongo.db[collection_name]
   total_documentos = my_collection.count_documents({})
   mongo.close()
   df = pd.DataFrame({f"total_{collection_name}": [total_documentos]})
   return df

def clear_console(wait_time:int=3):
    import os
    from time import sleep
    sleep(wait_time)
    os.system("clear")