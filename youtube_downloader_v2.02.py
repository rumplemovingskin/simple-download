# YouTube Video Downloader
# v2.02
#
# User enters a YouTube URL
# Function returns a list of video stream options
# User selects an option and initiates download

from tkinter import *
from pytube import YouTube
from tkinter import filedialog
from tkinter import messagebox
import threading
import time
import sys
import os

root = Tk()
root.geometry('1000x600+100+100')
root.resizable(True, True) # Allow resizing in both directions
root.title("YouTube Video Downloader")

# Frame to hold the UI elements
frame = Frame(root, width=1000, height=600)
frame.pack(pady=(50, 0)) 

Label(frame, text='YouTube Video Downloader', font='arial 20 bold').pack()

# Instructions label below the main label
Label(frame, text='Enter your YouTube video link and click "SCAN VIDEO".\n Scanning may take up to a minute.', font='arial 10', wraplength=500, justify=CENTER).pack(pady=(0,5))

link = StringVar()
streams_checkboxes = []
status_label = Label(frame, text='', width=50, height=2, font='arial 15 bold', bg='#dddddd', relief=SUNKEN)
status_label.pack(pady=10)

Label(frame, text='Paste Link Here:', font='arial 12 bold').pack(pady=(5,0))
link_enter = Entry(frame, width=70, textvariable=link).pack()

def show_streams(retries=3):
    global streams_checkboxes
    if retries == 0:
        status_label.config(text="Please Check The URL And Try Again.", fg="red")  # Update status label with red text
        return
    try:
        status_label.config(text="Scanning Video Properties...", fg="blue")  # Update status label with blue text
        root.update()  # Update the GUI to display the status label change
        url = YouTube(str(link.get()))
        video_title = Label(frame, text=f'Title: {url.title}', font='arial 10 bold', fg='#333333')
        video_title.pack(pady=(10,0))
        video_runtime = Label(frame, text=f'Runtime: {url.length // 60}:{url.length % 60}', font='arial 10 bold', fg='#333333')
        video_runtime.pack(pady=0)
        streams_frame = Frame(frame)  # Create a new frame to hold the streams
        streams_frame.pack(pady=0)
        streams = url.streams.filter(progressive=True)
        for i, stream in enumerate(streams, start=1):
            var = IntVar()
            stream_label = f"Resolution: {stream.resolution}, Format: {stream.mime_type}"
            c = Checkbutton(streams_frame, text=stream_label, variable=var)
            c.pack(anchor=W)
            streams_checkboxes.append((var, stream))
        status_label.config(text="Results Found.", fg="green")  # Update status label with green text
        download_button.pack(pady=5)  # Show the "DOWNLOAD SELECTED FORMAT" button
    except Exception as e:
        print(e)
        time.sleep(3)  # Wait for 3 seconds
        show_streams(retries-1)

def download_selected():
    url = YouTube(str(link.get()))
    download_path = filedialog.askdirectory()
    for var, stream in streams_checkboxes:
        if var.get() == 1:
            t = threading.Thread(target=download_stream, args=(stream, download_path))
            t.start()

def download_stream(stream, download_path):
    try:
        status_label.config(text=f"Downloading {stream.resolution}/{stream.mime_type}...", fg="blue")  # Update status label with blue text
        root.update()  # Update the GUI to display the status label change
        stream.download(download_path)
        status_label.config(text=f"{stream.resolution}/{stream.mime_type} Downloaded Successfully!\n Click Restart App To Download A New Video.", fg="green")  # Update status label with green text
    except Exception as e:
        print(e)
        status_label.config(text=f"Failed to download {stream.resolution}, {stream.mime_type}.", fg="red")  # Update status label with red text

# Function to close and restart the script
def restart_script():
    python = sys.executable
    # Use the sys.executable to get the path of the current Python interpreter
    # and then use it to restart the script with the same arguments
    # as the original script
    args = sys.argv[:]
    args.insert(0, python)
    # Close the Tkinter window
    root.destroy()
    # Restart the script
    os.execvp(python, args)

# "SCAN URL" button
scan_button = Button(frame, text="SCAN VIDEO", font='arial 10 bold', bg='#b3d4f5', command=show_streams)
scan_button.pack(pady=10)

# "DOWNLOAD SELECTED FORMAT" button but hide it initially
download_button = Button(frame, text="DOWNLOAD SELECTED FORMAT", font='arial 10 bold', bg='#81eb9b', command=download_selected)
download_button.pack_forget()

# Button that calls the restart_script function when clicked
restart_button = Button(frame, text="RESTART APP", font='arial 8 bold', bg='red', fg="white", command=restart_script)
restart_button.pack(pady=5)


root.mainloop()
