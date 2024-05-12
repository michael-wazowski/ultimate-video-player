import whisper
from whisper.utils import get_writer

def STTFunction(path, id):
    model = whisper.load_model("base")
    result = model.transcribe(path)
    writer = get_writer("vtt", "static/video/")
    writer(result, str(id) + ".vtt")
    #print(f' The text in video: \n {result["text"]}')

if __name__ == "__main__":
    inputPath = """static/video/subtitles.mp4"""
    print("Running STT Function")
    STTFunction(inputPath, 2)