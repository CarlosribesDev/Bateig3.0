
class SlabCodeNotFound(Exception):

    def __init__(self,code,file_name):
       
        self.message = f'El codigo {code} no se encuentra en \n el archivo {file_name}'
        
        super().__init__(self.message)


class FileCantOpen(Exception):

    def __init__(self,file):

        self.message = f'No se ha podido abrir el archivo {file}'
        super().__init__(self.message)
    

class DirectoryException(Exception):

    def __init__(self,directory):

        self.message = f'No se ha podido acceder al directorio de XML\n {directory}'
        super().__init__(self.message)

class XmlNotFound(Exception):

    def __init__(self,code):

        self.message = f'No se ha encuentra el XML para {code} \n revisar primera tabla'
        super().__init__(self.message)

