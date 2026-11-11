# Pikku - AI Desktop Companion Robot

Pikku is a small desktop companion robot project. The repository currently contains staged Python prototypes for camera-based face detection, directional/head-tracking logic, voice commands, speech output, and simulated movement.

## Current implementation status

**Status: partial prototype.** Selected camera and software modules are implemented, and the physical build is in progress. This repository is not yet a fully integrated autonomous robot.

| Area | Current state |
|---|---|
| Camera input | Webcam test using OpenCV |
| Face detection | OpenCV Haar-cascade face detection |
| Direction/head tracking | Face position mapped to directional states and a simulated servo angle |
| Voice input | SpeechRecognition with Google's online recognition service |
| Speech output | pyttsx3 |
| Movement | Pygame-based simulation |
| Physical actuation | Motor/servo and Raspberry Pi-to-ESP32 integration remain in progress |
| LLM conversation | Planned; no complete provider integration is included in the current scripts |

## Repository contents

| File | Purpose |
|---|---|
| `camera_test.py` | Opens the default webcam and displays the camera feed |
| `face_detect.py` | Detects faces and displays a simple left/center/right direction and action |
| `phase2_head_tracking.py` | Maps face position to a simulated head-servo angle |
| `phase3_robot_brain.py` | Converts face position into simple directional actions |
| `phase4_head_servo_sim.py` | Demonstrates head-angle mapping in the camera view |
| `phase4_virtual_robot.py` | Keyboard-controlled Pygame movement simulation |
| `phase5_voice_robot.py` | Voice-command recognition with text-to-speech responses |
| `phase5_face_voice_robot.py` | Combines face-direction logic and voice commands in a Pygame simulation |
| `phase6_ai_robot_simulator.py` | Uses face direction to control a virtual robot |
| `phase6_smart_robot.py` | Combines face-direction logic with a voice stop command |

These are separate phase experiments, not a single integrated application.

## Software setup

Use Python 3.10 or a compatible version supported by the installed packages.

```bash
git clone https://github.com/itzakus09/Pikku.git
cd Pikku
python -m venv .venv
```

Activate the virtual environment, then install the dependencies:

```bash
# Windows
.venv\\Scripts\\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Start with the camera test:

```bash
python camera_test.py
```

Other prototype scripts can be run individually, for example:

```bash
python face_detect.py
python phase5_voice_robot.py
python phase5_face_voice_robot.py
```

A working webcam is required for camera scripts. A microphone is required for voice scripts. PyAudio installation can vary by operating system; consult its installation guidance if `pip install -r requirements.txt` fails.

## Hardware direction

The intended architecture separates high-level perception/assistant work on a Raspberry Pi from low-level motor and sensor control on an ESP32. The current repository does not yet contain a complete ESP32 firmware or verified physical motor-control pipeline. Do not interpret the Pygame simulator or displayed servo angle as physical robot actuation.

## Limitations and next steps

- Face detection currently uses OpenCV's Haar-cascade classifier; it is a classical computer-vision baseline, not a trained deep-learning detector.
- Directional decisions are simple image-position heuristics and have not been benchmarked for accuracy or robustness.
- Pygame movement and servo-angle outputs are simulations.
- Voice recognition calls `recognize_google`, which requires internet access and sends audio to an online recognition service. Do not use it with sensitive conversations.
- The project does not yet include a complete LLM conversation stack, integrated ESP32 motor firmware, or measured end-to-end latency/accuracy results.

Planned work includes completing the mechanical/electrical integration, connecting the Raspberry Pi and ESP32 interfaces, adding safety limits for movement, and evaluating perception under varied lighting and camera positions.

## Safety

Test movement logic in simulation before connecting motors. Use a physical emergency stop, conservative motor limits, and supervised testing when hardware actuation is added.
