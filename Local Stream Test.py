import subprocess
import time

def start_ffmpeg_stream(input_file, stream_url):
    """
    Start an FFmpeg process to stream a video to MediaMTX.

    :param input_file: Path to the video file or webcam device.
    :param stream_url: RTSP URL where the stream will be pushed.
    """
    ffmpeg_command = [
        "ffmpeg",
        "-re",  # Read input at native frame rate
        "-i", input_file,  # Input file or device
        "-c", "copy",  # Use codec copy to avoid re-encoding
        "-f", "rtsp",  # Output format is RTSP
        stream_url  # RTSP URL for the stream
    ]

    # Start the FFmpeg process
    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return process

def main():
    # Define the video sources (replace these with the paths to your video files or webcam devices)
    video_sources = [
        "videos\input1.mp4",  # Example file 1
        "videos\input2.mp4",  # Example file 2
        "videos\input3.mp4"   # Example file 3
    ]

    # Define the RTSP URLs for each stream
    rtsp_urls = [
        "rtsp://localhost:8554/stream1",
        "rtsp://localhost:8554/stream2",
        "rtsp://localhost:8554/stream3"
    ]

    # Start the FFmpeg processes to stream each video source to its corresponding RTSP URL
    processes = []
    for i in range(3):
        process = start_ffmpeg_stream(video_sources[i], rtsp_urls[i])
        processes.append(process)
        print(f"Started streaming {video_sources[i]} to {rtsp_urls[i]}")

    # Run the streams for a certain amount of time (e.g., 1 hour)
    try:
        time.sleep(3600)  # Keep the streams running for 1 hour
    except KeyboardInterrupt:
        pass  # Allow user to stop the streams with Ctrl+C

    # Close all FFmpeg processes after the duration
    for process in processes:
        process.terminate()
        process.wait()
        print("Stopped streaming.")

if __name__ == "__main__":
    main()
