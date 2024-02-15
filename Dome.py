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
