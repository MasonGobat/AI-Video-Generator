from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
from moviepy.editor import *
import re, time, os, random

def getText():
    driver = webdriver.Firefox()
    text = []
    parsedText = ""

    while len(parsedText.split()) < 100:
        driver.get("https://en.wikipedia.org/wiki/special:random") ## Goto a random wikipedia article

        content = driver.find_element(By.CLASS_NAME, "mw-parser-output")
        useableContent = content.find_elements(By.XPATH, "descendant::p | descendant::h2 | descendant::li") ## Get the elements with text in them
        text = [x.text for x in useableContent]

        for i in range(len(text)):
            if text[i] == "References[edit]" or text[i] == "External links[edit]": ## Remove random markup
                text = text[:i]
                break

        parsedText = "" ## Get one long text block
        for sent in text:
            parsedText += sent + " "

    driver.close()

    ## Clean up the text
    parsedText = re.sub("\[[0-9]+\]", "", parsedText)
    parsedText = re.sub("\[edit\]", "", parsedText)
    parsedText = re.sub("\"", "", parsedText)

    split = parsedText.split()
    parsedText = ""

    if len(split) > 300:
        for i in range(300):
            parsedText += split[i] + " "

    return parsedText

def getSummary(text):
    driver = webdriver.Firefox()

    driver.get("https://www.paraphraser.io/text-summarizer") ## Our summarizing tool

    ## Multiple pauses to allow the site to load and process
    time.sleep(5)

    ai = driver.find_element(By.ID, "inner_title2") ## Grabs different parts of the page and clicks them or loads our text
    ai.click()

    time.sleep(5)

    paste = driver.find_element(By.ID, "input-content")
    paste.send_keys(text)

    time.sleep(3)

    sum = driver.find_element(By.ID, "summarize_now")
    sum.click()
    time.sleep(7)

    text = driver.find_element(By.ID, "output-content").text

    driver.close()

    return re.sub("\n", "", text)

def create_voice_over(fileName, text):
    voiceoverDir = "" ## TODO: Put where you wanna save your voice overs here
    filePath = f"{voiceoverDir}/{fileName}"
    command = f'edge-tts --rate=+30% --voice en-US-MichelleNeural --text "{text}" --write-media {filePath}.mp3' ## Has some custom properties inside, check them out with the online documentation for edge-tts

    print(text)

    os.system(command)

    return filePath + ".mp3"

def makeVideo():
    text = getText()
    sum = getSummary(text)

    create_voice_over(date.today(), sum)

    ## Grabs one of the clips that you have, the audio that you just made, and creates a new video and audio element to overlay together.

    clipPath = random.choice(os.listdir("")) ## TODO: Add where your clips come from
    audioPath = f"{date.today()}.mp3" ## TODO: Put where your audio was saved to
    video = VideoFileClip(f"{clipPath}")
    audio = AudioFileClip(audioPath)
    video = video.set_audio(audio)
    video = video.set_duration(audio.duration) if audio.duration <= 59 else video.set_duration(59) ## I limit the clips to 60 seconds, but you can get rid of this line to leave it unlimited.
    
    video.write_videofile(f"{date.today()}.mp4", fps=60) ## TODO: Put where you want your finished video to go to

makeVideo()