import tkinter as tk
from SimplyVector import SimplyVector
flag = False
class Graphics:
    def __init__(self, width, height):
        self.root = tk.Tk()
        self.root.title("SimplyEngine")#窗口标题
        self.width = width#窗口宽度
        self.height = height#窗口高度
        self.create_canvas()
        self.mouse = SimplyVector(0,0)
        self.mouseLeftState = False
        self.mouseRighState = False
        
        self.canvas.bind(sequence="<Button-1>", func=self.mouse_left_down)
        self.canvas.bind("<ButtonRelease-1>", func=self.mouse_left_up)
        self.canvas.bind(sequence="<Button-3>", func=self.mouse_Righ_down)
        self.canvas.bind("<ButtonRelease-3>", func=self.mouse_Righ_up)

    def create_canvas(self):#创建窗口函数
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        # 让画布获取焦点
        self.canvas.focus_set()
        # 绑定鼠标左键事件
        
    def canvas_background(self, color):#设置背景颜色
        self.canvas.configure(bg=color)

    def draw_line(self, x1, y1, x2, y2, color="white"):#绘制线段
        self.canvas.create_line(x1, y1, x2, y2, fill=color)
        
    
    def draw_circle(self, x, y, radius, color="black", fill=None):#绘制圆形
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=fill, outline=color)
    

    def draw_polygon_1(self, *points, color="black", fill=None):#使用多边形顶点绘制多边形
        self.canvas.create_polygon(points, fill=fill, outline=color)
    

    def clear_canvas(self):#清除画布
        self.canvas.delete("all")

    def update(self):#更新画布
        self.root.update()

    # 判断鼠标左键是否按下的方法
    def mouse_left_down(self, event):
        self.mouseLeftState = True
        self.mouse =  SimplyVector(event.x,event.y)
        
    def mouse_left_up(self,event):
        self.mouseLeftState = False

    def mouse_Righ_down(self, event):
         self.mouseRighState = True
         self.mouse =  SimplyVector(event.x,event.y)
        
    def mouse_Righ_up(self,event):
         self.mouseRighState = False
