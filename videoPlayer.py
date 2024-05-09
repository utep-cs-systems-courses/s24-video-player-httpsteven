#!/usr/bin/env python3

import cv2
import threading
import queue

# Constants
FRAME_RATE = 24
MAX_QUEUE_SIZE = 10

# Queues for frame processing
color_frame_queue = queue.Queue(maxsize=MAX_QUEUE_SIZE)
gray_frame_queue = queue.Queue(maxsize=MAX_QUEUE_SIZE)

def extract_frames(video_path):
    """Extract frames from a video file and enqueue them into the color_frame_queue."""
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        color_frame_queue.put(frame)
        print(f"Extracting frame {frame_count}")
        frame_count += 1
    cap.release()
    color_frame_queue.put(None)  # Indicate completion of extraction

def convert_to_grayscale():
    """Convert frames from color_frame_queue to grayscale and enqueue them in gray_frame_queue."""
    frame_count = 0
    while True:
        frame = color_frame_queue.get()
        if frame is None:
            gray_frame_queue.put(None)  # Indicate completion of conversion
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame_queue.put(gray_frame)
        print(f"Converting frame {frame_count}")
        frame_count += 1

def display_frames():
    """Display grayscale frames from gray_frame_queue on the screen."""
    frame_count = 0
    while True:
        frame = gray_frame_queue.get()
        if frame is None:
            break
        cv2.imshow('Video', frame)
        print(f"Displaying frame {frame_count}")
        if cv2.waitKey(int(1000 / FRAME_RATE)) & 0xFF == ord('q'):
            break
        frame_count += 1
    cv2.destroyAllWindows()

def main():
    video_path = 'clip.mp4'
    
    # Define the threads for frame extraction, conversion, and display
    threads = [
        threading.Thread(target=extract_frames, args=(video_path,)),
        threading.Thread(target=convert_to_grayscale),
        threading.Thread(target=display_frames)
    ]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
