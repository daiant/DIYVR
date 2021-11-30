from direct.task import Task
from direct.showbase.ShowBase import ShowBase, messenger
from direct.showbase import DirectObject
from panda3d.core import WindowProperties, Vec3, Vec4, lookAt, Quat
import serial, json

arduino = serial.Serial('/dev/ttyACM0')  # open serial port


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
        self.speed = 50.0

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
        controller_info = self.read_serial_values()
        if float(controller_info["x"]) < 0:
            messenger.send('arrow_right-up')
            messenger.send('arrow_left')
        if float(controller_info["x"]) > 0:
            messenger.send('arrow_left-up')
            messenger.send('arrow_right')
        if float(controller_info["y"]) < 0:
            messenger.send('arrow_up-up')
            messenger.send('arrow_down')
        if float(controller_info["y"]) > 0:
            messenger.send('arrow_down-up')
            messenger.send('arrow_up')
 
        hpr = Vec3(0, 0, 0)
        
        if self.keyMap["up"]:
            hpr += Vec3(0, -self.dt * self.speed, 0)
        if self.keyMap["down"]:
            hpr += Vec3(0, self.dt * self.speed, 0)
        if self.keyMap["left"]:
            hpr += Vec3(-self.dt * self.speed, 0, 0)
        if self.keyMap["right"]:
            hpr += Vec3(self.dt * self.speed, 0, 0)
        if self.keyMap["reset"]:
            self.ball.setHpr(0, 0, 0)
            self.ball.setPos(0, 5, 0)

        deltaQuat = Quat()
        deltaQuat.setHpr(hpr)
        oldQuat = self.ball.getQuat()
        newQuat = oldQuat * deltaQuat
        self.ball.setQuat(newQuat)

        ballpos = Vec3(0, 0, 0)
        if self.keyMap["forward"]:
            ballpos += Vec3(0, 0, self.dt * self.speed / 10)
        if self.keyMap["backward"]:
            ballpos += Vec3(0, 0, -self.dt * self.speed / 10)
        if self.keyMap["moveright"]:
            ballpos += Vec3(self.dt * self.speed / 10, 0, 0)
        if self.keyMap["moveleft"]:
            ballpos += Vec3(-self.dt * self.speed / 10, 0, 0)
        
        self.ball.setPos(self.ball.getPos() + ballpos)

        return task.cont
     
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState

    def rotateBall(self, task):
        self.ball.setH(self.ball,1)
        return Task.cont

    def read_serial_values(self):
        try:
            values = json.loads(self.read_serial().decode().strip())
        except:
            values = {"x": "0", "y": "0", "z": "0"}
        return values

    def read_serial(self):
        data = arduino.readline()
        return data
app = MyApp()
app.run()