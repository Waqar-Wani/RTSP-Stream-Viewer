import cv2
import subprocess
import numpy as np

# Replace with your RTSP URLs
rtsp_urls = [
    "rtsp://localhost:8554/stream2",
    "rtsp://localhost:8554/stream1",
    "rtsp://localhost:8554/stream3",
    "rtsp://waqarwani:waqarwani@192.168.29.170:554/stream1"
]

# Number of rows and columns in the grid
grid_rows, grid_cols = 2, 2

# Launch ffplay for audio playback for each stream (initially muted)
ffplay_processes = []
is_audio_muted = [True] * len(rtsp_urls)  # Tracks audio mute/unmute status
current_unmuted_idx = -1  # No stream is unmuted initially

for url in rtsp_urls:
    ffplay_process = subprocess.Popen(
        ["ffplay", url, "-nodisp", "-autoexit", "-hide_banner", "-loglevel", "panic", "-an"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
    )
    ffplay_processes.append(ffplay_process)

# Open a list of RTSP streams
caps = [cv2.VideoCapture(url) for url in rtsp_urls]

# Check if all streams are opened successfully
if not all(cap.isOpened() for cap in caps):
    print("Error: Unable to open all RTSP streams.")
    for cap in caps:
        cap.release()
    for process in ffplay_processes:
        process.terminate()
    exit()

# Function to close all streams and ffplay processes
def close_all_streams():
    for cap in caps:
        cap.release()
    cv2.destroyAllWindows()
    for process in ffplay_processes:
        process.terminate()
        process.wait()
    print("All streams and audio processes closed.")
    exit()

# Mouse callback for detecting button clicks and unmuting audio for selected stream
def click_event(event, x, y, flags, param):
    global current_unmuted_idx

    # Check if the "Close All" button is clicked
    button_x, button_y, button_width, button_height = param['close_button']
    if event == cv2.EVENT_LBUTTONDOWN:
        if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
            close_all_streams()
            return
        
        # Determine which stream was clicked
        frame_width, frame_height = param['frame_width'], param['frame_height']
        for idx, (button_x, button_y) in enumerate(param['frame_positions']):
            if button_x <= x <= button_x + frame_width and button_y <= y <= button_y + frame_height:
                if current_unmuted_idx != -1 and current_unmuted_idx != idx:
                    # Mute the previously unmuted stream
                    ffplay_processes[current_unmuted_idx].terminate()
                    ffplay_processes[current_unmuted_idx] = subprocess.Popen(
                        ["ffplay", rtsp_urls[current_unmuted_idx], "-nodisp", "-autoexit", "-hide_banner", "-loglevel", "panic", "-an"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
                    )
                    is_audio_muted[current_unmuted_idx] = True  # Mute the previous stream

                if is_audio_muted[idx]:  # If the clicked stream is muted, unmute it
                    ffplay_processes[idx].terminate()  # Terminate the current ffplay process
                    ffplay_processes[idx] = subprocess.Popen(
                        ["ffplay", rtsp_urls[idx], "-nodisp", "-autoexit", "-hide_banner", "-loglevel", "panic"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
                    )
                    is_audio_muted[idx] = False  # Unmute this stream
                    current_unmuted_idx = idx  # Track the currently unmuted stream
                break

# Display the grid of video streams
try:
    # Create a window
    cv2.namedWindow("RTSP Stream Grid", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("RTSP Stream Grid", 1280, 720)  # Set initial size

    # Calculate positions for each stream
    frame_positions = []
    frame_width = 640
    frame_height = 480
    for i in range(grid_rows):
        for j in range(grid_cols):
            button_x = j * frame_width
            button_y = i * frame_height
            frame_positions.append((button_x, button_y))

    while True:
        # Read frames from each stream
        frames = []
        for cap in caps:
            if cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    # Black frame as fallback
                    frame = np.zeros((480, 640, 3), dtype=np.uint8)
                    cv2.putText(frame, "Stream Error", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                # Black frame as fallback for closed streams
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(frame, "Stream Not Available", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            frames.append(frame)

        # Get the current window size
        if cv2.getWindowProperty("RTSP Stream Grid", cv2.WND_PROP_VISIBLE) < 1:
            break  # Exit if the window is closed

        # Resize frames to fit into the grid
        resized_frames = [cv2.resize(frame, (frame_width, frame_height)) for frame in frames]

        # Combine frames into a grid
        rows = [
            np.hstack(resized_frames[i * grid_cols:(i + 1) * grid_cols])
            for i in range(grid_rows)
        ]
        grid_frame = np.vstack(rows)

        # Add a "Close All" button
        button_width, button_height = 200, 60
        button_x = grid_frame.shape[1] - button_width - 10
        button_y = grid_frame.shape[0] - button_height - 10
        cv2.rectangle(grid_frame, (button_x, button_y), (button_x + button_width, button_y + button_height), (0, 0, 0), -1)
        cv2.putText(grid_frame, "Close All", (button_x + 10, button_y + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Display the grid
        cv2.imshow("RTSP Stream Grid", grid_frame)

        # Register the mouse callback for detecting click events
        cv2.setMouseCallback("RTSP Stream Grid", click_event, param={
            'close_button': (button_x, button_y, button_width, button_height),
            'frame_width': frame_width,
            'frame_height': frame_height,
            'frame_positions': frame_positions
        })

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    close_all_streams()
