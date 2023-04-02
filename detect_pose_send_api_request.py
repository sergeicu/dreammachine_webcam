# requirements: 
    # pip install mediapipe # or mediapipe-silicon 
    # pip install opencv-python
    # pip install numpy 
    # pip install requests 


import cv2
import mediapipe as mp
import numpy as np
import time
import requests

# mediapipe objects 
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# For webcam input:
cap = cv2.VideoCapture(0)

# initialize time counter 
first_time = True
last_time = time.time()

# turn on for api / pose detection debug 
debug = False


# API details 
api_url = "https://dream-machine-helper.azurewebsites.net/api/callPhone"
headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "DELETE, POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
        'Content-Type': 'application/json',
    }                


# read frames 
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    pose_detected = True if results.pose_landmarks is not None else False 
    # if pose_detected and first_time:
    #     last_time = time.time()
    #     first_time = False
    
    current_time = time.time()
    if (pose_detected and first_time) or (pose_detected and current_time - last_time >= 60): 
        first_time = False 
        print("detected a human")

        response = requests.get(api_url, headers=headers)
        if debug: 
            from IPython import embed; embed()
            exhibits = response.json()['exhibits']
        last_time = current_time 

    else: 
        # skipping 
        print("_")

    # Uncomment if you want to show pose on a video feed -> could be cool if there is a screen showing it 
    # # Draw the pose annotation on the image.
    # image.flags.writeable = True
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # mp_drawing.draw_landmarks(
    #     image,
    #     results.pose_landmarks,
    #     mp_pose.POSE_CONNECTIONS,
    #     landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # # Flip the image horizontally for a selfie-view display.
    # cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    # if cv2.waitKey(5) & 0xFF == 27:
    #   break
cap.release()
