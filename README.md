# Raspberry Pi Object Detection — Canon 1300D + YOLOv8

Tethered capture from a Canon EOS 1300D on a headless Raspberry Pi, with YOLOv8n object
detection drawn onto every shot.

The script captures a full-resolution JPEG over USB, runs detection on it, and writes an
annotated copy next to the original — no monitor or desktop session required.

---

## Repository layout

```
AI_project/
└── UIT/
    ├── capture_detect.py     # the whole program (~80 lines)
    ├── captured_images/      # output: image_*.jpg and image_*_detected.jpg
    └── AI video.mp4          # 19 MB demo recording
```

> Note: the code sits inside the `UIT/` subfolder, so every command below is run from
> `AI_project/UIT`, not from the repository root.

---

## Requirements

**Hardware**

- Raspberry Pi 4 or 5 (8 GB recommended) — or any Linux host with USB
- Canon EOS 1300D and a USB cable
- microSD card, 32 GB or larger

**Software**

- Raspberry Pi OS 64-bit (or Debian/Ubuntu)
- Python 3.8+
- Python packages: `ultralytics`, `opencv-python-headless`, `numpy`

`opencv-python-headless` is deliberate — there is no display server, so the full OpenCV
build with GUI support is not needed.

---

## Setup

```bash
# 1. System packages
sudo apt update
sudo apt install -y gphoto2 python3-venv

# 2. Clone and enter the working directory
git clone https://github.com/UNKNOWN0410/AI_project.git
cd AI_project/UIT

# 3. Virtual environment
python3 -m venv objdetect_env
source objdetect_env/bin/activate

# 4. Python dependencies
pip install ultralytics opencv-python-headless numpy
```

### Configure the camera

Connect the 1300D, power it on, and set the mode dial to **Manual (M)**. Detection needs
JPEG, not RAW:

```bash
gphoto2 --set-config /main/imgsettings/imageformat=0
```

If that path is rejected by your firmware, set it on the camera itself:
**Menu → Image Quality → JPEG (Large/Fine)**.

Confirm the tether works before touching Python:

```bash
gphoto2 --auto-detect
gphoto2 --capture-image-and-download --filename test.jpg && rm test.jpg
```

---

## Usage

```bash
source objdetect_env/bin/activate
python3 capture_detect.py
```

The program prompts `Capture image? (q to quit):`

- press **Enter** (or type anything) → grab a frame and run detection
- type **q** → exit

On first run, Ultralytics downloads `yolov8n.pt` (~6 MB) into the current directory.

> The prompt is line-based `input()`, not a keypress listener, so each capture needs Enter
> plus a newline. This keeps it usable over SSH without a terminal in raw mode.

### Output

Both files land in `captured_images/`, named by timestamp so captures never overwrite:

| File | Contents |
|---|---|
| `image_20260413_141532.jpg` | the original frame from the camera |
| `image_20260413_141532_detected.jpg` | the same frame with YOLO boxes and class labels |

---

## How it works

1. **Capture** — `gphoto2 --capture-image-and-download` is invoked as a subprocess, writing
   straight to `captured_images/`. A failed capture is retried up to 3 times with a 2-second
   delay, since tethered cameras occasionally miss a trigger.
2. **Load** — the JPEG is read with `cv2.imread()`.
3. **Detect** — `yolov8n.pt` (COCO, 80 classes) runs inference on the frame.
4. **Annotate** — `results[0].plot()` renders boxes and labels, and the result is written
   alongside the original.

`yolov8n` is the nano variant, chosen so inference stays practical on Pi-class CPUs. On a
Pi 5 you can trade speed for accuracy:

```python
model = YOLO("yolov8s.pt")   # or yolov8m.pt on a desktop GPU
```

---

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `Could not claim the USB device` | Another process holds the camera. Stop the auto-mounter: `sudo killall gvfs-gphoto2-volume-monitor` and re-plug the camera |
| `gphoto2: command not found` | `sudo apt install gphoto2` |
| `gphoto2 --auto-detect` lists nothing | Cable or mode issue — check the camera is on, out of sleep, and not in print/PTP mode |
| Capture fails all 3 attempts | Card full, camera asleep, or the lens is hunting for focus. Switch to manual focus |
| `Failed to load image` | gphoto2 wrote a different filename or extension than requested — check what actually landed in `captured_images/` |
| Detections look wrong or empty | Nano model at full 18 MP resolution detects small objects poorly; downscale the frame before inference |

---

## Notes and limitations

- **One frame at a time.** This is a capture-inspect loop, not a live video pipeline. For
  continuous detection you would need `gphoto2 --capture-movie` with a MJPEG stream.
- **18 MP is slow.** Each frame is a full-resolution JPEG, so expect roughly 1–3 seconds per
  detection cycle on a Pi 4.
- **The demo video is committed in-repo** at 19 MB, which is most of this repository's size.
  Moving it to a release asset or Git LFS would keep clones fast.
- **Not unattended.** There is no systemd unit or scheduling; it is an interactive tool.

---

## License

No license file is included. Add one (MIT is a reasonable default) before treating this as
reusable code.
