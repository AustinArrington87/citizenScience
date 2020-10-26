import sys
import io
from PIL import Image
try:
    from PIL import ImageCms
    from PIL.ImageCms import ImageCmsProfile
    ImageCms.core.profile_open
except ImportError as v:
    # Skipped via setUp()
    pass

def convert_to_srgb(img):
    '''Convert PIL image to sRGB color space (if possible)'''
    icc = img.info.get('icc_profile', '')
    if icc:
        io_handle = io.BytesIO(icc)     # virtual file
        src_profile = ImageCms.ImageCmsProfile(io_handle)
        dst_profile = ImageCms.createProfile('sRGB')
        img = ImageCms.profileToProfile(img, src_profile, dst_profile)
    return img

img = Image.open('C9BA161EDB-6.jpg')
img_conv = convert_to_srgb(img)
if img.info.get('icc_profile', '') != img_conv.info.get('icc_profile', ''):
    # ICC profile was changed -> save converted file
    img_conv.save('image_sRGB.jpg',
                  format = 'JPEG',
                  quality = 100,
                  icc_profile = img_conv.info.get('icc_profile',''))