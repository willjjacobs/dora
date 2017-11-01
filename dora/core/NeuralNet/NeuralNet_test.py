import cv2
import tensorflow as tf
import NeuralNet

cap = cv2.VideoCapture(0)
nn = NeuralNet.NeuralNet()

with nn.detection_graph.as_default():
    with tf.Session(graph=nn.detection_graph) as sess: 
        while(True):
            ret, image = Your image capture function here #cap.read()      
            dto = nn.run_inference(image, sess)
            // Put your function here
            cv2.imshow('object detection', cv2.resize(image, (800,600)))
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break