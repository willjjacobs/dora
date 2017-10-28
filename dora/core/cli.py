import jpeg
"""
Module that contains the command line app.
This is the primary entry point.
"""

class Vision_input:
    def __init__(self, camera):
        pass

class Dashboard:


    def __init__(self, ip_addr):
        pass

    task ={}

    task['multi'] = list((1, "TennisBall"),(2,"Rock"))
    task['file'] =  "filename"
    task['stream'] = "STREAM"
    task['type'] = "check"
    task ['resolution'] = [300,320]
    task['network'] = list(("filename", "rock"))
    task['output'] = "filename/STREAM"



    def get_task(self):
        return task




class Neural_network:
    def __init__(self, nn_file):
        pass

class Core:
    objects = ["Tennis Ball", "Rock", "Cliff"]
    visions = dict()
    visions["webcam"] = Vision_input("webcam")
    visions["kinect"] = Vision_input("kinect")
    neurals = dict()
    dashes = dict()

    def __init__():
        dashes["default"] = Dashboard(null)
        main()

    """handles tasks, which then return to this function when they are over"""
    def main():
        while True:
            task = dashes["default"].get_task()
                while task != null:
                    """parse command line arguments into parameters"""
                    """if task is a single input command """
                   if task["type"] in {"check", "distance", "number", "pixel"}:
                       single(task)
                        task = null
                   else if task is a log command:
                       task = log(task)

    """ provides stream of images and data to UI"""
    def log(timestep, functions, parameters):
        if timestep == 0:
            return null
        set_networks(parameters["network"])
        dash = get_dash(parameters["output"])
        while True:
            task = dash.get_task()
            if task != null:
                return task
            frame = vision[parameters["stream"]].get_frame(parameters["resolution"])
            depth_map = vision["kinect"].get_depth()
            data = infer(frame)
            overlay = overlay_image(data, frame)
            process_data(data, parameters, depth_map)
            dash.push(data, overlay, depth, frame) 
            time.sleep(timestep/1000)

    def set_networks(networks):
        """networks is dict from file names to lists of object types"""
        for nn_file in networks:
            for o_type in networks[nn_file]:
                if neurals[o_type].name != nn_file:
                    neurals[o_type] = Neural_network(nn_file)

    def get_dash(dash_ip):
        if dash_ip !in dashes:
            dashes[dash_ip] = Dashboard(dash_ip)
        return dashes[dash_ip]

    def single(parameters):
        dash = dashes["default"]
        set_networks(parameters["network"])
        frame = vision[parameters["stream"]].get_frame(parameters["resolution"])
        depth_map = vision["kinect"].get_depth()
        data = infer(frame, task["not_wildcard"])
        overlay = overlay_image(data, frame)
        process_data(data, parameters, depth_map)
        dash.push(data, overlay, depth, frame) 
        with open(parameters["output"], "wb") as output:
            output.write(overlay)
        output.close()

  """uses iterator design pattern"""
  def infer(frame, not_wildcard):
      """dict of NN_objects"""
        data_dict = dict()
        """inefficient"""
        for each obj in not_wildcard:
            object_inference = neurals[obj].run_inference(frame)
            for i in object_inference:
                if i.prediction == obj:
                    data_dict[obj] = i
        wildcard_inference = neurals["*"].run_inference(frame)
                for i in wildcard_inference:
                    if i.prediction !in input_object_types:
                        data_dict[obj] = i
        return data_dict

"""
        add_depth(data, depth_map): uses iterator design pattern
            adds depth value of center pixel (found by averaging top left and bottom right pixel) to each element of each object list in data

        overlay_image(data, frame, parameters): uses iterator design pattern
            if parameters[pixel]:
                calls OpenCV to draw rectangles over image based on coordinates in data
                if parameters[distance]:
                    calls OpenCV to draw distances on top of rectangles
            returns edited frame


        process_data(data, parameters, depth_map): adjusts data based on user specifications, uses iterator design pattern
            Sets up new empty payload with fields for each object
            for object in objects:
                Remove all but the parameters["multi"][object] most confident objects in data[object]
            for object in objects:
                if parameters[check]:
                    if data[object] not empty:
                        add true to check section of payload
                if parameters[number]:
                    add data[object].size() to payload
                for o in data[object]:
                    if parameters[pixel]:
                        add pixel coordinates to payload
                    if parameters[distance]:
                        use get_distance(pixel_coords, depth_map) to add distance for each pixel coordinate to payload
            return payload string
"""
