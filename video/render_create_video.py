import cv2
import numpy as np
from model_3d.create_ship_animation import animate_ship
import os
import bpy



def render_images():

    animate_ship()

    bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 0), rotation=(1.44513, 1.647e-07, 0.502655), scale=(1, 1, 1))

    cam = bpy.data.objects['Camera']
    x = 18
    y = -30
    z = 30
    rx = -0.5
    ry = 0.8
    rz = -1.3
    cam.location = (x,y,z)
    cam.rotation_euler  = (rx,ry,rz)

    for scene in bpy.data.scenes:
        scene.render.ffmpeg.codec = 'FFV1'
        scene.render.fps = 24
        scene.render.ffmpeg.constant_rate_factor = 'LOW'
        scene.render.ffmpeg.ffmpeg_preset = 'REALTIME'
        scene.render.filepath = '/Users/juleslockey/code/AndyW1990/rl-control/model_3d/test_images/test'
        bpy.ops.render.render(animation=True)






def generate_video():
    image_folder = '/Users/juleslockey/code/AndyW1990/rl-control/model_3d/test_images' # make sure to use your folder
    video_name = 'test_vid.mp4'
    os.chdir("/Users/juleslockey/code/AndyW1990/rl-control/model_3d/test_images")

    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")]

    images = sorted(images)

    # Array images should only consider
    # the image files ignoring others if any

    frame = cv2.imread(os.path.join(image_folder, images[0]))

    # setting the frame width, height width
    # the width, height of first image
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    video = cv2.VideoWriter(video_name, fourcc, 24, (width, height))

    # Appending the images to the video one by one
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    # Deallocating memories taken for window creation
    # cv2.destroyAllWindows()
    video.release()  # releasing the video generated

# motion_setup()

render_images()

# Calling the generate_video function
generate_video()
