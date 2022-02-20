class Piece():

    def __init__(self,length,width,thick,m2,code):
        
        self.length = length
        self.width = width
        self.thick = thick
        self.amount = 1
        self.m2 = m2
        self.code = code
        self.material = 'sin material'
        self.measure = (length,width,thick)

    def __str__(self):

        return f'{self.length} x {self.width} x {self.thick}'
    