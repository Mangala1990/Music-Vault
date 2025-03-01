import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
from pygame import mixer
root = tk.ThemedTk()
root.get_themes()                 
root.set_theme("plastik")
statusbar = ttk.Label(root, text="Welcome to Music Vault", justify='center', relief=FLAT, anchor=CENTER, background='violet', font='Times 14 bold')
statusbar.pack(side=TOP, fill=Y)
#Create the menubar
menubar = Menu(root)
root.config(menu=menubar)
#Create the submenu
subMenu = Menu(menubar, tearoff=0)
playlist = []
# Playlist - contains the full path + filename
# Playlistbox - contains just the filename
# Fullpath + filename is required to play the music inside play_music load function

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)
    mixer.music.queue(filename_path)

def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1

def browse_folder():
    global myfolder_path
    myfolder_path = filedialog.askdirectory()
    getFolderPlaylist(myfolder_path)

def getFolderPlaylist(myfolder):
    mp3s = []
    ls = os.listdir(myfolder)
    index = 0
    for item in ls:
        if item.count('wav'):
            mp3s.append(item)
            filename = os.path.basename(item)
            filename_path=os.path.join(myfolder,item)
            playlistbox.insert(index, filename)
            playlist.insert(index, filename_path)
            index += 1
            #add_to_playlist(item)
            mixer.music.queue(filename_path)
    if len(mp3s) > 0:
        folderName = os.path.basename(myfolder)
        return (folderName,myfolder,mp3s)
    else:
        return None
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)
def about_us():
    tkinter.messagebox.showinfo('About Music Vault', 'This is a music player build using Python Tkinter by @Music Vault')
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)
mixer.init()
root.title("Music Vault")
root.iconbitmap(r'images/melody.ico')
# Root Window - StatusBar, LeftFrame, RightFrame
# LeftFrame - The listbox (playlist)
# RightFrame - TopFrame,MiddleFrame and the BottomFrame
#Input: A path to a folder
#Output: List containing paths to all of the nested folders of path
leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)
playlistbox = Listbox(leftframe)
playlistbox.pack()
      
addBtn = ttk.Button(leftframe, text="+ Add File", command=browse_file)
addBtn.pack(side=LEFT)
addFolderBtn = ttk.Button(leftframe, text="+ Add Folder", command=browse_folder)
addFolderBtn.pack(side=LEFT)
 
def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)
delBtn = ttk.Button(leftframe, text="- Remove", command=del_song)
delBtn.pack(side=LEFT)
rightframe = Frame(root)
rightframe.pack(pady=30)
topframe = Frame(rightframe)
topframe.pack()
lengthlabel = ttk.Label(topframe, text='Total Length : --:--', font='Times 14')
lengthlabel.pack(pady=5)

def show_details(play_song):
    file_data = os.path.splitext(play_song)
    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()
    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1

def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Music Vault could not find the file. Please check again.')

def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"

paused = FALSE
def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"

def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"

def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1

muted = FALSE
def mute_music():
    global muted
    if muted:  
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE
  
middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)
playPhoto = PhotoImage(file='images/play.png')
playBtn = ttk.Button(middleframe, image=playPhoto, command=play_music)
playBtn.grid(row=0, column=0, padx=10)
stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)
pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)
# Bottom Frame for volume, rewind, mute etc.
bottomframe = Frame(rightframe)
bottomframe.pack()
rewindPhoto = PhotoImage(file='images/rewind.png')
rewindBtn = ttk.Button(bottomframe, image=rewindPhoto, command=rewind_music)
rewindBtn.grid(row=0, column=0)
mutePhoto = PhotoImage(file='images/mute.png')
volumePhoto = PhotoImage(file='images/volume.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
volumeBtn.grid(row=0, column=1)
scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)
def on_closing():
    stop_music()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()