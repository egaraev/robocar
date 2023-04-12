from PIL import Image, ImageDraw
import numpy as np
import tensorflow as tf

# Load the TFLite model
tflite_model_path = 'converted_model.tflite'
interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load the image
image_path = '20230407_180957.jpg'
image = Image.open(image_path).convert('RGB')
image = image.resize((input_details[0]['shape'][2], input_details[0]['shape'][1]))
image_np = np.array(image)

# Preprocess the image
input_data = np.expand_dims(image_np, axis=0)

# Set the input tensor
interpreter.set_tensor(input_details[0]['index'], input_data)

# Run the TFLite model
interpreter.invoke()

# Retrieve the output data
output_data = interpreter.get_tensor(output_details[0]['index'])
output_boxes = interpreter.get_tensor(output_details[1]['index'])
output_classes = interpreter.get_tensor(output_details[2]['index'])
output_scores = interpreter.get_tensor(output_details[3]['index'])

image_pil = Image.fromarray(np.uint8(image_np)).convert('RGBA')
draw = ImageDraw.Draw(image_pil)

# Draw the bounding boxes
for i in range(len(output_boxes[0])):
    max_class_index = np.argmax(output_scores[0][i])
    if output_scores[0][i][max_class_index] > 0.5:
        ymin, xmin, ymax, xmax = output_boxes[0][i]
        xmin = int(xmin * image_pil.width)
        xmax = int(xmax * image_pil.width)
        ymin = int(ymin * image_pil.height)
        ymax = int(ymax * image_pil.height)

        draw.rectangle([(xmin, ymin), (xmax, ymax)], outline='red', width=3)

image_pil.show()
