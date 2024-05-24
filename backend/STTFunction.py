import whisper
from whisper.utils import get_writer

class Caption:
    def __init__(self, start, end, text, ip):
        self.start = start
        self.end = end
        self.text = text.strip()
        self.ip = ip

    def to_webvtt(self):
        string = ""
        if self.ip:
            string = "\nIP"
        return string+f"\n{format_time(self.start)} --> {format_time(self.end)}\n{self.text}"

    def make_true(self):
        self.ip = True

def format_time(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours:02}:{minutes:02}:{secs:06.3f}"

def STTFunction(path, id):

    print("Opening: "+str(id)+", "+str(path))

    model = whisper.load_model("base")
    result = model.transcribe(path)
    #writer = get_writer("vtt", "static/video/")
    #writer(result, str(id) + ".vtt")
    #print(f' The text in video: \n {result["text"]}')

    captionList = []

    for segment in result["segments"]:

        isIP = any(char in ['!','?'] for char in segment['text'])

       
        for word in ['Portuguese']:
            if word in segment['text']:
                isIP = True

        captionList.append(Caption(segment['start'],segment['end'],segment['text'],isIP))

    print("scanning list")
    for i, caption in enumerate(captionList):
        if (i + 1) == len(captionList):
            break

        nextCaption = captionList[i+1]

        difference = nextCaption.start - caption.end
        if difference >= 1:
            captionList[i+1].make_true()

    with open("""static/video/"""+str(id)+".vtt", 'w', encoding='utf-8') as f:
        f.write("WEBVTT\n")
        for caption in captionList:
            f.write(caption.to_webvtt())
            f.write("\n")
        
        


if __name__ == "__main__":
    print("File Not Found? FFMPEG NOT on PATH most likely")
    inputPath = """static/video/1.mp4"""
    print("Running STT Function")
    STTFunction(inputPath, 1)