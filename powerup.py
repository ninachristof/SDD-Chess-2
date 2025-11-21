class powerup():
    description = ""
    new_capture = []
    new_move = []

    def __init__(self,newdescription,newcapture,newmove):
        self.description = newdescription
        self.new_capture = newcapture
        self.new_move = newmove

    def get_description(self):
        return self.description
    
    def get_capture(self):
        return self.new_capture
    
    def get_move(self):
        return self.new_move
