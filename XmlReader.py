from itertools import tee
import xml.etree.ElementTree as ET
import os
from Exceptions import DirectoryException,XmlNotFound,FileCantOpen
from Data import load_data

class XmlReader():

    def __init__(self,folder_path,first_slab_code):

        self.folder_path = folder_path
        self.first_slab_code = first_slab_code
    
    def get_first_xml_code(self):

        try:
            folder = os.listdir(self.folder_path)
        except:
            raise DirectoryException(self.folder_path)
        
        for file in folder:
            
            file_slab_code = file[13:31]

            if (file_slab_code == self.first_slab_code):
                
                file_code = file[4:12]
                return file_code
        
        #si no se ha encontrado el archivo
        raise XmlNotFound(self.first_slab_code)
        
    def get_all_slab_data(self,slab_list,first_code):
        
        file_code = first_code
       
        for slab in slab_list:
   
            try:
                self.set_slab_data(slab,file_code)
            except:
               continue
            
            file_code = str(int(file_code) + 1).zfill(8)      

    def set_slab_data(self,slab,file_code):

        try:
            
            root = self.get_xml_data(file_code)
        except Exception as e:            
            raise e  
        #Combramos que sea el codigo de la tabla,si no,pasamos al siguiente
       
        code_correct = False
       
        while(not code_correct):
            code = root[2].attrib['Code']
       
            if(slab.code == code): code_correct = True
            else:
                
                file_code = str(int(file_code) + 1).zfill(8)
                try:
                    root = self.get_xml_data(file_code)
                except Exception as e:            
                    raise e

        
        #Dimensiones
        slab.length =  root[2].attrib['Length'] 
        slab.width =  root[2].attrib['Width']
        slab.thick = float(root[2].attrib['Thickness'])/10
        slab.m2 = (float(slab.length) * float(slab.width)) / 1000000
        
        #Material
        data = load_data()
        material_id = root[2].attrib['MaterialId']
        materials_list = data['materials']
        material = materials_list[material_id] 
        slab.set_material(material)

        
    def get_xml_data(self,file_code):
       
        file_name = f'{self.folder_path}/CME_{file_code}_CUT_SCHEME.xml'
        try:
            
            tree = ET.parse(file_name)
        except:
            
            raise FileCantOpen(f'CME_{file_code}_CUT_SCHEME.xml')

        root = tree.getroot()
        return root