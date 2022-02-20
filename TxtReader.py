from Slab import Slab
from Piece import Piece
from Exceptions import FileCantOpen

class TxtReader():

    def __init__(self,directory,file_name):
        self.directory = directory
        self.file_name = file_name

    


    def get_txt_date(self):
    #abre el documento del dia correspondiente en el directorio especificado
        try:
            doc = open(f'{self.directory}/{self.file_name}')
        except:
            raise FileCantOpen(self.file_name)
        slab_list = doc.read().split('START LOG TRACE:') 
        #fecha
        date=slab_list[1][1:11]

        doc.close()
        return date

    def get_txt_slabs(self):

        #lista de tablas con losas que creara a partir del documento
        slab_list = []
        #abre el documento del dia correspondiente en el directorio especificado
        try:
            doc = open(f'{self.directory}/{self.file_name}')
        except:
            raise FileCantOpen(self.file_name)

        #separa el documento por patron slabs
        txt_slab_list = doc.read().split('START LOG TRACE:')

        #comprobar cada tabla(se ignora la primera que no es una tabla)
        for txt_slab_data in txt_slab_list[1:]:

            #intenta leear una nueva tabla
            try:
                #coge la hora de la tabla 
                hour = int(txt_slab_data[12:14])
                minute = int(txt_slab_data[15:17])
                seconds = int(txt_slab_data[18:20])

                slab = Slab(hour,minute,seconds)
                #separa las piezas por patron 
                txt_pieces_list = txt_slab_data.split("_SP")

                for pieces_data in txt_pieces_list[1:]:
                    #coge los datos de la losa
                    data_list = pieces_data.split("|")               
                    #largo
                    length = int(data_list[12].strip()[:-3])/10                   
                    #ancho
                    width = int(data_list[13].strip()[:-3])/10         
                    #grueso
                    thick = int(data_list[14].strip()[:-3])/10
                    #code
                    code = data_list[15]
                   
                    #metros cuadrados
                    m2 = (length * width) / 10000

                    piece = Piece(length,width,thick,m2,code)
                    slab.pieces_list.append(piece)
              
                #si la tabla no esta vacia la añadimos a lista
                if(len(slab.pieces_list) > 0):   
                    #asignamos el codigo de la tabla
                    
                    slab.code = slab.pieces_list[0].code
                    slab_list.append(slab)
            
            except:
                
                continue

        doc.close()
        return slab_list
