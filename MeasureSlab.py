class MeasureSlab():
    def __init__(self,slab,report):
        self.m2 = slab.m2
        self.thick = slab.thick
        self.material = slab.material
        self.report = report
        self.amount = 1
    def measure_exist(self):

        for measure in self.report.measures_slab_list:
            if(measure.material == self.material and measure.thick == self.thick):
                measure.amount += 1
                measure.m2 += self.m2
                return True
        
        return False