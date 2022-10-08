# import the necessary packages
from importlib.resources import path
from tkinter import Tk, Button, Label, filedialog, ttk, font, StringVar
import base64

import grpc
from PIL import Image
from PIL import ImageTk
import numpy as np

import backend_pb2
import backend_pb2_grpc


# initialize the window toolkit along with the two image panels
root = Tk()
panelA = None




prediction_string_var = StringVar()
prediction_string_var.set("prediction")

def select_image():
    # grab a reference to the image panels
    global panelA, backend_client
    # open a file chooser dialog and allow the user to select an input
    # image
    global path
    path = filedialog.askopenfilename()

    # ensure a file path was selected
    if len(path) > 0:
        
        path_message = backend_pb2.img_path(path=path)
        print(path_message)
        print(type(path_message))
        response = backend_client.load_image(path_message)

        img_content = response.img_content
        img_w = response.width
        img_h = response.height

        b64decoded = base64.b64decode(img_content)
        image = np.frombuffer(b64decoded, dtype=np.uint8).reshape(img_h, img_w, -1)

        # convert the images to PIL format...
        image = Image.fromarray(image)
        # ...and then to ImageTk format
        image = ImageTk.PhotoImage(image)

        # if the panels are None, initialize them
        if panelA is None:
            # the first panel will store our original image
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)
        else:
            # update the pannels
            panelA.configure(image=image)
            panelA.image = image

def predict_image():
    global path
    
    if len(path) > 0:
        path_message = backend_pb2.img_path(path=path)   

        response = backend_client.predicting(path_message)
        inferencia = response.val_inferencia
        prediction_string_var.set("Diagnóstico= "+ inferencia)

    


# Backend client definition
options = [('grpc.max_message_length', 100 * 1024 * 1024)]
channel = grpc.insecure_channel("192.168.1.53:50051", options=options)
backend_client = backend_pb2_grpc.BackendStub(channel=channel)

# create a button, then when pressed, will trigger a file chooser
# dialog and allow the user to select an input image; then add the
# button the GUI
btn = Button(root, text="Select an image", command=select_image)
btn_prediction = Button(root, text="Predecir", command=predict_image)
#--------------------------------------------------------------------------------
fonti = font.Font(weight="bold")
prediction_label = ttk.Label(root, textvariable = prediction_string_var, font=fonti)
#---------------------------------------------------------------------------------
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
btn_prediction.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
prediction_label.pack()
# kick off the GUI
root.mainloop()
