import numpy as np
import pandas as pd
from scipy.stats import norm
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import *
import matplotlib
import seaborn as sns
from matplotlib import pyplot as plt
from PIL import Image, ImageTk

def BS_command():
    global window

    def BlackScholesPrice():
        S = var_s.get()
        K = var_k.get()
        sigma = var_sigma.get()
        T = var_t.get()
        r = var_r.get()
        option_type = var_cp.get()
        print(S)
        print(option_type)
        T = T/365.0
        if option_type == 'call':
            d1 = ( np.log(S/K) + (r + np.power(sigma,2)/2) * T ) / ( sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)
            Price = S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
            result_box.delete(0.0,END)
            result_box.insert(INSERT,str(Price)) 
        elif option_type == 'put':
            d1 = ( np.log(S/K) + (r + np.power(sigma,2)/2) * T ) / ( sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)
            Price = K * np.exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(d1)
            result_box.delete(0.0,END)
            result_box.insert(INSERT,str(Price))
        else:
            result_box.delete(0.0,END)
            result_box.insert(INSERT,'The Type is not correct,try again')
    
    BS_window = tk.Toplevel(window)
    BS_window.title('BS价格计算')
    BS_window.geometry('400x400')
    tk.Label(BS_window, text='现货价格S: ').place(x=10,y=10,anchor='nw')
    tk.Label(BS_window, text='执行价格K: ').place(x=10,y=50,anchor='nw')
    tk.Label(BS_window, text='到期天数T: ').place(x=10,y=90,anchor='nw')
    tk.Label(BS_window, text='无风险利率r: ').place(x=10,y=130,anchor='nw')
    tk.Label(BS_window, text='波动率sigma: ').place(x=10,y=170,anchor='nw')
    tk.Label(BS_window, text='Call or Put: ').place(x=10,y=210,anchor='nw')

    var_s = tk.DoubleVar()
    entry_s = tk.Entry(BS_window, textvariable=var_s)
    entry_s.place(x=120,y=10,anchor='nw')
    
    var_k = tk.DoubleVar()
    entry_k = tk.Entry(BS_window, textvariable=var_k)
    entry_k.place(x=120,y=50,anchor='nw')
    
    var_t = tk.DoubleVar()
    entry_t = tk.Entry(BS_window, textvariable=var_t)
    entry_t.place(x=120,y=90,anchor='nw')
    
    var_r = tk.DoubleVar()
    entry_r = tk.Entry(BS_window, textvariable=var_r)
    entry_r.place(x=120,y=130,anchor='nw')
    
    var_sigma = tk.DoubleVar()
    entry_sigma = tk.Entry(BS_window, textvariable=var_sigma)
    entry_sigma.place(x=120,y=170,anchor='nw')
    
    var_cp = tk.StringVar()
    entry_sigma = tk.Entry(BS_window, textvariable=var_cp)
    entry_sigma.place(x=120,y=210,anchor='nw')
    
    print(var_s.get)
    result_box = tk.Text(BS_window,height=3,width=20)
    result_box.place(x=110,y=320) 
    
    b = tk.Button(BS_window, 
    text='计算欧式期权价格:',      # 显示在按钮上的文字
    width=15, height=2, 
    command=BlackScholesPrice).place(x=120,y=250)
    
    
def Newton_commant():
    global window
    global image
    global im
    image = None
    im = None
    def GetImpliedV():
        S = var_s.get()
        K = var_k.get()
        T = var_t.get()/365
        r = var_r.get()
        Price = var_price.get()
        option_type = var_cp.get()
        

        
        GetTheIVPlot(S,K,T,r,Price,option_type)
        #canvas.create_image(100, 200, image=i, anchor=tk.NW)
        global image
        global im
        image = Image.open("Temp.png")  
        im = ImageTk.PhotoImage(image)  
  
        
        theimage = canvas.create_image(0,0,image=im,anchor=tk.NW)
     
        result_box.delete(0.0,END)

        implied_v = 0.5
        implied_v_update = 0
        delta_iv = 1e-5
        num_derivative = (BlackScholesPrice(S,K,T,implied_v,r,option_type) - BlackScholesPrice(S,K,T,implied_v-delta_iv,r,option_type))/delta_iv
        implied_v_update = implied_v - ( BlackScholesPrice(S,K,T,implied_v,r,option_type) - Price ) / num_derivative
        iter_num = 0
        while abs(implied_v_update - implied_v) > 1e-30 :
            implied_v = implied_v_update
            num_derivative = (BlackScholesPrice(S,K,T,implied_v,r,option_type) - BlackScholesPrice(S,K,T,implied_v-delta_iv,r,option_type))/delta_iv
            implied_v_update = implied_v - ( BlackScholesPrice(S,K,T,implied_v,r,option_type) - Price ) / num_derivative        
            iter_num = iter_num + 1
            if iter_num % 1000 == 0:
                result_box.insert(INSERT,"After %d times iter,the implied_v = %6f\n" % (iter_num,implied_v))
            if iter_num > 10000:
                result_box.insert(INSERT,"The max iter_nums have been limited\n")
                break
        result_box.insert(INSERT,str(implied_v_update)) 

    def BlackScholesPrice(S,K,T,sigma,r,option_type):
        if option_type == 'call':
            d1 = ( np.log(S/K) + (r + np.power(sigma,2)/2) * T ) / ( sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)
            Price = S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
            return Price
        elif option_type == 'put':
            d1 = ( np.log(S/K) + (r + np.power(sigma,2)/2) * T ) / ( sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)
            Price = K * np.exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(d1) 
            return Price
        else:
            print('The type is not correct,try again!')
            
    def GetImpliedVFast(S,K,T,r,Price,option_type):
        implied_v = 0.5
        implied_v_update = 0
        delta_iv = 1e-5
        num_derivative = (BlackScholesPrice(S,K,T,implied_v,r,option_type) - BlackScholesPrice(S,K,T,implied_v-delta_iv,r,option_type))/delta_iv
        implied_v_update = implied_v - ( BlackScholesPrice(S,K,T,implied_v,r,option_type) - Price ) / num_derivative
        iter_num = 0
        while abs(implied_v_update - implied_v) > 1e-100 :

            implied_v = implied_v_update
            num_derivative = (BlackScholesPrice(S,K,T,implied_v,r,option_type) - BlackScholesPrice(S,K,T,implied_v-delta_iv,r,option_type))/delta_iv
            implied_v_update = implied_v - ( BlackScholesPrice(S,K,T,implied_v,r,option_type) - Price ) / num_derivative        
            iter_num = iter_num + 1
            
            if iter_num > 100:
                
                break
        return implied_v_update
    
    def GetTheIVPlot(S,K,T,r,Price,option_type):
  
        KList = []
        VolList = []
        for i in np.arange(S/2,K*3/2,(S+K)/100):
            
            VolList.append(GetImpliedVFast(S,i,T,r,Price,option_type))
            KList.append(i)
        
        plt.figure(figsize=(2, 2))
        plt.plot(KList,VolList)
        plt.xticks(fontsize=3.3)
        plt.scatter(K,GetImpliedVFast(S,K,T,r,Price,option_type),color='r')
        plt.yticks(fontsize=3.3)
        plt.savefig('Temp.png',dpi=200)
        
            
    Newton_window = tk.Toplevel(window)
    Newton_window.title('牛顿法IV计算')
    Newton_window.geometry('800x400')


    
    tk.Label(Newton_window, text='现货价格S: ').place(x=10,y=10,anchor='nw')
    tk.Label(Newton_window, text='执行价格K: ').place(x=10,y=50,anchor='nw')
    tk.Label(Newton_window, text='到期天数T: ').place(x=10,y=90,anchor='nw')
    tk.Label(Newton_window, text='无风险利率r: ').place(x=10,y=130,anchor='nw')
    tk.Label(Newton_window, text='期权价格P: ').place(x=10,y=170,anchor='nw')
    tk.Label(Newton_window, text='Call or Put: ').place(x=10,y=210,anchor='nw')
    
    var_s = tk.DoubleVar()
    entry_s = tk.Entry(Newton_window, textvariable=var_s)
    entry_s.place(x=120,y=10,anchor='nw')
    
    var_k = tk.DoubleVar()
    entry_k = tk.Entry(Newton_window, textvariable=var_k)
    entry_k.place(x=120,y=50,anchor='nw')
    
    var_t = tk.DoubleVar()
    entry_t = tk.Entry(Newton_window, textvariable=var_t)
    entry_t.place(x=120,y=90,anchor='nw')
    
    var_r = tk.DoubleVar()
    entry_r = tk.Entry(Newton_window, textvariable=var_r)
    entry_r.place(x=120,y=130,anchor='nw')
    
    var_price = tk.DoubleVar()
    entry_price = tk.Entry(Newton_window, textvariable=var_price)
    entry_price.place(x=120,y=170,anchor='nw')
    
    var_cp = tk.StringVar()
    entry_sigma = tk.Entry(Newton_window, textvariable=var_cp)
    entry_sigma.place(x=120,y=210,anchor='nw')
    
    result_box = tk.Text(Newton_window,height=5,width=50)
    result_box.place(x=25,y=320) 
    
    canvas  = tk.Canvas(Newton_window, width=400, height=400)
    canvas.place(x=400,y=0,anchor='nw')
   
    
    
    
    b = tk.Button(Newton_window, 
    text='牛顿法计算隐含波动率:',      # 显示在按钮上的文字
    width=20, height=2, 
    command=GetImpliedV).place(x=110,y=250)
    
def main():
    global window
    window = tk.Tk()
    window.title('期权计算器')
    window.geometry('400x400')

    l1 = tk.Label(window, 
                  text='期权计算器 v2.0',    
                  font=('微软雅黑', 18),     # 字体和字体大小
                  width=15, height=2  # 标签长宽
                  )

    l2 = tk.Label(window, 
                  text='主要功能：',
                  font=('微软雅黑', 12),     # 字体和字体大小
                  width=50, height=2  # 标签长宽
                  )
    l3 = tk.Label(window, 
                  text='1.利用BS公式计算欧式期权价格',
                  font=('微软雅黑', 12),     # 字体和字体大小
                  width=50, height=2  # 标签长宽
                  )
    l4 = tk.Label(window, 
                  text='2.利用BS公式反推期权隐含波动率（牛顿）',
                  font=('微软雅黑', 12),     # 字体和字体大小
                  width=50, height=2  # 标签长宽
                  )
    l5 = tk.Label(window, 
                  text='作者：Kang',
                  font=('微软雅黑', 12),     # 字体和字体大小
                  width=50, height=2  # 标签长宽
                  )

    l1.pack()
    l2.pack()
    l3.pack()
    l4.pack()
    l5.pack()

    menubar = tk.Menu(window)
    filemenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='功能', menu=filemenu)
    filemenu.add_command(label='BS价格', command=BS_command)
    filemenu.add_command(label='牛顿IV', command=Newton_commant)
    window.config(menu=menubar)
    window.mainloop()

if __name__ == "__main__":
    global window
    main()
