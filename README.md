# Controller Emulator and Modifier

This is an **open source** program that was *quickly* designed to remove/improve the deadzone in Forza Horizon 5.

This project was specifically created to use with <a href="https://makerworld.com/en/models/977748-driving-simulator-v2?from=search#profileId-950873">**this**</a> 3D printed steering wheel. I recently printed this wheel, but was disappointed to find that you have to steer about 1.5x to 2x as much as you should need (oversteering). This makes it very difficult to drive, and no amount of messing with the inner and outer dead zones will get me even close to fixing this issue. That's why I decided to make this program, which works fairly well. This is the first version and isn't perfect. If you encounter any issues, please open in the issues tab.

## What this program does:

- Emulates all controller actions  
- "Amplifies" the left stick axis values  
- Provides 0 deadzone for Forza Horizon 5  
- Clean & simple user-friendly GUI (with options for no GUI)  

## How to use:

- Go to advanced control settings in FH5 and reset them all to default (or just default the inner and outer steering deadzones).
- Download the exe from the releases page, OR run the code yourself via Python.
- You first start the program, then you connect your controller to your PC. Next, select your controller within the program (dropdown menu) and press start (or press 'enter' in nogui mode).
- The program is now emulating your controller; you must keep the program running for it to work (obviously).
- Press Stop button to end emulation or CTRL+C in nogui version.

## Command Line Arguments:

- There are two optional command-line arguments you can use:
  - `nogui` or alternatively, `ng:` runs the program without a GUI (still a bit buggy).
  - `r:<ms>`: changes how often (in ms) the emulator checks your controller inputs.  
    Smaller values = theoretically less input lag, but it may end up lagging the program if your values are too low (faster refreshes).

## Notes & Tips:

- I recommend not changing the "rep" value (which is the `r:<ms>` arg).
- Feel free to modify some of the values in the code if NEEDED, but don't skid my program.
- I also recommend setting an inner deadzone in the game settings (even though the whole point of the program is 0 deadzone). It's very tricky to drive without an inner deadzone, so I would do at least 30–35 on the inside deadzone.
- If the program stops detecting your inputs:
  - Try pressing the refresh button.
  - If that doesn't work: turn off the controller → restart the program → turn on the controller → select it again.
  - If you're using the nogui version, you have to do this every time.
- **MAKE SURE YOU INSTALL VIGEMBUS DRIVERS!!!**
  - You can install them <a href="https://vigembus.com/download/">**here**</a>

---

THIS IS VERSION 1. THERE WILL BE BUGS!  
More updates in the future, probably.

NO SKIDDING ALLOWED!!!
