from direct.task import Task
from direct.showbase.ShowBase import ShowBase, messenger
from direct.showbase import DirectObject
from panda3d.core import WindowProperties, Vec3, Vec4, lookAt, Quat
import serial, json, time
from threading import Thread

arduino = serial.Serial('/dev/ttyACM0')  # open serial port
VALUES = {"AngleX": float("0"), "AngleY": float("0"), "AngleZ": float("0"),
          "AccX": float("0"), "AccY": float("0"), "AccZ": float("0")}

def read_serial_values():
    global VALUES
    try:
        values_ant = json.loads(read_serial().decode().strip())
        values_act = json.loads(read_serial().decode().strip())
        VALUES = {"AngleX": calculateAcc(values_act["AngleX"], values_ant["AngleX"]), 
                    "AngleY": calculateAcc(values_act["AngleY"], values_ant["AngleY"]),
                    "AngleZ": calculateAcc(values_act["AngleZ"], values_ant["AngleZ"]),
                    "AccX"  : calculateAcc(values_act["AccX"], values_ant["AccX"]),
                    "AccY"  : calculateAcc(values_act["AccY"], values_ant["AccY"]),
                    "AccZ"  : calculateAcc(values_act["AccZ"], values_ant["AccZ"])}

    except Exception as e:
        VALUES = {"AngleX": float("0"), "AngleY": float("0"), "AngleZ": float("0"),
                    "AccX": float("0"), "AccY": float("0"), "AccZ": float("0")}
        

def calculateAcc(ant, act):
    return float(act) - float(ant)

def read_serial():
    data = arduino.readline()
    return data
    
class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.properties = WindowProperties()
        self.properties.setOrigin(1000, 1000)

        self.win.requestProperties(self.properties)

        self.setBackgroundColor(0.5, 0.5, 0.5, 0)
        
        # Add a ball model
        self.ball = self.loader.loadModel("./DiscoBall/DiscoBall.blend")
        self.ball.setTexture(self.loader.loadTexture("./DiscoBall/DiscoUV.png"))
        self.ball.reparentTo(self.render)
        self.ball.setScale(1,1,1)
        self.ball.setPos(0, 5, 0)
        self.speed = 20.0

        # Controll the camera (not moving)
        self.disableMouse()
        self.camera.setPos(0, -20, 0)
        self.camera.setHpr(0, 0, 0)

        # Add rotation overTime to the ball
        self.keyMap = {
            "up" : False,
            "down": False,
            "left": False,
            "right": False,
            "reset": False,
            "forward": False,
            "backward": False,
            "moveleft": False,
            "moveright": False,
        }

        # Añadir una manera de triggerear estas cosas con el movimiento del sensor

        self.accept("arrow_up", self.updateKeyMap, ["up", True])
        self.accept("arrow_up-up", self.updateKeyMap, ["up", False])
        self.accept("arrow_down", self.updateKeyMap, ["down", True])
        self.accept("arrow_down-up", self.updateKeyMap, ["down", False])
        self.accept("arrow_right", self.updateKeyMap, ["right", True])
        self.accept("arrow_right-up", self.updateKeyMap, ["right", False])
        self.accept("arrow_left", self.updateKeyMap, ["left", True])
        self.accept("arrow_left-up", self.updateKeyMap, ["left", False])
        self.accept("r", self.updateKeyMap, ["reset", True])
        self.accept("r-up", self.updateKeyMap, ["reset", False])

        self.accept("w", self.updateKeyMap, ["forward", True])
        self.accept("w-up", self.updateKeyMap, ["forward", False])
        self.accept("s", self.updateKeyMap, ["backward", True])
        self.accept("s-up", self.updateKeyMap, ["backward", False])
        self.accept("a", self.updateKeyMap, ["moveleft", True])
        self.accept("a-up", self.updateKeyMap, ["moveleft", False])
        self.accept("d", self.updateKeyMap, ["moveright", True])
        self.accept("d-up", self.updateKeyMap, ["moveright", False])


        self.updateTask = self.taskMgr.add(self.update, "update")

        
    def update(self, task):
        self.dt = globalClock.getDt()

        controller_info = VALUES
               
        hpr = Vec3(0, 0, 0)
        hpr += Vec3(
            # Esto es así por algún motivo
            -controller_info["AngleX"] * self.dt * self.speed, 
            +controller_info["AngleY"] * self.dt * self.speed, 
            +controller_info["AngleZ"] * self.dt * self.speed)        
        
        self.ball.setHpr(self.ball, hpr)
        
        ## Esto deberá ser lo mismo que el ángulo, pero con otra propiedad que ni idea de cual es
        ballpos = Vec3(0, 0, 0)
        ballpos += Vec3(
            # Esto es así por algún motivo
            -controller_info["AccX"], 
            +controller_info["AccY"], 
            +controller_info["AccZ"]) 
        
        # self.ball.setPos(self.ball.getPos() + ballpos)

        if self.keyMap["reset"]:
            self.ball.setHpr(0, 0, 0)
            self.ball.setPos(0, 5, 0)

        return task.cont
     
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState

    def rotateBall(self, task):
        self.ball.setH(self.ball,1)
        return Task.cont

def reader():
    while True:
        read_serial_values()

if __name__ == "__main__":
    Thread(target=reader).start()
    app = MyApp()
    app.run()