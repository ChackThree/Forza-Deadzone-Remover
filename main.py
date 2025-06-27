#Github.com/ChackThree 
#NO SKIDS
import pygame, time, os, sys
import customtkinter as ctk
import vgamepad as vg
from CTkMessagebox import CTkMessagebox

class StickFixer:
  def __init__(self, gui=True, rep=10):
    os.system("cls")
    self.rep = rep
    self.threads = []
    self.gui = gui
    self.keepRunning = True
    self.current = None
    self.last_hat = (0, 0)
    self.last_x, self.last_y = 0.0, 0.0
    self.last_rx, self.last_ry = 0.0, 0.0 #is all this yap stupid? probly
    self.button_states = {}
    self.button_names = {
      0: vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
      1: vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
      2: vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
      3: vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
      4: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
      5: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
      6: vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
      7: vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
      8: vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
      9: vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
      10: vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE #i think this is correct, idrk tbh
    }
    self.doRun()

  def doRun(self):
    self.gp = vg.VX360Gamepad()
    print("Virtual Gamepad Connected")
    if self.gui == False:
      input("Make sure your controller isn't currently connected, if so restart the program.\nTurn on your controller and press enter when you have connected your controller...")
      print("Controllers Found: \n")
      controllers = self.getControllers()
      for gp in controllers:
        print(gp)
      print("\n")
      self.current = int(input("Enter controller number: "))
      self.currentName = controllers[self.current].split(" - ")[1]
      self.start()
    elif self.gui == True:
      self.startGui()

  def checkForTriggers(self):
    lt = self.joystick.get_axis(4)
    rt = self.joystick.get_axis(5)

    lt_val = max(0.0, min(lt, 1.0))
    rt_val = max(0.0, min(rt, 1.0))

    self.gp.left_trigger_float(value_float=lt_val)
    self.gp.right_trigger_float(value_float=rt_val)
    self.gp.update()

  def checkForRightStick(self):
    threshold = 0.001

    x_axis = self.joystick.get_axis(2)
    y_axis = self.joystick.get_axis(3)
    x_axis *= -1
    y_axis *= -1

    if abs(x_axis - self.last_rx) > threshold or abs(y_axis - self.last_ry) > threshold:
      self.gp.right_joystick_float(x_value_float=x_axis, y_value_float=y_axis)
      self.gp.update()

      self.last_rx, self.last_ry = x_axis, y_axis

  def checkForDpad(self):
    hatDict = {
      "(0, 1)" : vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
      "(0, -1)" : vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
      "(1, 0)" : vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
      "(-1, 0)" : vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
    }
    current_hat = self.joystick.get_hat(0)

    if current_hat != (0, 0) and self.last_hat == (0, 0):
      self.gp.press_button(button=hatDict[str(current_hat)])
      self.gp.update()

    if current_hat == (0, 0) and self.last_hat != (0, 0):
      self.gp.release_button(button=hatDict[str(self.last_hat)])
      self.gp.update()

    self.last_hat = current_hat

  def checkForButton(self):
    for i in range(self.joystick.get_numbuttons()):
      current = self.joystick.get_button(i)
      previous = self.button_states.get(i, 0)

      if current == 1 and previous == 0:
        self.gp.press_button(button=self.button_names.get(i))
        self.gp.update()

      if current == 0 and previous == 1:
        self.gp.release_button(button=self.button_names.get(i))
        self.gp.update()

      self.button_states[i] = current

  def checkForStick(self):
    threshold = 0.001

    x_axis = self.joystick.get_axis(0)
    y_axis = self.joystick.get_axis(1)
    intensity = (x_axis**2 + y_axis**2) ** 0.5

    if abs(x_axis - self.last_x) > threshold or abs(y_axis - self.last_y) > threshold:
      x2_axis = float(f"{x_axis:.2f}")
      dead = 0.30 #act dont touch this
      if x2_axis < 0:
        if x2_axis >= -0.70:
          xValue = x2_axis - dead
        else:
          xValue = -1.0
      elif x2_axis > 0:
        if x2_axis <= 0.70:
          xValue = x2_axis + dead
        else:
          xValue = 1.0
      else:
        xValue = 0.0
      self.gp.left_joystick_float(x_value_float=xValue, y_value_float=0.0)
      self.gp.update()
      self.last_x, self.last_y = x_axis, y_axis

  def getControllers(self):
    pygame.init()
    pygame.joystick.init()
    controllers = []
    for i in range(pygame.joystick.get_count()):
      joystick = pygame.joystick.Joystick(i)
      joystick.init()
      name = joystick.get_name()
      controllers.append(f"{i} - {name}")
    return controllers

  def menuCB(self, opt):
    opt = opt.split(" - ")
    self.current = int(opt[0])
    self.currentName = opt[1]

  def showMainGui(self):
    for widget in self.content.winfo_children():
      widget.destroy()

    label = ctk.CTkLabel(self.content, text="Main Menu", font=("Arial", 25), padx=10, pady=0, fg_color=self.content.cget("fg_color"), corner_radius=10)
    label.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(8, 0))

    controllers = self.getControllers()

    menuVar = ctk.StringVar(value=None)
    menu = ctk.CTkOptionMenu(
      self.content,
      values=controllers,
      command=self.menuCB,
      variable=menuVar
    )

    self.content.grid_rowconfigure(1, minsize=10)

    refreshBtn = ctk.CTkButton(self.content, text="Refresh", command=self.showMainGui)
    refreshBtn.grid(row=2, column=0, padx=70, sticky="w")

    self.content.grid_rowconfigure(3, minsize=5)

    menu.grid(row=4, column=0, padx=60, sticky="ew")

    self.content.grid_rowconfigure(5, minsize=115)

    startBtn = ctk.CTkButton(self.content, text="Start", command=self.start)
    startBtn.grid(row=6, column=0, padx=70, sticky="w")

    self.content.grid_rowconfigure(7, minsize=5)

    stopBtn = ctk.CTkButton(self.content, text="Stop", command=self.stop)
    stopBtn.grid(row=8, column=0, padx=70, sticky="w")

  def startGui(self):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    self.app = ctk.CTk()
    self.app.geometry("300x320")
    self.app.resizable(False, False)
    self.app.title("Stick Fixer v0.1")

    self.content = ctk.CTkFrame(self.app, corner_radius=10)
    self.content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    self.content.grid_columnconfigure(0, weight=1)

    self.app.grid_rowconfigure(0, weight=1)
    self.app.grid_columnconfigure(1, weight=1)

    self.showMainGui()
    
    self.app.mainloop()

  def stop(self):
    self.keepRunning = False
    print("Stopping all threads...")
    pygame.quit()
    if self.gui == True:
      CTkMessagebox(title="Stopped", message=f"The emulator has stopped using: {self.currentName}", icon="check")
    else:
      print(f"The emulator has stopped using: {self.currentName}")

  def getRep(self):
    return self.rep / 1000 #this doesnt even need to be a function lol but whatever

  def guiPolling(self):
    if not self.keepRunning: 
      return
    pygame.event.pump()
    self.checkForStick()
    self.checkForButton()
    self.checkForDpad()
    self.checkForRightStick()
    self.checkForTriggers()
    self.app.after(self.rep, self.guiPolling)

  def altPolling(self):
    print("Press CTRL+C to stop...")
    rep = self.getRep()
    while self.keepRunning:
      try:
        pygame.event.pump()
        self.checkForStick()
        self.checkForButton()
        self.checkForDpad()
        self.checkForRightStick()
        self.checkForTriggers()
        time.sleep(rep)
      except KeyboardInterrupt:
        self.stop()

  def start(self):
    if self.current != None or self.current != "":
      self.keepRunning = True
      self.joystick = pygame.joystick.Joystick(self.current)
      self.joystick.init()
      print(f"Got controller {self.current} ({self.currentName})...")
      if self.gui == True:
        self.app.after(0, self.guiPolling)
        print("All threads running...")
        CTkMessagebox(title="Success", message=f"The emulator is now using controller: {self.currentName}", icon="check")
      else:
        print(f"The emulator is now using controller: {self.currentName}")
        self.altPolling()
    else:
      if self.gui == True:
        CTkMessagebox(title="Error", message="You must select a controller before starting.", icon="cancel")
      print("No controller selected...")
  
if len(sys.argv) > 1:
  guiS = True
  t = 10
  sys.argv.pop(0) #im well aware of the correct way to do this, but i wanna do this way instead stfu
  args = sys.argv
  for arg in args:
    if arg == "ng" or arg == "nogui":
      guiS = False
    if arg.startswith("r"):
      try:
        t = int(arg.split(":")[1])
      except:
        print(f"Invalid rep value: {arg}")
  StickFixer(gui=guiS, rep=t)
else:
  StickFixer(gui=True)

#I also know that the above is not very efficient but i slopped it together in like 2mins so idc