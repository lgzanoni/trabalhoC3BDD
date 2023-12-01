from utils import config

class SplashScreen:

    def __init__(self):
        self.created_by = "Luis Gustavo Zanoni Bermudes"
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2023/2"

    def get_documents_count(self, collection_name):
        df = config.query_count(collection_name=collection_name)
        return df[f"total_{collection_name}"].values[0]

    def get_updated_screen(self):
        return f"""
        ########################################################
        #                   SISTEMA DE PETSHOP                     
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - PETS:         {str(self.get_documents_count(collection_name="pets")).rjust(5)}
        #      2 - CLIENTES:         {str(self.get_documents_count(collection_name="clientes")).rjust(5)}
        #      3 - RACAS:     {str(self.get_documents_count(collection_name="racas")).rjust(5)}
        #      4 - PROTOCOLOS:          {str(self.get_documents_count(collection_name="protocolos")).rjust(5)}
        #      5 - SERVICOS: {str(self.get_documents_count(collection_name="servicos")).rjust(5)}
        #      6 - PRODUTOS: {str(self.get_documents_count(collection_name="produtos")).rjust(5)}
        #
        #  CRIADO POR: {self.created_by}
        #
        #  PROFESSOR:  {self.professor}
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        ########################################################
        """