import cv2
import numpy as np
import os
import bpy

def render_images(directory, episode='last'):

    """
    Calls the animated ship function and produces a set of images based on each frame
    produced throughout the model. It then saves each individual image into a seperate
    folder to be called again later.
    """
    
    image_folder = f'{directory}/episode={episode}/renderings/'
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    #abs_path = os.path.dirname(__file__)
    #rel_path = os.path.join(abs_path, '/renderings')
    #animate_ship()

    # Creates a camera and positions the camera at a point to accurately view the object
    bpy.ops.object.camera_add()
    bpy.context.object.name = 'Camera'
    cam = bpy.data.objects['Camera']

    bpy.context.scene.camera = cam
    # x_3d = 22
    # y_3d = -30
    # z_3d = 10
    # rx_3d = 1.38
    # ry_3d = 0.18
    # rz_3d = 0.59
    x_2d = 0.89
    y_2d = -80.2
    z_2d = 3.67
    rx_2d = 1.6
    ry_2d = 0
    rz_2d = 0
    cam.location = (x_2d,y_2d,z_2d)
    cam.rotation_euler  = (rx_2d,ry_2d,rz_2d)

    # Sun Object
    # lamp_data = bpy.data.lights.new(name="Lighting", type='AREA')
    # lamp_data.energy = 1000
    # lamp_object = bpy.data.objects.new(name="Lighting", object_data=lamp_data)
    # lamp_object.location = (15.0, -15.0, 15.0)
    bpy.ops.object.light_add()
    bpy.context.object.name = 'Light'

    light = bpy.data.objects['Light']
    light.data.type = 'SUN'
    light.rotation_euler = (0.5, 0, 1)
    light.data.energy = 10

    # Renders the images at set values and saves these images in a new folder
    for scene in bpy.data.scenes:
        scene.render.ffmpeg.codec = 'FFV1'
        scene.render.fps = 10
        scene.render.ffmpeg.constant_rate_factor = 'LOW'
        scene.render.ffmpeg.ffmpeg_preset = 'REALTIME'
        scene.render.filepath = image_folder
        bpy.ops.render.render(animation=True)


    # And finally select it make active
    # scene.objects.active = lamp_object

def generate_video(directory, episode='last', video_name='Sim_Vid'):
    """
    Takes in all the image files in a ceration folder and from there, merges all of the images
    in order to produce a video at a set frame rate that is saved in the same folder as
    where the images are saved.
    """
    
    image_folder = f'{directory}/episode={episode}/renderings/'
    video_name = f'{video_name}.mp4'


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
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(image_folder + video_name, fourcc, 10, (width, height))

    # For each image, it writes the image sequentially into the video to produce the video
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    # 'Releases' the video, meaning it now knows the video is finished and pushes it back to the folder
    video.release()



if __name__ == '__main__':
# Generate a model to test viedo creation
    dir_name = 'test_vid'
# Calling the render images before the video creation
    render_images(dir_name)
# Calling the generate_video function
    generate_video(dir_name)

