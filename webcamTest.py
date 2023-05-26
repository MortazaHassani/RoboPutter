import cv2

# Open the video capture
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

# Set the desired resolution
width = 1280
height = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Check if the resolution was set successfully
actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print("Actual Resolution: {} x {}".format(actual_width, actual_height))

# Start capturing and displaying frames
while True:
    ret, frame = cap.read()
    
    # Perform any processing or display operations here
    
    cv2.imshow("Webcam", frame)
    
    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close any open windows
cap.release()
cv2.destroyAllWindows()
