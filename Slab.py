
class Slab():
    
    def __init__(self,hour,minutes,seconds):
        self.hour = hour
        self.minutes = minutes
        self.seconds = seconds
        self.code = ''
        self.pieces_list = []
        self.material = 'sin material'
        self.length = 0  
        self.width =  0
        self.thick = 0
        self.m2 = 0
        
    def __str__(self):
        string = ''
        string += f'{self.code}\n'
        
        for piece in self.pieces_list:
        
            string += f'{piece.length} x {piece.width} x {piece.thick} \n'

        return string

    def set_material(self,material):

        self.material = material
        for piece in self.pieces_list:
            piece.material = material
    
    def set_dimensions(self,width,length,thick):
        self.width = width
        self.length = length
        self.thick = thick
        self.m2 = (length * width) / 1000000

    