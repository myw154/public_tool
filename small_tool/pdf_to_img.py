import fitz
import os
import sys
import cv2
import numpy as np
from PIL import Image


def get_pre_pdf(pdf_path,  out_path):
    """生成一个pdf的所有图片"""
    doc = fitz.open(pdf_path)
    pdf_name = os.path.basename(pdf_path).replace('.pdf', '')
    if not os.path.exists(out_path):
       os.makedirs(out_path)
    img_path = os.path.join(out_path, pdf_name+'_{}.jpg')
    totaling = doc.pageCount
    img_list = []
    for pg in range(0, totaling):
        page = doc[pg]
        trans = fitz.Matrix(100 / 100.0, 100 / 100.0).preRotate(0)
        pm = page.getPixmap(matrix=trans, alpha=False)
        pm.writePNG(img_path.format(pg))
        img_list.append(img_path.format(pg))
    if len(img_list) > 1:
        get_merge_img(img_list)

def get_merge_img_old(img_list):
    """" 多张图片合成一张图片 """
    read_img_list = []
    new_img_path = img_list[0].replace('_0', '')
    for one_img in img_list:
         imge_read = cv2.imread(one_img)
         read_img_list.append(imge_read)
         with open(new_img_path, 'ab+') as f:
             with open(one_img, 'rb') as r:
                f.write(r.read())
    image = np.concatenate(read_img_list)
    cv2.imwrite(new_img_path, image)

    for one in img_list:
        os.remove(one)

def get_merge_img(img_list):
    # 此处为路径，将三张图像的路径对应自己的改一下
    big_w = 0
    big_h = 0
    for image_file in img_list:
        image_f = Image.open(image_file)
        w,h = image_f.size
        if w > big_w:
            big_w=w
        if h > big_h:
            big_h = h
    img_array = ''
    img = ''
    for i, v in enumerate(img_list):
        img = Image.open(v)  # 打开图片
        # 此处将单张图像进行缩放为统一大小，改为自己单张图像的平均尺寸即可
        img = img.resize((big_w, big_h), Image.ANTIALIAS)
        if i:
            img_array2 = np.array(img)
            # img_array = np.concatenate((img_array, img_array2), axis=1)  # 横向拼接
            img_array = np.concatenate((img_array, img_array2), axis=0)# 纵向拼接
            img = Image.fromarray(img_array)
        else:
            img_array = np.array(img)  # 转化为np array对象
        os.remove(v)
    # 保存图片
    new_img_path = img_list[0].replace('_0', '')
    img.save(new_img_path)


def reset_size(img_list):
    # 设置图片尺寸
    images = []
    big_w = 0
    big_h = 0
    for image_file in image_files:
        image = Image.open(image_file)
        w,h = img.size
        if w > big_w:
            big_w=w
        if h > big_h:
            big_h = h
    for image_file in image_files:
        image = Image.open(image_file)
        image = image.resize((big_w, big_h))
        image.save(image_file)

    # 创建一个新的400x400像素大小的白色背景图像
    new_image = Image.new('RGB', (400, 400), 'white')
    # 将四个图像粘贴到新图像的正确位置
    new_image.paste(images[0], (0, 0))
    new_image.paste(images[1], (200, 0))
    new_image.paste(images[2], (0, 200))



# pdf_dir是pdf绝对路径，out_dir 为解析图片的存储路径
def get_all_pdf():
    pdf_dir = input('请输入pdf文件目录完整路径\n').strip()
    out_dir_name = input('请输入要保存的文件夹名称\n').strip()
    if not out_dir_name:
        print('输入的文件夹名称不正确,结束运行')
        return
    i= 1
    for dir_path, sub_dirs, sub_files in os.walk(pdf_dir):
        all_num = len(sub_files)
        for sub_file in sub_files:
            # 列报表中存在一个'.DS_Store'的隐藏文件
            if sub_file.startswith('.') or (not sub_file.endswith('.pdf')):
                continue
            # 拼接文件的路径
            print('文件总数为：%s 正在解析第{}个pdf文件'.format(all_num, i))
            pdf_file = os.path.join(dir_path, sub_file)
            try:
                get_pre_pdf(pdf_file, os.path.join(dir_path,out_dir_name))
            except Exception as err:
                print(err)
                with open(os.path.join(dir_path, 'error_name.txt'), 'a', encoding='utf-8') as f:
                    f.write(pdf_file+'\n')
            i += 1

def analys_error():
    out_dir = input('请输入要保存的文件夹名称\n').strip()
    with open(out_dir+'/../error_name.txt', 'r', encoding='utf-8') as f:
        file_path_list = f.readlines()
        for file_path in file_path_list:
            get_pre_pdf(file_path.replace('\n', ''), out_dir)

def pdf_to_img(pdf_path):
    # ONE PDF to Images
    import fitz
    doc = fitz.open(pdf_path)
    img_name = pdf_path.replace('.pdf', 'page-{}.png')
    for page in doc:
        pix = page.getPixmap(alpha=False)
        pix.writePNG(img_name.format(page.number))


if __name__ == '__main__':
    # get_all_pdf()
    # analys_error()
    # pdf_to_img()
