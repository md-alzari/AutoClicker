# Built-in Modules
import time
import os
import sys
import random
import math
import traceback
import subprocess
import ctypes

# Configuration
InputEventsFile = os.path.join(os.path.dirname(__file__), "Clicks.txt")
StopKey = "esc"
bUseCustomLoops = False
DefaultLoops = 0
bUseCustomWindow = False
DefaultWindow = "CROSSFIRE"
AutoExit = True

# Advanced
UseDelayes = True
MoveDurationRange = (0.005, 0.03) 
ClickDurationRange = (0.05, 0.3)
LoopDurationRange = (0.05, 0.3)

# Human Curve
UseCurve = False
BasePoints = 2 
MaxPoints = 7 

# DO NOT EDIT
RequiredModules = ['pyautogui', 'keyboard', 'pygetwindow', 'pywin32']
JitterAmount = 0.7  
MicroMovementChance = 0.03  
MinCPU_Delay = 0.005
CPU_Time = 0.001

AppWindow = None

# ADMIN CHECK
def IsAdmin():
 try:
     return ctypes.windll.shell32.IsUserAnAdmin()
 except:
        return False
 
if not IsAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

def ImportModle(module):
    try:
        __import__(module)
        print(f"Module {module} is already installed")
    except ImportError:
        print(f"Installing {module}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            print(f"Successfully installed {module}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {module}: {e}")
            input("Press Enter to exit...")
            sys.exit(1)

for module in RequiredModules:
    ImportModle(module)

os.system('cls' if os.name == 'nt' else 'clear')

def Error(message, TraceBack=False):
    print(f"Error: {message}")
    if TraceBack:
      traceback.print_exc()

    input("Press Enter to exit...")

# Third-party Modules
import pyautogui
import keyboard
pyautogui.FAILSAFE = False

# Functions
def HumanMove(Target):

    def CalculatePointsNumber(Start, End):         
      Distance = math.dist(Start, End)
      return min(MaxPoints, max(BasePoints, int(Distance / 10)))
  
    def HumanCurve(Start, End):     
      
     PointsCount = CalculatePointsNumber(Start, End)
     ControlPoints = [
          (Start[0] + (End[0] - Start[0]) * random.uniform(0.2, 0.4), 
           Start[1] + (End[1] - Start[1]) * random.uniform(0.2, 0.4)),
          (Start[0] + (End[0] - Start[0]) * random.uniform(0.6, 0.8), 
           Start[1] + (End[1] - Start[1]) * random.uniform(0.6, 0.8))
         ]

     points = []
     for t in [i/PointsCount for i in range(PointsCount+1)]:
        x = (1-t)**3 * Start[0] + 3*(1-t)**2*t*ControlPoints[0][0] + 3*(1-t)*t**2*ControlPoints[1][0] + t**3*End[0]
        y = (1-t)**3 * Start[1] + 3*(1-t)**2*t*ControlPoints[0][1] + 3*(1-t)*t**2*ControlPoints[1][1] + t**3*End[1]

        points.append((x + random.uniform(-JitterAmount, JitterAmount),
                       y + random.uniform(-JitterAmount, JitterAmount)))
    
     return points

    if (UseDelayes): MoveDuration = random.uniform(*MoveDurationRange)-CPU_Time  
    else: MoveDuration = 0.0
    if (not UseCurve):
          # Move Directly
          pyautogui.moveTo(*Target, duration=MoveDuration)   
    else:
      Points = HumanCurve(pyautogui.position(), Target) 
      
      # Simulate Human Curve
      TimePerPoint = max(0.001, (MoveDuration / len(Points)) - CPU_Time)
      for Point in Points:
       pyautogui.moveTo(*Point, duration=0)    
       time.sleep(TimePerPoint* random.uniform(0.1, 0.9))

       # Occasionally add tiny micro-movements
       if random.random() < MicroMovementChance:
             pyautogui.moveRel(
                 random.uniform(-1, 1),
                 random.uniform(-1, 1),
                 duration=random.uniform(0.02, 0.05)
             )            
  
def HumanClick(Target): 
    if (UseDelayes): ClickDuration = random.uniform(*ClickDurationRange) - CPU_Time
    else: ClickDuration = 0.0
    
    # Mouse down
    pyautogui.mouseDown()

    # Add small movements during click hold
    StartTime = time.time()
    while UseDelayes and ((time.time() - StartTime) < ClickDuration):
        time.sleep(MinCPU_Delay)   
        pyautogui.moveRel(
            random.uniform(-0.5, 0.5),
            random.uniform(-0.5, 0.5),
            duration=0.01
        )

    # Mouse Up             
    pyautogui.mouseUp()
 
def SimulateInputEvents(Events, Loops):
   
   # Loop broken flag
   LoopBroken = False
   
   def BreakLoop():
      nonlocal LoopBroken 
      LoopBroken = True
      print("\nStopping Now")
   
   keyboard.add_hotkey(StopKey, BreakLoop)
    
   # Start the simulation Loop
   StartTime = time.localtime()
   print(f"\nRunning Script, Current time: {time.strftime('%a %H:%M', StartTime)}")

   try:
      CurrentLoop = 0
      while not LoopBroken and (Loops == 0 or CurrentLoop < Loops):                
         CurrentLoop += 1    
         print(f"Current Loop: {CurrentLoop}")         

         for Event in Events:
                if LoopBroken:   
                    print("\rStopped by user request")
                    FinishTime = time.localtime()
                    print(f"\nScript finished, Current time: {time.strftime('%a %H:%M', FinishTime)}")
                    ElapsedTime = int(time.mktime(FinishTime) - time.mktime(StartTime))
                    print(f"\rPlayed For: {ElapsedTime // 86400} days, {ElapsedTime // 3600 % 24} hours, and {ElapsedTime // 60 % 60} minutes")
                    if (not AutoExit): input("\nPress Enter to exit...")                     
                    return
                
                if not FocusOnWindow():
                    return

                X, Y, Action= Event

                # Screen Size
                ScreenWidth, ScreenHeight = pyautogui.size()
                ScreenWidth //= 2  
                ScreenHeight //= 2

                # Compute target position
                TargetPosition = (ScreenWidth + X, ScreenHeight + Y)
                               
                # Move Mouse
                HumanMove(TargetPosition)
                if Action == 'Left Click':
                  HumanClick(TargetPosition)
                
         if(UseDelayes): time.sleep(random.uniform(*LoopDurationRange))

   # On the end unhook stop key.
   finally:
    keyboard.unhook_all()

def GetInputEventsFromFile(filename):
      
    events = []
    if not os.path.exists(filename):
      raise FileNotFoundError(f"Input file {filename} not found!")
    
    # Open file
    with open(filename, 'r') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line:
                continue
            parts = [part.strip() for part in line.split(',')]
            if len(parts) != 3:
                print(f"Skipping invalid line {line_num}: {line}")
                continue
            try:
                x, y, action = parts
                events.append((int(x), int(y), action))
            except ValueError:
                print(f"Skipping line {line_num} with invalid format: {line}")

    # Return found events            
    return events

def FocusOnWindow():     
    try:     
        if not AppWindow :
            print(f"Invalid App Window")
            return False
        
        if AppWindow.isMinimized:
            AppWindow.restore()
        AppWindow.activate()
        time.sleep(0.5)
        return True

    except Exception as e:
        print(f"Error focusing app window: {e}")
        return False

def RefreshAppWindow():    
    global AppWindow
    
    # Get all windows and try to find a matching title
    FoundWindows = [win for win in pyautogui.getAllWindows() if win.title.strip()]
    Selection = -1
    if (not bUseCustomWindow):
      # Try to find default window
     Selection = next((i for i, win in enumerate(FoundWindows) if DefaultWindow.lower() in win.title.lower()), -1)

    if (not Selection >= 0):
     for i, win in enumerate(FoundWindows, 1):
      print(f"{i}. {win.title}") 
    
    # Try to get an input of user to select a window
    try:
          if (not Selection >= 0): 
              Selection = int(input("Enter the number of the app window: ")) -1
          if 0 <= Selection < len(FoundWindows):
              SelectedTitle = FoundWindows[Selection].title
              windows = pyautogui.getWindowsWithTitle(SelectedTitle)
              if windows:
                AppWindow = windows[0]  # Store single window object
                print(f"\nSelected window: {SelectedTitle}")
                return True
          else:
            raise IndexError

    except (ValueError, IndexError):
          Error("Invalid selection!")
          return    
         
    # Validate App Window   
    if not AppWindow:
         Error("Invalid App Window, please try again")

def main():
    # Settings
    print(f"Input events file: {InputEventsFile}")
    print(f"Stop Key: {StopKey.upper()}\n")
      
    # Input Events
    try:
         InputEvents = GetInputEventsFromFile(InputEventsFile)
    except FileNotFoundError as e:
         Error(e)
         return
      
    # App Window
    RefreshAppWindow()

    # Loops Count
    try:
        if (bUseCustomLoops): Loops = int(input("\nEnter number of loops (0 for infinite): "))
        else: Loops = DefaultLoops
    except ValueError:
         print("Invalid input. Using default value: 0.")
         Loops = 0

    # Starting ...
    print("\nStarting in 3 seconds... Ensure app window is visible!")
    for i in range(3, 0, -1):
       print(f"{i}...")
       time.sleep(1)
    print("GO!")

    # Excute Simulation
    SimulateInputEvents(InputEvents, Loops)   

if __name__ == "__main__":
    try:          
        main()
    except Exception as e:
        Error("Critical error occurred", True)
