import cv2
import NeuralNet

nn = NeuralNet()

cap = cv2.VideoCapture(0)
nn.neural_net_init()

while(True):
    ret, image = cap.read()
    image = nn.run_inference(image)
    cv2.imshow('object detection', cv2.resize(image, (800,600)))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break