from itertools import tee
import xml.etree.ElementTree as ET
import os
from Exceptions import DirectoryException,XmlNotFound,FileCantOpen
from Data import load_data

class XmlReader():

    def __init__(self,folder_path):

        self.folder_path = folder_path
      
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
        raise XmlNotFound(self.first_slab_code)
        
    def get_xml_slabs_data(self,slab_code_set,first_code):
      
        file_code = first_code
        code_list = list(slab_code_set)
        slab_data_dic = {}
       
        
        read_files = 0
        while(len(code_list) != 0 and read_files < 200):

            try:
                
                slab_data = self.get_slab_data(file_code,code_list)
                if( slab_data != False):
                    slab_data_dic.update(slab_data)
                   
            except:

                print('erro añadiendo datos de tabla')

            read_files += 1
            file_code = str(int(file_code) + 1).zfill(8)  

        return slab_data_dic

    def get_slab_data(self,file_code,code_list):
        
        

        file_name = f'{self.folder_path}/CME_{file_code}_CUT_SCHEME.xml'

        try:
            
            tree = ET.parse(file_name)
        except:
            
            raise FileCantOpen(f'CME_{file_code}_CUT_SCHEME.xml')

        root = tree.getroot()
        
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
       
               
        
            