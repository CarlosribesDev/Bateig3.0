
from operator import contains
import Values
import os
from Measure import Measure
from MeasureSlab import MeasureSlab
from TxtReader import TxtReader
from XmlReader import XmlReader
from Exceptions import SlabCodeNotFound

class Report():
    
    def __init__(self,name,start_hour,start_minute,end_hour,end_minute,first_slab,last_slab):

        self.name = name

        self.pieces_list = []
        self.slab_list = []
        self.materials_list = []
        self.measures_list = []
        self.measures_slab_list = []
        self.total_m2 = 0
        self.total_slab_m2 = 0

        self.start_hour = start_hour
        self.start_minute = start_minute

        self.end_hour = end_hour
        self.end_minute = end_minute

        self.first_slab = first_slab
        self.last_slab = last_slab
 
    #coge toda la informacion de archivo txt
    def get_data(self,folder_summary,folder_materials,day):
         
        day_file_name = Values.WEEK_DAYS_FILE_NAMES[day]
        txt_reader = TxtReader(folder_summary,day_file_name)
        #lectura de los ficheros de texto
        try:
            txt_slab_list = txt_reader.get_txt_slabs()
            self.date = txt_reader.get_txt_date()
        except Exception as e:
            raise e
        
        #comprobar que el primero codigo existe
        if(not self.contains_first_code(txt_slab_list)): raise SlabCodeNotFound(self.first_slab,day_file_name)
        
        #añadir slabs que pertenecen al parte
        self.add_slabs(txt_slab_list) 
        #leer dimesiones y material de cada tabla
        self.get_slabs_data(folder_materials)
        #recuento total
        self.get_total()
        #agrupar las losas por medidas
        self.group_by_measures()

        
    def contains_first_code(self,slab_list):
        
        contains_code = False

        for slab in slab_list:
           if(slab.code == self.first_slab): contains_code = True 
        
        return contains_code

    def add_slabs(self,slab_list):

        for slab in slab_list:
           
            if(slab.code >= self.first_slab and slab.code <= self.last_slab):

                self.slab_list.append(slab)

        #recuento de piezas
        for slab in self.slab_list:
            
            for piece in slab.pieces_list:
                
                self.pieces_list.append(piece)
                self.total_m2 += piece.m2
    #recuento total de tablas y losas,añadir material y m2 de la tabla
    def get_slabs_data(self,path):
        
        xml_reader = XmlReader(path,self.first_slab)

        #buscamos el primer codigo
        try:
            first_code = xml_reader.get_first_xml_code()
        except Exception as e:
            raise e

        #coge los datos de todas las tablas
        try:
            xml_reader.get_all_slab_data(self.slab_list,first_code)
        except Exception as e:
            raise e  

            
    def get_total(self):

        self.total_slabs = len(self.slab_list)
        self.total_pieces = len(self.pieces_list)
        if(len(self.slab_list) > 1) : self.avegare_time()
        
        
        

    #agrupa todas las losas en medias
    def group_by_measures(self):

        #losas
        for piece in self.pieces_list:
            
            measure = Measure(piece,self)
          
            if( not measure.measure_exist()):
                
                self.measures_list.append(measure)
        
        
        #tablas
        for slab in self.slab_list:

            measure = MeasureSlab(slab,self)

            if(not measure.measure_exist()):
                self.measures_slab_list.append(measure)
        

        #ordena las medias 
        self.measures_list.sort( key = lambda measure: (measure.material,measure.thick,measure.width,measure.length), reverse= True)
        self.measures_slab_list.sort( key = lambda measure: (measure.material,measure.thick), reverse= True)
                    
    #calcula la media de tiempo entre tablas
    def avegare_time(self):

        start_time = (self.slab_list[0].hour* 3600) + (self.slab_list[0].minutes * 60) + self.slab_list[0].seconds

        end_time = (self.slab_list[len(self.slab_list)-1].hour * 3600) + (self.slab_list[len(self.slab_list)-1].minutes * 60) + self.slab_list[len(self.slab_list)-1].seconds
       
        total_time = (end_time - start_time)/60

        average_time = (total_time)/(len(self.slab_list)-1)
        self.avegare_minutes = str(int(average_time))
        self.average_seconds = str(int((abs(average_time)-abs(int(average_time)))*60))
        #para que se muestre el 0 cuando los segundos son una cifra
        if(len(self.average_seconds)==1):
            self.average_seconds = "0" + self.average_seconds[0]
    
   



       

        


