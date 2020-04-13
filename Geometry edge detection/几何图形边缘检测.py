#2020.02.24日   2020.02.25日修改,加入显示选中后的图片，但无法清除该位置，永远停留
#imread读取中文路径报错,PhotoImage()只能读取png文件
#
#要运行该程序首先要安装opencv库
################################################################################

#import S

#导入tk库用于建立tk界面
import tkinter as tk
from tkinter import filedialog
from tkinter import *


global Filepath
global frame1
global photo1,w_box,h_box

#导入opencv库使用识别算法
import cv2
import numpy as np

import io  
from PIL import Image, ImageTk


###########################图片缩放函数#####################################
def resize(w, h, w_box, h_box, pil_image):  
      ''' 
      对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例
      '''      
      f1 = 1.0*w_box/w # 1.0 forces float division in Python2  
      f2 = 1.0*h_box/h  
      factor = min([f1, f2])  
      #print(f1, f2, factor) # test  
      # use best down-sizing filter  
      width = int(w*factor)  
      height = int(h*factor)  
      return pil_image.resize((width, height), Image.ANTIALIAS)

###########################################################################
    

##########################用文件管理器选择文件###############################
def callback():
    '''打开选择文件夹对话框'''
    root = tk.Tk()
    root.withdraw()
    global Filepath
    global frame1
    global photo1,w_box,h_box
    #Folderpath = filedialog.askdirectory()#获得选择的文件夹路径
    Filepath = filedialog.askopenfilename()#获得选择的文件路径，不可有中文

    
    #print('Folderpath:',Folderpath)
    var.set(Filepath)	#在界面左侧显示文件路径

    #显示选中的文件
#=====================为图像缩放做准备====================================#
    #期望图像显示的大小  
    w_box = 300  
    h_box = 300
    #以一个PIL图像对象打开  
    pil_image = Image.open(Filepath)
    
    #获取图像的原始大小  
    w, h = pil_image.size
    
    #缩放图像让它保持比例，同时限制在一个矩形框范围内  
    pil_image_resized = resize(w, h, w_box, h_box, pil_image)

    #把PIL图像对象转变为Tkinter的PhotoImage对象  
    photo1 = ImageTk.PhotoImage(pil_image_resized)
#=========================================================================#
    
    #photo1 = PhotoImage(file=Filepath)
    imgLabel = Label(frame1, image=photo1,width=w_box,height=h_box)    #将photo1设置为全局变量才能在函数中显示图片
    imgLabel.pack(side=RIGHT)
    
############################################################################




###################canny算子检测#####################################
def callback2():                
    global Filepath			#使用全局路径，注意：千万不能有中文路径，否则报错！
    img = cv2.imread(Filepath, 0)
    cv2.imwrite("canny.jpg", cv2.Canny(img, 200, 300))
    pi=cv2.Canny(img, 200, 300)
    cv2.imshow("Canny",cv2.imread("canny.jpg"))
    var.set('已完成Canny边缘检测')
    #cv2.waitKey()
    #cv2.destroyAllWindows()

#####################################################################


###################sobel算子检测#####################################
def callback3():
    global Filepath		#注意：千万不能有中文路径，否则报错！
    source = cv2.imread(Filepath)
    source = cv2.cvtColor(source,cv2.COLOR_BGR2GRAY)

    
    #sobel_x:发现垂直边缘
    sobel_x =cv2.Sobel(source,cv2.CV_64F,1,0)
    #sobel_y:发现水平边缘
    sobel_y = cv2.Sobel(source,cv2.CV_64F,0,1)
     
    sobel_x = np.uint8(np.absolute(sobel_x))
    sobel_y = np.uint8(np.absolute(sobel_y))
    np.set_printoptions(threshold=np.inf)
    
     
    sobelCombined = cv2.bitwise_or(sobel_x, sobel_y)#按位或
    sum = sobel_x+sobel_y
     
    cv2.imshow('sobel_x',sobel_x)
    cv2.imshow('sobel_y',sobel_y)
    cv2.imshow('sobel_combined',sobelCombined)
    cv2.imshow('sum',sum)
    var.set('已完成Sobel边缘检测')
    
    #cv2.imwrite('sobel_x.jpg',sobel_x)
    #cv2.imwrite('sobel_y.jpg',sobel_y)
    #cv2.imwrite('sobel_combined.jpg',sobelCombined)
    #cv2.imwrite('sum.jpg',sum)


######################################################################






###################自编算法检测（完善中）#############################
#def callback4():
      #调用另一个py文件的功能
#      global Filepath
      #S.ShapeRecognition('D:/1.png')     
#      src = cv2.imread('D:/1.png')
#      ld=S.ShapeAnalysis()
#      ld.S.analysis(src)

######################################################################








root = Tk()	#将tk库赋值给句柄
root.title('基于python的几何图形边缘检测')#界面主标题

#Frame    框架控件；在屏幕上显示一个矩形区域，多用来作为容器
frame1 = Frame(root)#主界面区域
frame2 = Frame(root)#按钮区域


var = StringVar()  #设置字符串
var.set("组长：李玉林  组员：冯烽 赵凌云 王鹏\n")
photo = PhotoImage(file="20.png")   #只能读取png图片

textLabel = Label(frame1,
                  textvariable = var,
                  justify = LEFT)

textLabel.pack(side=LEFT)




imgLabel = Label(frame1, image=photo)
imgLabel.pack(side=RIGHT)

   

#定义按钮，两种不同的按钮定义方式。
theButton = Button(frame2,text="选择一张图片",command=callback)               
theButton2 = Button(frame2,text="Canny算子检测",bg='blue',fg='black',command=callback2)
theButton.pack()
theButton2.pack()

Button(frame2,text='sobel算子检测',bg='blue',fg='black',command=callback3).pack()
Button(frame2,text='自编算法检测').pack()


#定义位置
frame1.pack(padx=100, pady=100)  #主界面位置
frame2.pack(padx=100, pady=100)  #按钮位置


mainloop()
