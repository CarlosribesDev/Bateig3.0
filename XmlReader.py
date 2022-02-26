from itertools import tee
import xml.etree.ElementTree as ET
import os
from Exceptions import DirectoryException,XmlNotFound,FileCantOpen
from Data import load_data

class XmlReader():

    def __init__(self,folder_path):

        self.folder_path = folder_path

    #devuelve el arhivo por el que empezar a partir del codigo de la primera tabla 
    def get_first_xml_code(self,first_slab_code):

        try:
            folder = os.listdir(self.folder_path)
        except:
            raise DirectoryException(self.folder_path)
        
        for file in folder:
            
            file_slab_code = file[13:31]

            if (file_slab_code == first_slab_code):
                
                file_code = file[4:12]
                return file_code
        
        #si no se ha encontrado el archivo
        raise XmlNotFound(first_slab_code)

    #devuelve un diccionario con los datos de cada tabla   
    def get_xml_slabs_data(self,slab_code_set,first_code):
      
        file_code = first_code
        code_list = list(slab_code_set)
        slab_data_dic = {}
       
        while(len(code_list) != 0 ):

            try:               
                slab_data = self.get_slab_data(file_code,code_list)
                if( slab_data != False):
                    slab_data_dic.update(slab_data)        
            except:
                break
                   
            file_code = str(int(file_code) + 1).zfill(8)  

        return slab_data_dic

    #Lee el CUT_SCHEME.xml de una tabla y devuelve los datos
    def get_slab_data(self,file_code,code_list):
        

        file_name = f'CME_{file_code}_CUT_SCHEME.xml'
        path = f'{self.folder_path}/{file_name}'

        try:     
            tree = ET.parse(path)
        except:
            
            raise FileCantOpen(file_name)

        root = tree.getroot()
        
        #Codigo
        code = root[2].attrib['Code']
        #Dimensiones
        length =  float(root[2].attrib['Length']) 
        width =  float(root[2].attrib['Width'])
        thick = float(root[2].attrib['Thickness'])/10
        
        #Material
        data = load_data()
        material_id = root[2].attrib['MaterialId']
        materials_list = data['materials']
        material = materials_list[material_id]

        if(code in code_list):
            slab_data = {
                code : {
                    'length' : length,
                    'width' : width,
                    'thick' : thick,
                    'material' : material

                }
                
            }
            code_list.remove(code)
            return slab_data
        else: return False
       
               
        
            