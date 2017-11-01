class Classification:
    def __init__(self, box, score, distance):
        self.box = box
        self.score = score
        self.distance = distance

class Vision_input:
    def __init__(self, camera):
        pass

    def get_frame(self):
        pass

    def get_depth(self):
        pass

class Dashboard:
    def __init__(self, ip_addr):
        pass

    task ={}

    task['multi'] = [(1, "TennisBall"),(2,"Rock")]
    task['file'] =  "filename"
    task['stream'] = "STREAM"
    task['type'] = "check"
    task ['resolution'] = [300,320]
    task['network'] = list(("filename", "rock"))
    task['output'] = "filename/STREAM"



    def get_task(self):
        return self.task