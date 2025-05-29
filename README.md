# Requirements
* Python 3.x
* OpenCV
* MediaPipe 
* Windows OS (for key input functionality)

# Installation
1. Clone or download this repository
2. Install the required packages:
```
pip install opencv-python mediapipe
```
# Usage
1. Run the steering script:
```
python steering.py
```

2. Position your hands in front of the camera:
* Two hands detected:
    - The system will calculate a steering direction based on hand positions

    - Moving both hands left/right will simulate pressing A/D keys

    - Keeping hands level will simulate pressing W (forward)
* One hand detected:
    - The system will simulate pressing S (backward)

3. Visual feedback:
* A circle and line will appear showing the detected steering direction
* On-screen text indicates the current command (turn left, turn right, etc.)

4. To quit:
* Press 'q' in the video window or close the window

# Controls
The system maps your hand positions to these keyboard inputs:
* W: Forward
* A: Left
* D: Right
* S: Backward

# Configuration
You can adjust these parameters in steering.py:

* **STEERING_SENSITIVITY**: Higher values require more pronounced hand movements to trigger turns
* **CIRCLE_RADIUS**: Size of the steering visualization circle
* **LINE_THICKNESS**: Thickness of the steering visualization lines

# Notes
* Works best in well-lit environments
* Requires both hands to be visible for steering control
* Only works on Windows due to the key input implementation
* Make sure no other applications are using the webcam while this is running

# Troubleshooting
If keys aren't being pressed:
* Check that your game/application window is active
* Verify the program has proper permissions
* Try adjusting the sensitivity if gestures aren't being detected properly

