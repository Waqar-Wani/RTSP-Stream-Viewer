# **RTSP Streaming and Testing Framework**

## **Project Overview**
This project provides a framework for streaming and testing RTSP streams with audio and video support. It is designed to handle multiple RTSP streams and allows easy switching of audio streams in real-time. Additionally, it includes utilities for generating local RTSP streams for testing purposes and verifying RTSP URL validity. The project is ideal for integrating RTSP-supported cameras with systems like Raspberry Pi for home or small-scale surveillance setups.

---

## **Instructions for Setup**

### **1. Prerequisites**
- Install [Python 3.7+](https://www.python.org/downloads/) on your system.
- Install [Git](https://git-scm.com/downloads).
- Install [FFmpeg](https://ffmpeg.org/download.html) and ensure it is added to your system's PATH.
- Ensure your network supports RTSP streaming.

### **2. Clone the Repository**
```bash
git clone <repository-url>
cd RSTP
```

### **3. Install Dependencies**
Use `pip` to install the required Python libraries:
```bash
pip install opencv-python numpy
```

### **4. File Descriptions**
- **`mediamtx_v1.11.1_windows_amd64/`**: Contains the `mediamtx.exe` and `mediamtx.yml` files for generating local RTSP streams.
- **`Start Stream.bat`**: Executes the `RSTP Stream with Audio.py` file to display RTSP streams in a 2x2 grid with audio selection.
- **`Local Stream Test.py`**: Streams local video files as RTSP streams for testing.
- **`RTSP Test URL.py`**: Verifies the validity of RTSP URLs.
- **`Single Screen Test.py`**: Displays a single RTSP stream with both video and audio for debugging.
- **Sample Video Folders**: Contains test video files used for generating local RTSP streams.

### **5. Configure RTSP URLs**
- Update RTSP URLs in `RSTP Stream with Audio.py` and `Single Screen Test.py` files as per your camera or stream sources.
- For local testing, generate dummy RTSP URLs using the `Start Local RTSP.bat` file and use them in the code.

---

## **Steps for Testing RTSP Streams**

### **1. Generating Local RTSP Streams**
- Place video files (minimum 10 minutes duration) in the 'video` folder.
- Run `Start Local RTSP.bat` to start the RTSP server.
- Note the generated RTSP URLs in the console for testing.

### **2. Testing a Single RTSP Stream**
- Open `Single Screen Test.py`.
- Replace the RTSP URL in the script with your stream URL.
- Run the script:
  ```bash
  python Single Screen Test.py
  ```
- Ensure video and audio are functional.

### **3. Testing Multiple Streams in a Grid**
- Open `RSTP Stream with Audio.py`.
- Replace the RTSP URLs in the script with your stream sources.
- Run the script:
  ```bash
  python RSTP Stream with Audio.py
  ```
- Test the audio switching by clicking on individual streams.

### **4. Checking RTSP URL Validity**
- Open `RTSP Test URL.py`.
- Update the RTSP URL in the script.
- Run the script:
  ```bash
  python RTSP Test URL.py
  ```
- Confirm the URL is streaming without errors.

---

## **Known Issues**

1. **Latency in Audio-Video Sync**:  
   Due to network conditions, you may experience delays in audio or video playback.

2. **Local RTSP Stream Testing**:  
   Ensure video files used for local RTSP testing are longer than 10 minutes. Shorter files may cause stream errors when they finish playing.

3. **Abrupt Closures**:  
   RTSP streams might close unexpectedly due to network instability or incomplete configurations. Restart the scripts if this occurs.

---

## **Future Enhancements**
1. **Integration with Raspberry Pi**:  
   Facilitate seamless use of the framework with Raspberry Pi for RTSP-supported cameras in home networks.

2. **Out-of-Network Camera Support**:  
   Enhance the framework to support cameras located outside the local network via port forwarding or VPN setups.

3. **Improved Error Handling**:  
   Add robust error-handling mechanisms to detect and recover from stream interruptions.

4. **Enhanced User Interface**:  
   Develop a user-friendly interface for managing multiple streams and audio switching.

---