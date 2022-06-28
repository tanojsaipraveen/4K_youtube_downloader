from fileinput import filename
from logging import logMultiprocessing
import pathlib
import re
from tkinter import * 
from tkinter import ttk,messagebox
from turtle import width
from urllib.request import urlopen
from pytube import YouTube
from pytube.cli import on_progress
from PIL import Image,ImageTk
import base64,os,threading
from io import BytesIO


root=Tk()

tt = pathlib.Path().resolve()

root.title("YOUTUBE VIDEO DOWNLOADER")
root.iconbitmap(str(tt)+"/YouTube.ico")
root.resizable(False,False)
canvas=Canvas(root,width=600,height=100)
canvas.grid(row=0,column=0)

Banner=ImageTk.PhotoImage(Image.open(str(tt)+"/YouTube.jpg"))
canvas.create_image(0,0,image=Banner,anchor=NW)

tab1=Frame(root,width=800,height=500)
tab1.grid(row=1,column=0)





urlbox=Entry(tab1,width=60,font=("Arial Bold",13))
urlbox.grid(row=0,column=0,columnspan=2,pady=3)
urlbox.focus_force()

label1=Label(tab1,text="",font=("Arial Bold",14),relief="solid")


canvas=Canvas(tab1,width=300,height=200,bg="grey")
canvas.grid(row=3,column=1,rowspan=6,pady=6)


Directory="Youtube_Videos"
Dir_Name="C:/"
path=os.path.join(Dir_Name,Directory)
try:
  os.mkdir(path)
  os.mkdir("C:/Youtube_Videos/Video")
  os.mkdir("C:/Youtube_Videos/Audio")
except OSError as error:
  pass

length_video=Label(tab1,text="",font=("Arial Bold",13))
length_video.grid(row=3,column=0,sticky=W,pady=6)

author=Label(tab1,text="",font=("Arial Bold",13))
author.grid(row=4,column=0,sticky=W)

views=Label(tab1,text="",font=("Arial Bold",13))
views.grid(row=5,column=0,sticky=W)

reso=Label(tab1,text="",font=("Arial Bold",13))
reso.grid(row=6,column=0,sticky=W)


#Progress Bar
my_progress=ttk.Progressbar(tab1,orient=HORIZONTAL,length=400,mode="indeterminate")


#percentage label
label2=Label(tab1,text="0%",font=("Arial Bold",15))

#FOR AUDIO DOWNLOAD
label3=Label(tab1,text="Audio Is Ready To Download",font=("Arial Bold",13),fg="green")



    
AUDIO=FALSE
VIDEO=FALSE


def get():
  global image1,clicked,yt,my_progress,dropdown,AUDIO,VIDEO
  chunk_size = 1024
  my_progress.grid(row=9,column=0,columnspan=2)
  my_progress.config(mode="indeterminate")
  my_progress.start(10)
  #DISPLAYING TITLE
  url=urlbox.get()
  yt=YouTube(url)
  title=yt.title
  label1.grid(row=2,column=0,columnspan=2,pady=8)
  label1.config(text=title)
  #DISPLAYING THUMBNAIL
  u=urlopen(yt.thumbnail_url).read()
  im=Image.open(BytesIO(u))
  resize=im.resize((300,200), Image.ANTIALIAS)
  image1=ImageTk.PhotoImage(resize)
  canvas.create_image(0,0,image=image1,anchor=NW)
  
  clicked=StringVar()
  if click=="GET VIDEO":
    label3.grid_forget()
    VIDEO=TRUE
    AUDIO=FALSE
    #LISTING ALL RESOLUTIONS
    #resolution= [stream.resolution for stream in yt.streams.filter(file_extension="mp4",progressive=True).all()]
    resolution = []
    resolution1= [stream.resolution for stream in yt.streams.filter(progressive=False).order_by('resolution').desc().all()]
    for x in resolution1:
        if x == '1440p':
            x = '2K'
        elif x == '2160p':
            x = '4K'
        elif x == '4320p':
            x = '8K'
        if x not in resolution:
           resolution.append(x)
    clicked.set("Select Resolution")
    dropdown=OptionMenu(tab1,clicked,*resolution)
    dropdown.grid(row=7,column=0)
    #reso.config(text=f"Available Resolutions: {resolution[:]}") 

  author.config(text=f"Author: {yt.author}")
  views.config(text="Views: {:,}".format(yt.views))
   
  Length=yt.length
  if Length>60 and Length<3600:
    minute=Length//60
    second=Length%60
    length_video.config(text=f"Length: {minute} minutes {second} seconds")
    
  elif Length>=3600:
      hour=(Length//60)//60
      minute=(Length//60)%60
      second=Length%60
      length_video.config(text=f"Length: {hour} hour {minute} minutes {second} seconds")

  elif Length<60:
      length_video.config(text=f"Length: {Length} seconds")
  
  if click=="GET AUDIO":
    try:
      dropdown.grid_forget()
    except Exception as e:
      pass
    AUDIO=TRUE
    VIDEO=FALSE
    reso.config(text=f"Audio Format: MP3")
    label3.grid(row=7,column=0)
  
  my_progress.grid_forget()
  

def on_progress(stream, chunk, bytes_remaining):
  global inc,my_progress,label2
  total_size = stream.filesize
  bytes_downloaded = total_size - bytes_remaining
  percentage_of_completion = bytes_downloaded / total_size * 100
  inc=int(percentage_of_completion)
  print(inc)
  my_progress["value"]+=inc-my_progress["value"]
  label2.config(text=f"{inc}%")
  if my_progress["value"]==100:
    my_progress.grid_forget()
    label2.grid_forget()
    label2["text"]="0%"
    messagebox.showinfo("Youtube Downloader","Downloaded Successfully...\nPath: C:/Youtube_Videos")

def replacestr(s: str, max_length: int = 255) -> str:
    ntfs_characters = [chr(i) for i in range(0, 31)]
    characters = [
        r'"',
        r"\#",
        r"\$",
        r"\%",
        r"'",
        r"\*",
        r"\,",
        r"\.",
        r"\/",
        r"\:",
        r'"',
        r"\;",
        r"\<",
        r"\>",
        r"\?",
        r"\\",
        r"\^",
        r"\|",
        r"\~",
        r"\\\\",
    ]
    pattern = "|".join(ntfs_characters + characters)
    regex = re.compile(pattern, re.UNICODE)
    filename = regex.sub("", s)
    return filename[:max_length].rsplit(" ", 0)[0]

def check_file_exists(filename):
  res = os.listdir("C:\\Youtube_Videos\\Video\\")
  exist_count = res.count(filename+"_out.mp4")
  return exist_count

 

def reset_form():
  urlbox.delete(0, END)
  urlbox.insert(0, "")
  #urlbox.set("")
  label1.config(text="")
  # label1.grid_forget()
  length_video.config(text="")
  author.config(text="")
  views.config(text="")
  #canvas.create_image(width=300,height=200,bg="grey")
  #canvas = Canvas(tab1,width=300,height=200,bg="grey")
  # canvas.grid_forget()
  



def download():
  global my_progress
  if VIDEO==TRUE:
    my_progress.grid(row=9,column=0)
    my_progress.config(mode="determinate")
    my_progress.stop()
    label2.grid(row=9,column=1)
    os.chdir("C:/Youtube_Videos/Video")
    try:
      if clicked.get() == '2K':
        val = '1440p'
      elif clicked.get() == '4K':
        val = '2160p'
      elif clicked.get() == '8K':
        val = '4320p'
      else:
        val = clicked.get()
      file=yt.streams.filter(res = val).first()

      size=file.filesize
      b = check_file_exists(replacestr(yt.title).replace(' ','_'))
      
      if b==True:
        a1=messagebox.askyesno("Message","Do You Want To Override")
        if a1:
          a=messagebox.askyesno("Do You Want To Download",f"File Size: {round(size* 0.000001, 2)} MegaBytes")
          file_download(a)
        else:
          print('')
          #file_download(a)
      else:
        a=messagebox.askyesno("Do You Want To Download",f"File Size: {round(size* 0.000001, 2)} MegaBytes")
        file_download(a)
      
      reset_form()
      os.startfile("C:/Youtube_Videos/Video")

      
    except Exception as e:
      dropdown.grid(row=7,column=0)
      my_progress.grid_forget()
      label2.grid_forget()
      messagebox.showerror("Error","Error Raised Due To!\n>UnSelected Resolution  \n>Your Internet Connectivity \n> "+e.args[0])
  
  
  if AUDIO==TRUE:
    my_progress.grid(row=9,column=0)
    my_progress.config(mode="determinate")
    my_progress.stop()
    label2.grid(row=9,column=1)
    os.chdir("C:/Youtube_Videos/Audio")
    try:
      mp3=yt.streams.filter(only_audio=True).desc().first()
      size=mp3.filesize
      get=messagebox.askyesno("Do You Want To Download",f"File Size: {round(size* 0.000001, 2)} MegaBytes")
      if get==True:
        yt.register_on_progress_callback(on_progress)  
        audio=yt.streams.filter(only_audio=TRUE).desc().first().download()
        base, ext = os.path.splitext(audio)
        converted=base +'.mp3'
        os.rename(audio,converted)
      if get==False:
        my_progress.grid_forget()
        label2.grid_forget()

      
      
    except Exception as e:
      my_progress.grid_forget()
      label2.grid_forget()
      messagebox.showerror("Error ","Error Raised Due To!\n\n>Your Internet Connectivity")



def pop_menu(event):
    menu.tk_popup(event.x_root, event.y_root)

def copy():
    urlbox.event_generate("<<Copy>>")

def cut():
    urlbox.event_generate("<<Cut>>")

def paste():
    urlbox.event_generate("<<Paste>>")

def select_all():
    urlbox.event_generate("<<SelectAll>>")

    #Right Click Menu
menu = Menu(urlbox, tearoff=0, bg="white", fg="black")
#options
menu.add_command(label="Copy", command=copy)
menu.add_command(label="Cut", command=cut)
menu.add_separator()
menu.add_command(label="Paste", command=paste)
menu.add_separator()
menu.add_command(label="Select All", command=select_all)

#Make the menu pop up
urlbox.bind("<Button - 3>", pop_menu)


def file_download(a):
   #a=messagebox.askyesno("Do You Want To Download",f"File Size: {round(size* 0.000001, 2)} MegaBytes")
   if a==True:
    yt.register_on_progress_callback(on_progress)  
    #file = yt.title.replace(':','_').replace('(','').replace(')','').replace('|','').replace(' ','_')
    file = replacestr(yt.title).replace(' ','_')
    yt.streams.filter(res=clicked.get()).first().download(filename=file+'.mp4')
    mp3=yt.streams.filter(only_audio=True).desc().first()
    size=mp3.filesize
    audio=yt.streams.get_audio_only().download(filename=file+'.mp3')
    #filename = yt.title.replace(':','_').replace('|','').replace(' ','_')
    filename =replacestr(yt.title).replace(' ','_')
    video_path = "C:\\Youtube_Videos\\Video\\"+filename+".mp4"
    audio_path = "C:\\Youtube_Videos\\Video\\"+filename+".mp3"
    output_path = "C:\\Youtube_Videos\\Video\\"+filename+"_out.mp4"
    combine_audio_video(video_path,audio_path,output_path)

        
    if a==False:
      dropdown.grid(row=7,column=0)
      my_progress.grid_forget()
      label2.grid_forget()

def combine_audio_video(video_path,audio_path,output_path):
  try:
    os.system(f'ffmpeg -y -i {video_path} -i {audio_path} -c copy {output_path}')
    remove_files(video_path,audio_path)
  except Exception as e:
    messagebox.showerror("Error ","Error Raised Due combine function"+e)


def remove_files(video_path,audio_path):
    if os.path.exists(video_path):
        os.remove(video_path)

    if os.path.exists(audio_path):
        os.remove(audio_path)  


def thread(b):
  global click
  click=b
  thread=threading.Thread(target=get)
  thread.start()
  combine_audio_video()

def thread1():
  thread=threading.Thread(target=download)
  thread.start()


button1=Button(tab1,text="GET VIDEO",font=("Arial Bold",10),bg="#c2dcf0",command=lambda b="GET VIDEO":thread(b))
button1.grid(row=1,column=0,ipadx=50,ipady=10)
button2=Button(tab1,text="GET AUDIO",font=("Arial Bold",10),bg="#c2dcf0",command=lambda b="GET AUDIO":thread(b))
button2.grid(row=1,column=1,ipadx=50,ipady=10,pady=5)


button3=Button(tab1,text="Download",font=("Arial Bold",10),bg="#c2dcf0",command=thread1)
button3.grid(row=8,column=0,ipadx=50,ipady=15,pady=5)


root.mainloop()