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
    task['file'] =  'filename'
    task['stream']



    def get_task(self):





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

"""
       main(): handles tasks, which then return to this function when they are over
            while True:
                task = dashes["default"].get_task()
                while task != null:
                    parse command line arguments into parameters
                    if task is a single input command (aka check, distance, number, or pixel):
                        single(parameters)
                        task = null
                   else if task is a log command:
                       task = log(parameters)

        log(timestep, functions, parameters): provides stream of images and data to UI
            if timestep == 0:
                return null
            set_networks(parameters[--network])
            dash = get_dash([parameters[--output]])
            while True:
                task = dash.get_task()
                if task != null:
                    return task
                frame = vision[parameters[--stream]].get_frame(parameters[--resolution])
                depth_map = vision["kinect"].get_depth()
                data = infer(frame)
                overlay = overlay_image(data, frame)
                process_data(data, parameters, depth_map)
                dash.push(data, overlay, depth, frame) 
                wait(timestep)

        set_networks(networks): uses iterator design pattern
            extract (neural_file_names, input_object_types) from networks
            for (n,o) in (neural_file_names, input_object_types):
                if neurals[o].name != n:
                    neurals[o] = Neural_network(n)

        get_dash(dash_ip):
            if dash_ip !in dashes:
                dashes[dash_ip] = Dashboard(dash_ip)
            return dashes[dash_ip]

        single(parameters):
            dash = dashes["default"]
            output  = File([parameters[--output]])
            set_networks(parameters[--network])
            frame = vision[parameters[--stream]].get_frame(parameters[--resolution])
            depth_map = vision["kinect"].get_depth()
            data = infer(frame)
            overlay = overlay_image(data, frame)
            process_data(data, parameters, depth_map)
            dash.push(data, overlay, depth, frame) 
            write overlay to output


      infer(): uses iterator design pattern
            data_dict = dict() - dict of lists of NN_objects
            for each object in input_object_types:
                object_inference = neurals[object].run_inference(frame)
                for i in object_inference:
                    if i.prediction == object:
                        data_dict[object].append(i)
            wildcard_inference = neurals["*"].run_inference(frame)
                    for i in wildcard_inference:
                        if i.prediction !in input_object_types:
                            data[object].append(i)
            return data_dict

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
                Remove all but the parameters[--multi][object] most confident objects in data[object]
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
