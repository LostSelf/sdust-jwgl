# coding:utf-8
from PIL import Image as image
from PIL import ImageFilter
import os
import time
import pytesseract
from char_lists import chars

base_path='/Volumes/Untitled 1/workspace/img/'

def covergrey(img):#灰度处理
    return img.convert('L')

def clearedge(img):#去除验证码边框
    for y in range(img.size[1]):
        img.putpixel((0,y),255)
        img.putpixel((1,y),255)
        img.putpixel((2,y),255)
        img.putpixel((img.size[0]-1,y),255)
        img.putpixel((img.size[0]-2,y),255)
        img.putpixel((img.size[0]-3,y),255)
    for x in range(img.size[0]):
        img.putpixel((x,0),255)
        img.putpixel((x,1),255)
        img.putpixel((x,2),255)
        img.putpixel((x,img.size[1]-1),255)
        img.putpixel((x,img.size[1]-2),255)
        img.putpixel((x,img.size[1]-3),255)
    return img

def clearline(img):#去除干扰线并转换为黑白照片
    for y in range(img.size[1]):
        for x  in range(img.size[0]):
            if int(img.getpixel((x,y)))>=110:
                img.putpixel((x,y),0xff)
            else:
                img.putpixel((x,y),0x0)
    return img

def identify(img):
	identification_code_temp=[];identification_code=['']*4;diff_min=[144]*4;
	for i in range (4):
		identification_code_temp.append(img.crop((i*10, 0, i*10+10, 12)).getdata())
	for char in chars:
		diff = [0]*4
		for i in range(4):
			for j in range(120):
				if identification_code_temp[i][j] ^ chars[char][j]:
						diff[i] += 1
		for i in range(4):
			if diff[i]<diff_min[i]:
				diff_min[i]=diff[i]
				identification_code[i]=char
	return ''.join(identification_code)

def identificationCodeHandle(img):
	rect_box = (4,4,44,16)	#crop rectangle,(left, upper, right, lower)
	img = img.crop(rect_box)
	img = img.convert('1')
	return img

'''
for char in chars:
    img=image.new('1',(13,12))
    for y in range(12):
        for x in range(13):
            print len(chars[char])
            img.putpixel((x,y),chars[char][y*13+x])
    img.show()
'''


'''
#方案1 正常图片处理
for i in range(100):
    
    img = image.open(base_path+str(i)+'.jpg')
    print img.mode
    img = covergrey(img)
    img = clearline(img)
    img = clearedge(img)
    img = clearline(img)
    img = img.filter(ImageFilter.EDGE_ENHANCE)
    img = identificationCodeHandle(img)
    img.show()
    identification_code = identify(img)
    print(identification_code)
    time.sleep(2)
#方案二 按照颜色提取字母
'''