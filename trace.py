# Untitled - By: 86199 - 周六 7月 22 2023
import sensor, image, time
import pyb
from image import SEARCH_EX, SEARCH_DS
sensor.reset()
sensor.set_vflip(True)#图像反转
sensor.set_hmirror(True)
sensor.set_pixformat(sensor.GRAYSCALE)#灰度图
sensor.set_framesize(sensor.QQVGA) # 80x60 (4,800 pixels) - O(N^2) max = 2,3040,000.
#sensor.set_windowing([0,20,80,40])
sensor.skip_frames(time = 2000)     # WARNING: If you use QQVGA it may take seconds
clock = time.clock()
img1 = sensor.snapshot()
blue_gray_thereshold = (36, 189) # (64, 189)
blue_thereshold = (16, 53, -10, 2, -128, -4)
trace_thereshold = (105, 195)
black_thereshold =(26, 91, -16, 10, -8, 10)
black_gray_thereshold = (58, 255)
w, h = img1.width(), img1.height()
cenx, ceny = w//2, h//2   # 计算屏幕中心点的坐标
ROI = (int(cenx-10),int(ceny-10),20,20)
#模板库
mouse = image.Image("/mouse.pgm")
template_two =image.Image("/2.pgm")
template_three =image.Image("/3.pgm")
template_four =image.Image("/4.pgm")
template_road = image.Image("/road.pgm")
#通过外部中断实现tag更改
tag = 1
#十字路口判别需要的变量
left_roi = 0
right_roi = 0
#也可模板匹配识别十字路口
template_road = image.Image("/road2.pgm")
#任务一:巡线
def mission1():
    global tag
    #二值化，对比度提高(不推荐)
    img = sensor.snapshot().binary([black_gray_thereshold])
    line = img.get_regression([(0,0)], x_stride=10, y_stride=1 ,robust = True)
    if line :
        img.draw_line(line.line(),color =255)
        rho_err = abs(line.rho())-img.width()/2
        if line.theta()>90 and :
            print("left")
        else :
            print("right")
        print(line.theta())
        print(rho_err)
    #判断十字路口
    temp = img.find_template(template_road,0.6,roi=(0,0,w,h),step=4,search=SEARCH_EX)
    if temp :
       print("mode 2")
       tag = 2

#模板匹配识别数字
def mission2():
    global tag
    img = sensor.snapshot()
    two = img.find_template(template_two,0.60,roi=(0,0,w,h),step=4,search=SEARCH_EX)
    three = img.find_template(template_three,0.60,roi=(0,0,w,h),step=4,search=SEARCH_EX)
    four = img.find_template(template_four,0.60,roi=(0,0,w,h),step=4,search=SEARCH_EX)
    if two:
        print("find 2")
        tag = 1
    if three:
        print("find 3")
    if four:
        print("find 4")
def mission3():
    print(" ")
while True:
    if tag == 1:
        sensor.reset()
        sensor.set_pixformat(sensor.GRAYSCALE)#灰度图
        sensor.set_framesize(sensor.QQQVGA) # 80x60
        sensor.skip_frames(time = 2000)
        while True:
            if tag != 1:
                break
            mission1()
    elif tag == 2:
        #这里可以加入修改senor设置的语句
        sensor.reset()
        sensor.set_pixformat(sensor.GRAYSCALE)#灰度图
        sensor.set_framesize(sensor.QQVGA) # 80x60
        sensor.skip_frames(time = 2000)
        while True:
            if tag != 2:
                break
            mission2()
    elif tag == 3 :
        while True:
            if tag != 2:
                break
            mission3()
