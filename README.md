# Object Detection and Retrieval With Hexapods

## Trey Crowther, Jacob Read, Shawn Jones, Jared Wasson

### Compilation and Running Instructions

1. SSH onto the Raspberry Pi on the USU network via `pi@144.39.245.255`
2. Verify that Pi has been turned on and the Hexapod is plugged in and turned on
3. Navigate to the directory `~/Projects/Python/tflite/`
4. Run the following command to initialize the tflite-environment `source tflite-env/bin/activate`
5. cd into `./object_detection`
6. Run the command `python SSHObjectDetection.py --modeldir=coco_ssd_mobilenet_v1`
7. The system will initialize, the Hexapod will rotate until it finds the object and go retrieve it

#### Note
The view from the Logitech Webcam can be viewed by connecting the Raspberry Pi to a display and running the same commands as above, with the exception of step 6
where the command should be replaced with `python Detection_webcam.py --modeldir=coco_ssd_mobilenet_v1`
