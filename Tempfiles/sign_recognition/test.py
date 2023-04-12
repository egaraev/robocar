import cv2
import os

from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference

import os

def main():
    model_path = 'D:\\repo\\robocar\\Tempfiles\\sign_recognition\\efficientdet-lite_edgetpu.tflite'
    label_path = 'D:\\repo\\robocar\\Tempfiles\\sign_recognition\\labels.txt'
    input_folder = 'D:\\repo\\robocar\\Tempfiles\\sign_recognition\\input_images'
    output_folder = 'D:\\repo\\robocar\\Tempfiles\\sign_recognition\\output_images'
    top_k = 10
    threshold = 0.1

    print('Loading {} with {} labels.'.format(model_path, label_path))
    interpreter = make_interpreter(model_path)
    interpreter.allocate_tensors()
    labels = read_label_file(label_path)
    inference_size = input_size(interpreter)

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(input_folder):
        # Check if the file is an image
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, file)
            output_image_path = os.path.join(output_folder, file)

            cv2_im = cv2.imread(image_path)
            cv2_im_rgb = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
            cv2_im_rgb = cv2.resize(cv2_im_rgb, inference_size)
            run_inference(interpreter, cv2_im_rgb.tobytes())
            objs = get_objects(interpreter, threshold)[:top_k]
            cv2_im = append_objs_to_img(cv2_im, inference_size, objs, labels, threshold)

            cv2.imwrite(output_image_path, cv2_im)
            print('Processed and saved:', output_image_path)
            cv2.imshow('Output Image', cv2_im)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


def append_objs_to_img(cv2_im, inference_size, objs, labels, threshold):
    height, width, channels = cv2_im.shape
    scale_x, scale_y = width / inference_size[0], height / inference_size[1]
    for obj in objs:
        if obj.score < threshold:  # Skip objects with a low score
            continue

        bbox = obj.bbox.scale(scale_x, scale_y)
        x0, y0 = int(bbox.xmin), int(bbox.ymin)
        x1, y1 = int(bbox.xmax), int(bbox.ymax)

        percent = int(100 * obj.score)
        label = '{}% {}'.format(percent, labels.get(obj.id, obj.id))

        cv2_im = cv2.rectangle(cv2_im, (x0, y0), (x1, y1), (0, 255, 0), 2)
        cv2_im = cv2.putText(cv2_im, label, (x0, y0-10),
                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    return cv2_im


if __name__ == '__main__':
    main()
