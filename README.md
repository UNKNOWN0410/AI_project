# AI_project

# Raspberry Pi Object Detection with Canon 1300D

Captures images using a Canon 1300D on a Raspberry Pi and performs object detection with YOLOv8. Saves original (`image_*.jpg`) and detected images with bounding boxes (`image_*_detected.jpg`) in `captured_images/`. Designed for headless operation.

## Prerequisites

- **Hardware**: Raspberry Pi (4/5, 8GB), Canon 1300D, USB cable, microSD card (32GB+)
- **Software**: Raspberry Pi OS (64-bit), Python 3.7+, `gphoto2`, Python libraries (`ultralytics`, `opencv-python-headless`, `numpy`)
- **Network**: Pi and client device on same network, SSH enabled

## Setup

1. **Install OS & Update**:
   ```bash
   sudo apt-get update
   sudo apt-get upgrade -y
   ```

2. **Install Dependencies**:
   ```bash
   sudo apt-get install gphoto2 -y
   python3 -m venv objdetect_env
   source objdetect_env/bin/activate
   pip install ultralytics opencv-python-headless numpy
   ```

3. **Configure Camera**:
   - Connect Canon 1300D via USB, set to Manual mode.
   - Set to JPEG:
     ```bash
     gphoto2 --set-config /main/imgsettings/imageformat=0
     ```
     - Or manually: Camera Menu > Image Quality > JPEG (Large/Fine).
   - Test:
     ```bash
     gphoto2 --capture-image-and-download --filename test.jpg
     rm test.jpg
     ```

4. **Clone Repository**:
   ```bash
   git clone https://github.com/your-username/UIT.git
   cd UIT
   ```

## Usage

1. **Run Script**:
   ``` violently
   source objdetect_env/bin/activate
   python3 capture_detect.py
   ```
   - Press any key to capture, `q` to quit.
   - Saves images to `captured_images/`.

2. **Transfer Files**:
   - From a client PC (e.g., Windows PowerShell):
     ```powershell
     scp -r pi@<pi-ip>:/home/pi/UIT ~/Downloads
     ```
     - Replace `<pi-ip>` with Pi’s IP (`hostname -I`).
     - Adjust username (`pi`) and path as needed.
   - Or use FileZilla (SFTP to `<pi-ip>`, port 22).

## Structure

```
UIT/
├── capture_detect.py
├── captured_images/
│   ├── image_*.jpg
│   └── image_*_detected.jpg
└── README.md
```

## Troubleshooting

- **RAW (`.CR2`) Images**:
  ```bash
  gphoto2 --set-config /main/imgsettings/imageformat=0
  ```

- **Camera Busy**:
  ```bash
  sudo killall gvfsd-gphoto2
  sudo chmod 666 /dev/bus/usb/*/*
  ```

- **No Detected Images**:
  - Verify JPEG capture and YOLO model (`yolov8n.pt`).
  - Check: `ls captured_images/*_detected.jpg`.

- **SCP Issues**:
  - Install OpenSSH: `Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0`
  - Ensure SSH: `sudo systemctl start ssh`

## License
MIT License. See [LICENSE](LICENSE).
