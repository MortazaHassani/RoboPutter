import cv2
import multiprocessing as mp
import sys

# Function to read frames from the camera
def read_frames(output, image_queue, flag, initial_frames):
    cap = cv2.VideoCapture(0)  # Change the argument to the appropriate camera index if needed
    while True:
        ret, frame = cap.read()
        if not ret:
            flag.value = 0
            break
        output.put(frame)
        if initial_frames.value < 11:
            image_queue.put(frame)
            initial_frames.value += 1
        if flag.value == 0:
            while not output.empty():
                _ = output.get()
            print('End read: Camera Stop', flush=True)
            break
    cap.release()

# Function to convert frames to grayscale and display them
def convert_to_grayscale(input, flag):
    cv2.namedWindow("Grayscale", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Grayscale", 640, 480)
    while True:
        frame = input.get()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Grayscale", gray)
        if cv2.waitKey(1) & 0xFF == ord('q') or flag.value == 0:
            flag.value = 0
            break
    while not input.empty():
        _ = input.get()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Create a multiprocessing Queue to share frames between processes
    frame_queue = mp.Queue()

    # img queue
    image_queue = mp.Queue(maxsize=10)
    initial_frames = mp.Value('i', 1)
    # Create a multiprocessing Value to share the flag variable
    flag = mp.Value('i', 1)  # 1 means the program should continue running

    # Create the processes
    frame_process = mp.Process(target=read_frames, args=(frame_queue, image_queue, flag, initial_frames))
    frame_process.daemon = True
    frame_process.start()

    grayscale_process = mp.Process(target=convert_to_grayscale, args=(frame_queue, flag))
    grayscale_process.start()

    # Wait for the user to terminate the program
    grayscale_process.join()
    flag.value = 0
    # frame_process.join()

    while not image_queue.empty():
        frame = image_queue.get()
        cv2.imshow("Frame", frame)
        cv2.waitKey(2000)  # Wait for 2 seconds
    cv2.destroyAllWindows()

    sys.exit()  # Terminate the program