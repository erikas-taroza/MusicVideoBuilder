import moviepy.editor as mpy
import os

temp_path = "./assets/temp.mp4"
data_path = "./export_path.txt"

def add_image_to_audio(export_path, audio_path, image_path):
    print()

    # combine the audio and image in a video. the exported video is the same size as the image
    print("Creating temp file...")
    audio_clip = mpy.AudioFileClip(audio_path)
    image_clip = mpy.ImageClip(image_path)
    video_clip = image_clip.set_audio(audio_clip)
    video_clip.duration = audio_clip.duration - 1.2
    video_clip.fps = 1
    video_clip.write_videofile(filename = temp_path, codec = "libx264", logger = None)#ffmpeg_params = ["-s", "1280x720"]
    video_clip.close()
    image_clip.close()
    audio_clip.close()

    # get the exported video from above and resize it to fit the black bars height
    print("Resizing to 1280x720...")
    exported = mpy.VideoFileClip(temp_path)
    exported_resized = exported.resize(height = 720)

    # create the new video with black bars and the video created earlier
    black_bars = mpy.ImageClip("./assets/black_bars1280x720.jpg")
    new_video = mpy.CompositeVideoClip([black_bars, exported_resized.set_position("center")])
    #new_video.duration = exported.duration
    new_video = new_video.set_end(exported.duration - 0.2)
    new_video.fps = 1
    print(new_video.duration)

    split_path = audio_path.split("\\")
    name = split_path[len(split_path) - 1].split(".")[0]
    new_video.write_videofile(export_path + name + ".mp4", codec = "libx264", logger = None)

    black_bars.close()
    new_video.close()
    exported.close()
    exported_resized.close()
    os.remove(temp_path)

    print()
    print("Exported: " + export_path)
    input("Press ENTER to close...")

def run():
    export_path = ""
    try:
        file = open(data_path, "r")
        export_path = file.readline()
    except:
        path = input("Enter file path for all exports: ")
        file = open(data_path, "w")
        file.write(path.replace("\"", ""))
        file.close()
        export_path = path

    audio_path = input("Enter file path of audio: ").replace("\"", "")
    image_path = input("Enter file path of image: ").replace("\"", "")
    if audio_path != "" and image_path != "":
        add_image_to_audio(export_path, audio_path, image_path)

if __name__ == "__main__":
    run()