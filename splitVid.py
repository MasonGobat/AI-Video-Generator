from moviepy.editor import *
import string, random

def splitVideo():
    vid = input("Please enter video name: ")
    video = VideoFileClip(f"C:/Users/Mason Gobat/Videos/{vid}.mp4")
    dur = video.duration // 60
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    for i in range(int(dur)): ## i & i++
        tempVid = video.subclip(i*60, (i+1)*60)
        tempVid.write_videofile(f"./Pictures/smarterDaily/clips/{code}{i}.mp4", fps=60)

splitVideo()