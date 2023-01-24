from fpioa_manager import *
import os, Maix, lcd, image, sensor, gc, time
from Maix import FPIOA, GPIO
import KPU as kpu

lcd.init(type=1,freq=15000000,width=240,height=240,color=(0,0,0))
lcd.rotation(3)
lcd.clear(0,0,0)

lcd.draw_string(20,20, "DIPAE - ML", lcd.WHITE, lcd.BLACK)
time.sleep(1)
lcd.draw_string(20,40, "- Initializing Camera...", lcd.WHITE, lcd.BLACK)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))    #set to 224x224 input

#sensor.set_hmirror(0)              #flip camera
sensor.set_vflip(0)
sensor.set_hmirror(0)
sensor.run(1)
sensor.skip_frames(30)

lcd.rotation(3)

# img_boot = image.Image("/sd/images/boot_digit.jpg")
# lcd.display(img_boot, oft=(0,0))
# time.sleep(2)
lcd.clear()
#task = kpu.load("/sd/model/mnist.kmodel")           #load model from flash address 0x200000
#task_mnist = kpu.load("/sd/models/mnist.kmodel")
task_mnist = kpu.load(0x300000)
sensor.run(1)

while True:
    img_mnist = sensor.snapshot()

    img_mnist1=img_mnist.to_grayscale(1)        #convert to gray
    img_mnist2=img_mnist1.resize(28,28)         #resize to mnist input 28x28
    a=img_mnist2.invert()                 #invert picture as mnist need
    a=img_mnist2.strech_char(1)           #preprocessing pictures, eliminate dark corner

    #lcd.display(img2,oft=(10,40))   #display small 28x28 picture
    a=img_mnist2.pix_to_ai()              #generate data for ai

    fmap_mnist=kpu.forward(task_mnist,img_mnist2)     #run neural network model
    plist_mnist=fmap_mnist[:]                   #get result (10 digit's probability)
    pmax_mnist=max(plist_mnist)                 #get max probability
    max_index_mnist=plist_mnist.index(pmax_mnist)     #get the digit

    print(str(max_index_mnist)+","+str(int(pmax_mnist*100)))

    img_mnist.draw_rectangle(0,0,45,50,color=(0,0,0),fill=True)
    img_mnist.draw_string(4,3,str(max_index_mnist),color=(255,255,255),scale=4)
    lcd.display(img_mnist,oft=(8,8))        #display large picture

    # lcd.draw_string(8,8,"%d: %.3f"%(max_index,pmax),lcd.WHITE,lcd.BLACK)

kpu.deinit(task)
