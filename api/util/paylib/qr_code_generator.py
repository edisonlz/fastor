#coding=utf-8
import random
import os
import urllib


def mk_qr(content, local_path='/tmp/', filename_pre_fix='prefix_'):
    from PIL import Image
    import qrcode

    # 1. make qr_image
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(content)
    qr.make(fit=True)

    img = qr.make_image()
    img = img.convert("RGBA")
  

    # 2. save qr_image
    img_name = 'qr_' + filename_pre_fix + gen_random_string(16)
    img_path = local_path + img_name + '.png'
    img.save(img_path, quality=100)


 
    #上传到服务器或者云上,需要重新实现
    remote_url = upload_file(file_obj)
    
    if img_path:
        os.remove(img_path)
    
    return remote_url



def gen_random_string(length):
    import string
    chars=string.ascii_letters+string.digits
    return ''.join([random.choice(chars) for i in range(length)])


