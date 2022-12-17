# Object Detection and Retrieval With Hexapods

## Trey Crowther, Jacob Read, Shawn Jones, Jared Wasson

### Central Server Setup
1. clone `https://github.com/Jared-Wasson/piServer.git`
2. Install npm
3. run `npm i`
3. In terminal run `npm run start`
4. Update `SSHObjectDetection.py` to use the current server IP address on lines: `179` and `238`

### Compilation and Running Instructions

1. Verify that Raspberry Pi has a power source and is turned on       
2. Verify that the Hexapod is plugged in and turned on. There is a power switch that is connected to the main board in the center of the body
3. SSH onto the Raspberry Pi on the USU network via `pi@144.39.245.255`
4. Navigate to the directory `~/Projects/Python/tflite/`
5. Run the following command to initialize the tflite-environment `source tflite-env/bin/activate`
6. cd into `./object_detection`
7. Run the command `python SSHObjectDetection.py --modeldir=coco_ssd_mobilenet_v1`
8. The system will initialize, the Hexapod will rotate until it finds the object and go retrieve it

The system would work with any number of Hexapods, but we were only able to get one built and functional in time. Once the second one is built, this codebase can be placed onto the controlling Raspberry Pi of the second robot and they will work together to perform the task.


##### Note
The view from the Logitech Webcam can be viewed by connecting the Raspberry Pi to a display and running the same commands as above, with the exception of step 6
where the command should be replaced with `python Detection_webcam.py --modeldir=coco_ssd_mobilenet_v1`
