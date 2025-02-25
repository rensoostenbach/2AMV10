"""
Created on Thu Oct 26 11:06:51 2017

@author: Utku Ozbulak - github.com/utkuozbulak

Adapted by Rens Oostenbach for custom trained YOLOv5 model.
"""
from PIL import Image
import numpy as np
import torch
import sys
from pytorch_cnn_visualizations.src.misc_functions import get_params, save_class_activation_images


class CamExtractor():
    """
        Extracts cam features from the model
    """

    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None

    def save_gradient(self, grad):
        self.gradients = grad

    def forward_pass_on_convolutions(self, x):
        """
            Does a forward pass on convolutions, hooks the function at given layer.
            Code is written for YOLOv5l as of now. Some adaptations had to be made in
            the next for loop, to deal with the model structure of YOLOv5l.
        """
        conv_output = None
        layer_outputs = []
        output = []
        for index, module in enumerate(self.model.model):
            x = x.cpu()
            module = module.to(torch.float32)

            if module.type == 'models.common.Concat':
                layer = module.f[1]
                x = torch.cat((x, layer_outputs[layer]), 1)
            elif module.type == 'models.yolo.Detect':
                # Use output of layer 23 for detection, since we are using YOLOv5l
                x = module.m[2].to(torch.float32)(layer_outputs[23])
                output.append(x)
            else:
                x = module(x)

            layer_outputs.append(x if int(index) in self.model.save else [])

            if int(index) == self.target_layer:
                x.register_hook(self.save_gradient)
                conv_output = x  # Save the convolution output on that layer
        return conv_output, x

    def forward_pass(self, x):
        """
            Does a full forward pass on the model
        """
        # Forward pass on the convolutions
        conv_output, x = self.forward_pass_on_convolutions(x)
        x = x.view(x.size(0), -1)  # Flatten
        # Forward pass on the classifier
        # x = self.model.classifier(x)
        return conv_output, x


class GradCam():
    """
        Produces class activation map
    """

    def __init__(self, model, target_layer):
        self.model = model
        self.model.eval()
        # Define extractor
        self.extractor = CamExtractor(self.model, target_layer)

    def generate_cam(self, input_image, target_class=None):
        # Full forward pass
        # conv_output is the output of convolutions at specified layer
        # model_output is the final output of the model (1, 1000)
        conv_output, model_output = self.extractor.forward_pass(input_image)
        if target_class is None:
            target_class = np.argmax(model_output.data.numpy())
        # Target for backprop
        one_hot_output = torch.FloatTensor(1, model_output.size()[-1]).zero_()
        one_hot_output[0][target_class] = 1
        # Zero grads
        self.model.model.zero_grad()

        # self.model.classifier.zero_grad()
        # Backward pass with specified target
        model_output.backward(gradient=one_hot_output, retain_graph=True)
        # Get hooked gradients
        guided_gradients = self.extractor.gradients.data.numpy()[0]
        # Get convolution outputs
        target = conv_output.data.numpy()[0]
        # Get weights from gradients
        weights = np.mean(guided_gradients, axis=(1, 2))  # Take averages for each gradient
        # Create empty numpy array for cam
        cam = np.ones(target.shape[1:], dtype=np.float32)
        # Multiply each weight with its conv output and then, sum
        for i, w in enumerate(weights):
            cam += w * target[i, :, :]
        cam = np.maximum(cam, 0)
        cam = (cam - np.min(cam)) / (np.max(cam) - np.min(cam))  # Normalize between 0-1
        cam = np.uint8(cam * 255)  # Scale between 0-255 to visualize
        cam = np.uint8(Image.fromarray(cam).resize((input_image.shape[2],
                                                    input_image.shape[3]), Image.ANTIALIAS)) / 255
        # ^ I am extremely unhappy with this line. Originally resizing was done in cv2 which
        # supports resizing numpy matrices with antialiasing, however,
        # when I moved the repository to PIL, this option was out of the window.
        # So, in order to use resizing with ANTIALIAS feature of PIL,
        # I briefly convert matrix to PIL image and then back.
        # If there is a more beautiful way, do not hesitate to send a PR.

        # You can also use the code below instead of the code line above, suggested by @ ptschandl
        # from scipy.ndimage.interpolation import zoom
        # cam = zoom(cam, np.array(input_image[0].shape[1:])/np.array(cam.shape))
        return cam


def run(original_image, obj, object_class, number, **person):
    # Get params
    (original_image, prep_img, file_name_to_export, pretrained_model) = \
        get_params(original_image=original_image, obj=obj, object_class=object_class, picture_number=number, person=person)
    # Grad cam, layer 22 because it is the last one before the final convolutional layer.
    grad_cam = GradCam(pretrained_model, target_layer=22)
    # Generate cam mask
    cam = grad_cam.generate_cam(prep_img, target_class=object_class)
    # Save mask
    save_class_activation_images(original_image, cam, file_name_to_export)

