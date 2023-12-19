from scripts.censor_image_filters import apply_filter
from scripts.pil_nude_detector import pil_nude_detector
from modules import scripts
from PIL import ImageFilter
from math import sqrt

class MyxNsfw(scripts.Script):
    def __init__(self):
        pass

    def title(self):
        return 'MyxNsfw'

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def postprocess(self, p, processed, *args):

        print("MyxNsfw")
        p.extra_generation_params["nsfw_check"] = "nsfw_check"

        if pil_nude_detector.thresholds is None:
            pil_nude_detector.refresh_label_configs()

        censor_mask = pil_nude_detector.get_censor_mask(processed.images[0], 0.5, 'Ellipse', 0.5, pil_nude_detector.thresholds, pil_nude_detector.expand_horizontal, pil_nude_detector.expand_vertical)
        # censor_mask = pil_nude_detector.get_censor_mask(processed.images[0], 0.5, 'Entire image', 0.5, pil_nude_detector.thresholds, pil_nude_detector.expand_horizontal, pil_nude_detector.expand_vertical)
        if censor_mask:
            scale_factor = sqrt((processed.images[0].size[0] ** 2 + processed.images[0].size[1] ** 2) / 524288)

            mask_blur_radis = 10 * scale_factor
            censor_mask = censor_mask.convert('L').filter(ImageFilter.GaussianBlur(mask_blur_radis))
            blur_radius = 30 * scale_factor
            filter_settings = {
                'blur_radius': blur_radius,
                'blur_strength_curve': 3,
                'pixelation_factor': 5,
                'color': '#000000',
            }
            p.extra_generation_params["is_nsfw"] = "is_nsfw"
            processed.images.append(apply_filter(processed.images[0], censor_mask, 'Gaussian Blur', **filter_settings))
