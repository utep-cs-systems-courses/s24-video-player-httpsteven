#!/usr/bin/env python3

import cv2
import threading
import queue
import time

# Constants
FRAME_RATE = 24
MAX_QUEUE_SIZE = 10

# Queues
color_frames = queue.Queue(maxsize=MAX_QUEUE_SIZE)
gray_frames = queue.Queue(maxsize=MAX_QUEUE_SIZE)

def extract_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        color_frames.put(frame)  # Blocks if full
        print(f"Extracting frame {count}")
        count += 1
    color_frames.put(None)  # Signal that extraction is done

def convert_to_grayscale():
    count = 0
    while True:
        frame = color_frames.get()  # Blocks if empty
        if frame is None:
            gray_frames.put(None)  # Signal that conversion is done
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frames.put(gray_frame)  # Blocks if full
        print(f"Converting frame {count}")
        count += 1

def display_frames():
    count = 0
    while True:
        frame = gray_frames.get()  # Blocks if empty
        if frame is None:
            break
        cv2.imshow('Video', frame)
        print(f"Displaying frame {count}")
        if cv2.waitKey(int(1000 / FRAME_RATE)) & 0xFF == ord('q'):
            break
        count += 1
    cv2.destroyAllWindows()

def main():
    video_path = 'clip.mp4'
    threads = [
        threading.Thread(target=extract_frames, args=(video_path,)),
        threading.Thread(target=convert_to_grayscale),
        threading.Thread(target=display_frames)
    ]

    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
