# 二维物理引擎|2D physics engine

**声明几件事**：

1. 本物理引擎按照YouTube上的教程制作，以我自己的水平很难写出来。[教程传送门](https://www.youtube.com/watch?v=lzI7QUyl66g&list=PLSlpr6o9vURwq3oxVZSimY8iC-cdd3kIs)
2. 本物理引擎用python编写，性能远不及静态语言编写的性能强悍，你可以使用cython，PyPy等来加速代码。
3. 本物理引擎有许多不足的地方，以后会不停优化，也考虑用C++编写。
4. 本物理引擎只能模拟刚体物理，并且由于摩擦力的难以处理，本物理引擎将摩擦力视为物体的固有属性(及此物体的摩擦力恒定，除非手动改变物体摩擦力属性)
5. 本文只讲怎么写出一个Dome
6. 以后版本会在此仓库更新，详细内容可以去作者的[博客](http://beisent.com)看看

本物理引擎主要以以下文件组成

| 文件               | 说明                                         |
| ------------------ | -------------------------------------------- |
| SimplyVector.py    | 此文件用于向量运算，以及与向量相关的功能     |
| SimplyTransform.py | 此文件用于向量旋转变换                       |
| SimplyMath.py      | 此文件用于数学操作                           |
| SimplyConverter.py | 此文件用于对向量转元组操作                   |
| SimplyWorld.py     | 此文件用于模拟物理世界的运行，例如解决碰撞   |
| SimplyBody.py      | 此文件用于创建物体，操作物体，获得物体的属性 |
| SimplyAABB.py      | 此文件用于存放最大致碰撞位置                 |
| SimplyManifold.py  | 此文件用于存放用于物体接触相关的内容         |
| Collisions.py      | 此文件用于处理碰撞相关的内容                 |

## 如何使用

首先要有一个绘图库，本文使用tkinter作为绘图库。

创建`DrawLib.py`文件，完成绘图库，由于我想使用鼠标来创建物体，所以实现一个获得鼠标位置的方法。

```python
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

```

后到正式使用物理引擎

创建Dome.py

1. 导入绘图库，随机数库，时间库(用于记录时间，因为SimplyWorld.Step需要传入时间)

   ```python
   #选用库
   import DrawLib
   from random import randint 
   import time 
   ```

2. 导入物理引擎库

   ```python
   #必用库
   from SimplyVector import SimplyVector 
   from SimplyBody import SimplyBody 
   from SimplyWorld import SimplyWorld
   from SimplyConverter import unpack
   from SimplyTransform import SimplyTransform
   ```

3. 初始化

   1. 初始化绘图库

      ```python
      gwidth = 400
      gheight=300
      graphics = DrawLib.Graphics(gwidth, gheight) 
      graphics.canvas_background("gray") 
      outline = "white"
      ```

   2. 初始化模拟世界

      ```python
      world = SimplyWorld()
      ```

   3. 在世界中添加物体

      ```python
      #创建3个固定的台面
      InherentStaticFriction,InherentDynamicFriction = 1,0.8#设定静摩擦力，滑动摩擦力
      """
      CreateBoxBody需要传入：
      width,height,Density,IsStatic,Restitution,InherentStaticFriction,InherentDynamicFriction
      宽度，高度，密度，否是是静态的，恢复系数，固有静摩擦，固有动摩擦
      返回元组：(bool是否创建成功,SimplyBody对象,物体类型)
      """
      body = SimplyBody.CreateBoxBody(gwidth-40,10,1,True,0.5,InherentStaticFriction,InherentDynamicFriction) #创建静态的Box刚体，此物理引擎可以处理多边形的碰撞不仅仅是矩形，你只需要在物理库中调整一下即可。
      if not body[0]: 
          raise Exception("创建失败") 
      body[1].MoveTo(SimplyVector(200,280))#SimplyBody.MoveTo方法传入SimplyVector向量，将物体TP到指定位置，物体的重心（几何中心）将位于终点
      world.AddBody(body[1])#添加物体至世界
      
      body = SimplyBody.CreateBoxBody(130,10,1,True,0.5,InherentStaticFriction,InherentDynamicFriction)
      if not body[0]:
          raise Exception("创建失败") 
      body[1].MoveTo(SimplyVector(80,150))
      body[1].RotateTo(3.1415926/6)#SimplyBody.RotateTo方法传入弧度向量，将物体以重心为轴旋转到指定角度
      world.AddBody(body[1])
      
      body = SimplyBody.CreateBoxBody(130,10,1,True,0.5,InherentStaticFriction,InherentDynamicFriction) 
      if not body[0]: 
          raise Exception("创建失败") 
      body[1].MoveTo(SimplyVector(250,100))
      body[1].RotateTo(-3.1415926/8)
      world.AddBody(body[1])
      ```

4. 构建主函数

   ```python
   #主函数
   def main():
       state = graphics.mouseLeftState#获取鼠标左键一开始状态
       stater = graphics.mouseRighState#获取鼠标右键一开始状态
    
       run = 1 
       t = 1#初始化模拟世界时间
       timebox = 0 #时间箱用于累加时间（用于实现显示FPS）
       t_list = []#时间列表（用于实现显示FPS）
       while run: 
           start = time.time()#获得程序初始时间
           graphics.clear_canvas() #清除画布
   
           #创建物体并添加到世界
           a = graphics.mouseLeftState
           #当鼠标左键完成一次点击后创建一个Box
           if a != state:
               state = a
               if a != True:
                   Position = graphics.mouse
                   body = SimplyBody.CreateBoxBody(randint(20,30),randint(20,30),10,False,0.5,InherentStaticFriction,InherentDynamicFriction) 
                   if not body[0]:
                       raise Exception("创建Box失败") 
                   body[1].MoveTo(Position)
                   world.AddBody(body[1])
                   
           b = graphics.mouseRighState
           #当鼠标左键完成一次点击后创建一个Circle
           if b != stater:
               stater = b
               if b != True:
                   Position = graphics.mouse
                   """
   CreateCircleBody需要传入：
   Radius,Density,IsStatic,Restitution,InherentStaticFriction,InherentDynamicFriction
   半径，密度，否是是静态的，恢复系数，固有静摩擦，固有动摩擦
   返回元组：(bool是否创建成功,SimplyBody对象,物体类型)
   """
                   body = SimplyBody.CreateCircleBody(randint(5,20),10,False,0.5,InherentStaticFriction,InherentDynamicFriction) 
                   if not body[0]: 
                       raise Exception("创建Circle失败") 
                   body[1].MoveTo(Position)
                   world.AddBody(body[1])
   
           #从世界中获得物体信息并绘制 
           for i in range(world.BodyCount()):
               getOrNot,body = world.GetBody(i)#GetBody方法返回元组（是否获得成功，SimplyBody对象）
               if not getOrNot:
                   raise Exception("获取物体失败")
               if body.ShapeType == "Box":
                   if body.IsStatic:
                       graphics.draw_polygon_1(unpack((body.GetTransformedVertices())),color='red') #GetTransformedVertices()方法用于返回多边形时实的顶点坐标，GetTransformedVertices()将返回一个由SimplyVector组成的列表，unpack将列表中的SimplyVector转为元组再放回一个由元组组成的列表
                   else:
                       graphics.draw_polygon_1(unpack((body.GetTransformedVertices())),color=outline) 
               if body.ShapeType == "Circle":
                   if body.IsStatic:
                       graphics.draw_circle(body.Position.x,body.Position.y,body.Radius,fill="black",color='red') 
                   else:
                       va = SimplyVector(0,0)
                       vb = SimplyVector(body.Radius,0)
                       transform = SimplyTransform(body.Position,body.angle)
                       va = SimplyVector.transform(va,transform)
                       vb = SimplyVector.transform(vb,transform)                   
                       graphics.draw_circle(body.Position.x,body.Position.y,body.Radius,fill="black",color=outline) 
                       graphics.draw_line(va.x,va.y,vb.x,vb.y)
   
           world.Step(t,4)#更新世界SimplyWorld.Step(传入模拟时间（float），将一次模拟分为几次进行（int）)
   
           try:
               for i in range(world.BodyCount()):
                   bool_result,body = world.GetBody(i)
                   box = body.GetAABB()
                   if(box.Min.y>gheight):#如果物体掉出窗口下方，在世界上删除物体
                       world.RemoveBody(body)#SimplyWorld.RemoveBody（SimplyBody对象）
           except:
               continue
   
           graphics.update()#更新绘图
           stop = time.time()#结束时间
           t = stop - start#模拟时间
           timebox +=t #累加模拟时间
   
           if len(t_list) == 5:
               t_list.pop(0)
           if t!=0:
               t_list.append(t)
   
           if timebox>0.5 :#当累积的模拟时间大于0.5时打印FPS和物体数量
               timebox = 0
               try:  
                   print(f"{1/sum(t_list)*5:.2f}",f"{world.BodyCount()}")
               except:
                   continue       
   ```

5. 执行主函数

   ```
   main()
   ```

   

完整代码`Dome.py`

```python
#选用库
import DrawLib #导入绘图库
from random import randint #导入随机数函数
import time #导入时间模块

#必用库
from SimplyVector import SimplyVector #导入平面向量类
from SimplyBody import SimplyBody #导入平面刚体类
from SimplyWorld import SimplyWorld
from SimplyConverter import unpack
from SimplyTransform import SimplyTransform


#初始化
#初始化绘图
gwidth = 400
gheight=300
graphics = DrawLib.Graphics(gwidth, gheight) 
graphics.canvas_background("gray") 
outline = "white"

#初始化世界
world = SimplyWorld()
"""
CreateBoxBody需要传入：
width,height,Density,IsStatic,Restitution,InherentStaticFriction,InherentDynamicFriction
宽度，高度，密度，否是是静态的，恢复系数，固有静摩擦，固有动摩擦
"""
InherentStaticFriction,InherentDynamicFriction = 1,0.8
body = SimplyBody.CreateBoxBody(gwidth-40,10,1,True,0.5,InherentStaticFriction,InherentDynamicFriction) 
if not body[0]: 
    raise Exception("创建失败") 
body[1].MoveTo(SimplyVector(200,280))
world.AddBody(body[1])

body = SimplyBody.CreateBoxBody(130,10,1,True,0.5,InherentStaticFriction,InherentDynamicFriction)
if not body[0]:
    raise Exception("创建失败") 
body[1].MoveTo(SimplyVector(80,150))
body[1].RotateTo(3.1415926/6)
world.AddBody(body[1])

body = SimplyBody.CreateBoxBody(130,10,1,True,0.5,InherentStaticFriction,InherentDynamicFriction) 
if not body[0]: 
    raise Exception("创建失败") 
body[1].MoveTo(SimplyVector(250,100))
body[1].RotateTo(-3.1415926/8)
world.AddBody(body[1])


#主函数
def main():
    state = graphics.mouseLeftState
    stater = graphics.mouseRighState
 
    run = 1 
    t = 1
    timebox = 0 
    t_list = []
    while run: 
        start = time.time()
        graphics.clear_canvas() 

        #创建物体并添加到世界
        a = graphics.mouseLeftState  
        if a != state:
            state = a
            if a != True:
                Position = graphics.mouse
                body = SimplyBody.CreateBoxBody(randint(20,30),randint(20,30),10,False,0.5,InherentStaticFriction,InherentDynamicFriction) 
                if not body[0]:
                    raise Exception("创建Box失败") 
                body[1].MoveTo(Position)
                world.AddBody(body[1])
        b = graphics.mouseRighState
        if b != stater:
            stater = b
            if b != True:
                Position = graphics.mouse
                body = SimplyBody.CreateBoxBody(randint(100,130),randint(20,30),10,False,0.5,10,9) 
                #body = SimplyBody.CreateCircleBody(randint(5,20),10,False,0.5,InherentStaticFriction,InherentDynamicFriction) 
                if not body[0]: 
                    raise Exception("创建Circle失败") 
                body[1].MoveTo(Position)
                world.AddBody(body[1])

        #从世界中获得物体信息并绘制 
        for i in range(world.BodyCount()):
            getOrNot,body = world.GetBody(i)
            if not getOrNot:
                raise Exception("获取物体失败")
            if body.ShapeType == "Box":
                if body.IsStatic:
                    graphics.draw_polygon_1(unpack((body.GetTransformedVertices())),color='red') 
                else:
                    graphics.draw_polygon_1(unpack((body.GetTransformedVertices())),color=outline) 
            if body.ShapeType == "Circle":
                if body.IsStatic:
                    graphics.draw_circle(body.Position.x,body.Position.y,body.Radius,fill="black",color='red') 
                else:
                    va = SimplyVector(0,0)
                    vb = SimplyVector(body.Radius,0)
                    transform = SimplyTransform(body.Position,body.angle)
                    va = SimplyVector.transform(va,transform)
                    vb = SimplyVector.transform(vb,transform)                   
                    graphics.draw_circle(body.Position.x,body.Position.y,body.Radius,fill="black",color=outline) 
                    graphics.draw_line(va.x,va.y,vb.x,vb.y)

        world.Step(t,4)#更新世界

        try:
            for i in range(world.BodyCount()):
                bool_result,body = world.GetBody(i)
                box = body.GetAABB()
                if(box.Min.y>gheight):
                    world.RemoveBody(body)
        except:
            continue

        graphics.update()
        stop = time.time()
        t = stop - start
        timebox +=t 

        if len(t_list) == 5:
            t_list.pop(0)
        if t!=0:
            t_list.append(t)

        if timebox>0.5 :
            timebox = 0
            try:  
                print(f"{1/sum(t_list)*5:.2f}",f"{world.BodyCount()}")
            except:
                continue       

main()

```

此文章的所有代码均可从博主的[GitHub](https://github.com/Yang-Junjie/2D-physics-engine)下载
