class Measure():

    def __init__(self,piece,report):
        self.length = piece.length
        self.width = piece.width
        self.thick = piece.thick
        self.amount = 1
        self.m2 = piece.m2
        self.material = piece.material
        self.report = report
        
        self.measures = f'{piece.length} x {piece.width} x {piece.thick} {piece.material}'
    
    def measure_exist(self):

        for measure in self.report.measures_list:

            if(measure.measures == self.measures) :
                measure.amount +=1
                measure.m2 += self.m2
                return True
                 
        return False
