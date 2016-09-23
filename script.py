import os, sys
from PIL import Image, ImageEnhance, ImageFilter, ImageOps


def ratio_resize(im, new_size):
    """
    Resize an image, maintaining the aspect ratio
    """
    x, y = im.size
    y = new_size * (y / x)
    return im.resize((int(new_size), int(y)), Image.BILINEAR)

def alter_band(i):
    """
    Alterations to be made on pixels in each band
    """
    # return i * i * 0.01
    if 90 < i < 110 or 140 < i < 160:
        return 0
    elif 110 < i < 140:
        return 255
    else:
        return i

def alter_img(i):
    """
    Alterations to be made on pixels in on the whole img
    """
    if i == 0 or i == 255:
        return 128
    else:
        return i

def process(img_name):
    im = Image.open("{}.jpg".format(img_name))
    # Apply a sharpen filter
    im = im.filter(ImageFilter.SHARPEN)

    # split the image into individual bands
    r, g, b = im.split()

    r = r.point(alter_band)
    g = g.point(alter_band)
    b = b.point(alter_band)

    # combine bands back into one
    im = Image.merge(im.mode, (r, g, b))

    # add contrast
    # im = ImageEnhance.Contrast(im).enhance(1.2)

    im = ImageOps.invert(im)
    im = ImageOps.solarize(im, 245)
    im = ImageOps.invert(im)

    im = ratio_resize(im, 500)

    im = im.point(alter_img)

    # im.show()
    im.save("{}-out.jpg".format(img_name))

for infile in sys.argv[1:]:
    f, e = os.path.splitext(infile)
    process(f)
