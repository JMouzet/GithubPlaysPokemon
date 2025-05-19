from pyboy import PyBoy
import os
import signal
from dotenv import load_dotenv
import sqlite3


# Load environment variables
load_dotenv()
DELAY = int(os.getenv("SCREEN_DELAY", 10))

# Saves backup function
def roll_states():
    # Delete backup 2
    if os.path.exists("/save/game.gb.state.2"):
        os.remove("/save/game.gb.state.2")
    # Rename backup 1 to backup 2
    if os.path.exists("/save/game.gb.state.1"):
        os.rename("/save/game.gb.state.1", "/save/game.gb.state.2")
    # Rename current to backup 1
    if os.path.exists("/save/game.gb.state"):
        os.rename("/save/game.gb.state", "/save/game.gb.state.1")


# Delete the screenshot
if os.path.exists("/shared/screen/screen.png"):
    os.remove("/shared/screen/screen.png")
# In case of an error, ensure the API shows the offline screen

# Catch SIGINT and SIGTERM signals to allow saving the state before exiting
class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self, signum, frame):
    self.kill_now = True


# Create inputs database if not exists
os.system("python init-db.py")

# Connect to the database
conn = sqlite3.connect("/shared/db/inputs.db")
cur = conn.cursor()


# Start the PyBoy emulator
if os.path.exists("/rom/game.gbc"):
    pyboy = PyBoy("./rom/game.gbc", window="null")
elif os.path.exists("/rom/game.gb"):
    pyboy = PyBoy("./rom/game.gb", window="null")
else:
    print("No ROM found")
    exit(1)

pyboy.set_emulation_speed(1)

# Load a save state if found
try:
    with open("/save/game.gb.state", "rb") as f:
        pyboy.load_state(f)
except:
    pass

frame = 0
wait = 0

if __name__ == "__main__":
    # Start the kill catcher
    killer = GracefulKiller()

    while not killer.kill_now:
        # Run the next frame
        pyboy.tick()

        # Wait for the last button to be released
        if(wait == 0):
            # Check for user input
            cur.execute("SELECT id, input FROM inputs ORDER BY id ASC LIMIT 1")
            row = cur.fetchone()
            if row:
                id, input = row

                wait = 2

                # Send the input in-game
                pyboy.button(input, wait)

                # Delete the input from the database
                cur.execute("DELETE FROM inputs WHERE id IN (SELECT id FROM inputs ORDER BY id ASC LIMIT 1)")
                conn.commit()
        else:
            wait -= 1

        # Take a screenshot every DELAY seconds
        if frame % (60 * DELAY) == 0:
            image = pyboy.screen.image
            type(image)
            image.save(f"/shared/screen/screen.png")
            frame -= 60 * DELAY

        # Save the current state every 10 minutes
        if frame % (60 * 10) == 0:
            # Roll the states
            roll_states()
            # Save the current state
            with open("/save/game.gb.state", "wb") as f:
                pyboy.save_state(f)
        
        frame += 1
    
    # Roll the states
    roll_states()
    # Save the current state
    with open("/save/game.gb.state", "wb") as f:
        pyboy.save_state(f)

    # Delete the screenshot
    if os.path.exists("/shared/screen/screen.png"):
        os.remove("/shared/screen/screen.png")
    # This will force the API to show the offline screen

    # Close the database connection
    conn.close()

    # Stop the emulator without saving
    pyboy.stop(False)
