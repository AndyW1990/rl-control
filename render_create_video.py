import cv2
import numpy as np
from model_3d.create_ship_animation import animate_ship
import os
import bpy



def render_images():
    """
    Calls the animated ship function and produces a set of images based on each frame
    produced throughout the model. It then saves each individual image into a seperate
    folder to be called again later.
    """

    animate_ship()

    # Creates a camera and positions the camera at a point to accurately view the object
    cam = bpy.data.objects['Camera']
    x = 22
    y = -30
    z = 10
    rx = 1.38
    ry = 0.18
    rz = 0.59
    cam.location = (x,y,z)
    cam.rotation_euler  = (rx,ry,rz)

    # Renders the images at set values and saves these images in a new folder
    for scene in bpy.data.scenes:
        scene.render.ffmpeg.codec = 'FFV1'
        scene.render.fps = 24
        scene.render.ffmpeg.constant_rate_factor = 'LOW'
        scene.render.ffmpeg.ffmpeg_preset = 'REALTIME'
        scene.render.filepath = '/Users/juleslockey/code/AndyW1990/rl-control/model_3d/test_images/test'
        bpy.ops.render.render(animation=True)

    lamp_data = bpy.data.lights.new(name="Lighting", type='SUN')

    # Create new object with our lamp datablock
    lamp_object = bpy.data.objects.new(name="Lighting", object_data=lamp_data)

    # Place lamp to a specified location
    lamp_object.location = (5.0, 5.0, 5.0)

    # And finally select it make active
    # scene.objects.active = lamp_object

def generate_video():
    """
    Takes in all the image files in a ceration folder and from there, merges all of the images
    in order to produce a video at a set frame rate that is saved in the same folder as
    where the images are saved.
    """

    # Sets the file locations and video name to be saved
    image_folder = '/Users/juleslockey/code/AndyW1990/rl-control/model_3d/test_images' # make sure to use your folder
    video_name = 'test_vid.mp4'
    os.chdir("/Users/juleslockey/code/AndyW1990/rl-control/model_3d/test_images")

    # Takes out all of the images saved in the given folder and saves them in a list before sorting them
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")]
    images = sorted(images)

    # Takes in the height and width of the first image to make sure later on that all images are of the same size
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    # Sets up the video paramaters, such as the frame rate, the type of video and the size
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    video = cv2.VideoWriter(video_name, fourcc, 24, (width, height))

    # For each image, it writes the image sequentially into the video to produce the video
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    # 'Releases' the video, meaning it now knows the video is finished and pushes it back to the folder
    video.release()

# Calling the render images before the video creation
render_images()

# Calling the generate_video function
generate_video()
