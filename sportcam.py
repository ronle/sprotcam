import cv2 
import numpy as np


#Define the source of the video streams
source1 = “http://192.168.0.101:8080/video” 
source2 = “http://192.168.0.102:8080/video”

#Create video capture objects for each source
cap1 = cv2.VideoCapture(source1) 
cap2 = cv2.VideoCapture(source2)

#Define the output file name and codec
output_file = “output.avi” 
codec = cv2.VideoWriter_fourcc(*“MJPG”)

#Define the output frame size and overlapping percentage
output_width = 1280 
output_height = 720 
overlap_percent = 0.2

#Calculate the width of each input frame and the overlapping region
input_width = int(output_width / (2 - overlap_percent)) 
overlap_width = int(input_width * overlap_percent)

#Create a video writer object for the output file
out = cv2.VideoWriter(output_file, codec, 30, (output_width, output_height))

#Create a stitcher object
stitcher = cv2.Stitcher.create()

#Loop until both video streams end
while cap1.isOpened() and cap2.isOpened(): # Read a frame from each source ret1, frame1 = cap1.read() ret2, frame2 = cap2.read()  
        # Check if both frames are valid
    if ret1 and ret2:
        # Resize the frames to the input width and output height
        frame1 = cv2.resize(frame1, (input_width, output_height))
        frame2 = cv2.resize(frame2, (input_width, output_height))

        # Crop the overlapping region from each frame
        crop1 = frame1[:, input_width - overlap_width:]
        crop2 = frame2[:, :overlap_width]

        # Stitch the cropped regions together
        status, stitched = stitcher.stitch([crop1, crop2])

        # Check if the stitching was successful
        if status == cv2.Stitcher_OK:
            # Resize the stitched region to the overlap width and output height
            stitched = cv2.resize(stitched, (overlap_width, output_height))

            # Copy the stitched region to the middle of the output frame
            output_frame = np.copy(frame1)
            output_frame[:, input_width - overlap_width:input_width] = stitched

            # Copy the right half of the second frame to the right of the output frame
            output_frame[:, input_width:] = frame2[:, overlap_width:]

            # Write the output frame to the output file
            out.write(output_frame)

            # Show the output frame on the screen
            cv2.imshow("Output", output_frame)

            # Wait for a key press or 10 milliseconds
            key = cv2.waitKey(10) & 0xFF

            # If the key is ESC, break the loop
            if key == 27:
                break

        else:
            # Print an error message if the stitching failed
            print("Stitching failed")

    else:
        # Break the loop if any of the frames are invalid
        break
    
cap1.release() cap2.release() out.release()
