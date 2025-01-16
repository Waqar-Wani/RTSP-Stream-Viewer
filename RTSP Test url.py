import cv2
import time

# Replace with the RTSP URL you want to check
rtsp_url = "rtsp://localhost:8554/mystream"  # Example invalid URL for testing

# Open the RTSP stream using OpenCV
cap = cv2.VideoCapture(rtsp_url)

# Start a timer to check if stream responds within 10 seconds
start_time = time.time()

# Wait for the stream to be accessible or timeout after 10 seconds
while True:
    if not cap.isOpened():
        # If unable to open the stream, check the time elapsed
        if time.time() - start_time > 10:
            print("Stream not available. The URL did not respond within 10 seconds.")
            cv2.destroyAllWindows()
            time.sleep(5)  # Wait for 5 seconds before closing the program
            break
        else:
            # Retry after a short delay if not opened yet
            print("Attempting to open stream...")
            time.sleep(1)
    else:
        # Try reading a frame after the stream is opened
        ret, frame = cap.read()

        if ret:
            print(f"RTSP stream from URL {rtsp_url} is accessible. Stream is OK.")
            
            # Display the frame for 10 seconds
            cv2.imshow("Stream Frame", frame)
            cv2.waitKey(10000)  # Wait for 10 seconds to display the frame
            cv2.destroyAllWindows()
            break  # Exit the loop once the frame is displayed
        else:
            print("Error: Unable to receive a frame from the RTSP stream.")
            cv2.destroyAllWindows()
            break

# Release the stream after checking
cap.release()

print("Testing completed.")
