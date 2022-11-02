class TargetValueMapping():
    def __init__(self):
        self.neg : int = 0
        self.pos : int = 1
    
    def to_dict(self):
        return self.__dict__
    
    def reverse_mapping(self):
        return dict(zip(self.__dict__.values() , self.__dict__.keys()))