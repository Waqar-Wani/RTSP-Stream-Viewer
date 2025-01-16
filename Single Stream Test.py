import cv2
import subprocess
import numpy as np

# Replace this with your RTSP URL
rtsp_url = "rtsp://waqarwani:waqarwani@192.168.29.170:554/stream1"

# Launch ffplay using subprocess, running it in the background and ensuring no CMD window shows
ffplay_process = subprocess.Popen(
    ["ffplay", rtsp_url, "-nodisp", "-autoexit", "-hide_banner", "-loglevel", "panic"],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW
)

# OpenCV for additional processing or handling the video
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Error: Unable to open the RTSP stream")
    exit()

# Function to close the OpenCV video window and the ffplay audio
def close_stream():
    cap.release()  # Release OpenCV resources
    cv2.destroyAllWindows()  # Destroy OpenCV window

    # Terminate the ffplay process
    if ffplay_process.poll() is None:  # Check if ffplay is still running
        ffplay_process.terminate()
        ffplay_process.wait()  # Ensure ffplay process is completely terminated

    print("Video and audio closed.")
    exit()  # Close the program completely

# Mouse callback function to detect clicks
def click_event(event, x, y, flags, param):
    global button_x, button_y, button_width, button_height
    if event == cv2.EVENT_LBUTTONDOWN:
        # Check if the click is inside the button area
        if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
            close_stream()

# Display the video stream using OpenCV
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to retrieve frame. Exiting...")
        break

    # Get the height and width of the frame to calculate button position
    height, width, _ = frame.shape

    # Set the button size and position in the bottom-right corner
    button_width = 200
    button_height = 60
    button_x = width - button_width - 10  # 10 pixels from the right edge
    button_y = height - button_height - 10  # 10 pixels from the bottom edge

    # Draw text "Close Stream" with no background color
    cv2.putText(frame, "Close Stream", (button_x + 10, button_y + button_height // 2 + 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)  # White text

    # Show the frame
    cv2.imshow("RTSP Stream", frame)

    # Register the mouse callback
    cv2.setMouseCallback("RTSP Stream", click_event)

    # Check if the user clicked on the button (within the defined area)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release OpenCV resources
cap.release()
cv2.destroyAllWindows()

# Close ffplay process when done
if ffplay_process.poll() is None:  # Check if ffplay is still running
    ffplay_process.terminate()
    ffplay_process.wait()  # Ensure ffplay process is completely terminated

print("Video and audio closed.")
