import cv2
import numpy as np
import math
from ultralytics import YOLO
import time

# Initialize the YOLOv8n model
# model = YOLO('ComputerVision/Saul.pt')
global calcDistanceAndVelocity_startTime

# #img_path = 'ComputerVision/6.png'
# #og_Image = cv2.imread(img_path)

# cap = cv2.VideoCapture(0)

# sensor_width_mm = 8.0  # From the provided specifications
# sensor_height_mm = 6.0  # From the provided specifications
# camera_fov_degrees_h = 78.0  # From the provided specifications
# known_rim_width_mm = 457.2  # Known width of an NBA-regulated basketball rim in millimeters


model = YOLO('ComputerVision/Saul.pt')


#img_path = 'ComputerVision/6.png'
#og_Image = cv2.imread(img_path)

cap = cv2.VideoCapture(0)

sensor_width_mm = 8.0  # From the provided specifications
sensor_height_mm = 6.0  # From the provided specifications
camera_fov_degrees_h = 78.0  # From the provided specifications
known_rim_width_mm = 457.2  # Known width of an NBA-regulated basketball rim in millimeters



def calculate_distance_to_rim(hoop_width_px, camera_fov_degrees_h, sensor_width_mm, sensor_height_mm, known_rim_width_mm):
    """
    Calculates the distance from the camera to the basketball rim.
    """
    # Convert horizontal field of view to radians
    fov_rad_h = camera_fov_degrees_h * math.pi / 180

    # Calculate the focal length of the camera using the sensor dimensions and horizontal field of view
    focal_length_mm = sensor_width_mm / (2 * math.tan(fov_rad_h / 2))

    # Calculate the distance to the rim using the known rim width and the measured width in pixels
    distance_to_rim_m = (known_rim_width_mm * focal_length_mm) / (hoop_width_px * sensor_width_mm / sensor_height_mm)

    return distance_to_rim_m

def calculate_angle_between_points(distance_between_points_px, fov_degrees_h, distance_to_center_m, sensor_width_mm, sensor_height_mm):
    """
    Calculates the angle between two points in the camera's field of view where the center
    of the image is aligned with the distance from the camera.
    """
    # Calculate the focal length of the camera using the provided FOV and sensor dimensions
    focal_length_mm = sensor_width_mm / (2 * math.tan(math.radians(fov_degrees_h / 2)))

    # Convert the distance between points from pixels to meters
    distance_between_points_m = (distance_between_points_px * distance_to_center_m * sensor_width_mm) / (focal_length_mm * sensor_height_mm)

    # Calculate the angle between the two points using the projected distance and sensor width
    angle_radians = math.atan(distance_between_points_m / (distance_to_center_m))
    angle_degrees = angle_radians * (180 / math.pi)

    return angle_degrees

def detect_and_crop_object(img, padding=10):
    """
    Detects objects in the image using YOLOv8n and crops the detected objects with padding.
    Returns a list of cropped images.
    """
    results = model(img, stream=True, device="cpu", conf=0.5, iou=0.7)  # Returns a generator of Results objects
    
    cropped_images = []
    cornerx = None
    cornery = None

    # Process results generator
    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy.int().tolist()[0]

            # Apply padding
            x1 = max(0, x1 - padding)
            cornerx = x1
            y1 = max(0, y1 - padding)
            cornery = y1
            x2 = min(img.shape[1], x2 + padding)
            y2 = min(img.shape[0], y2 + padding)

            # Crop the object from the image
            cropped_img = img[y1:y2, x1:x2]
            cropped_images.append(cropped_img)

            # Apply additional padding for the top and bottom
            width = x2 - x1
            height = y2 - y1
            padding_x = 2 * width
            padding_y_top = 3 * height  # Padding for the top
            padding_y_bottom = round(0.5 * height)  # Padding for the bottom

            x1 = max(0, x1 - padding_x)
            y1 = max(0, y1 - padding_y_top)
            x2 = min(img.shape[1], x2 + padding_x)
            y2 = min(img.shape[0], y2 + padding_y_bottom)

            # Crop the object with additional padding
            cropped_img = img[y1:y2, x1:x2]
            cropped_images.append(cropped_img)

    return cropped_images, cornerx, cornery


def find_backboard_width(img):
    """
    Finds the width of the backboard in the image.
    """
    resized = img.copy()
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    thresh = cv2.dilate(thresh, None, iterations=2)
    thresh = cv2.erode(thresh, None, iterations=1)

    contours, _ = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    contours = contours[1:]
    
    for i, contour in enumerate(contours):
        # Make a copy of the original image
        image_copy = img.copy()
        
        # Draw the current contour on the image copy
        cv2.drawContours(image=image_copy, contours=[contour], contourIdx=-1, color=(255, 0, 0), thickness=cv2.FILLED, lineType=cv2.LINE_AA)
        
        # Save the image with the drawn contour
        cv2.imwrite(f'contour_{i+1}.jpg', image_copy)
        
        # Display the image copy with the drawn contour
        cv2.imshow(f'Contour {i+1}', image_copy)
        cv2.waitKey(0)

    cv2.destroyAllWindows()
    
    largest_contour = max(contours, key=cv2.contourArea)

    image_copy = resized.copy()
    cv2.drawContours(image=image_copy, contours=[largest_contour], contourIdx=-1, color=(255, 0, 0), thickness=cv2.FILLED, lineType=cv2.LINE_AA)
    cv2.imwrite('contours_none_image1.jpg', image_copy)

    epsilon = 0.01 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    image_copy = resized.copy()
    cv2.drawContours(image=image_copy, contours=[approx], contourIdx=-1, color=(0, 255, 0), thickness=cv2.FILLED, lineType=cv2.LINE_AA)
    cv2.imwrite('contours_none_image2.jpg', image_copy)

    largest_contour = cv2.convexHull(approx)

    image_copy = resized.copy()
    cv2.drawContours(image=image_copy, contours=[largest_contour], contourIdx=-1, color=(0, 0, 255), thickness=cv2.FILLED, lineType=cv2.LINE_AA)
    cv2.imwrite('contours_none_image3.jpg', image_copy)

    x, y, width, height = cv2.boundingRect(largest_contour)

    return width

def find_basketball_hoop_width(img, og_Image, cornerx, cornery):
    """
    Finds the width of the basketball hoop in the image and the x-coordinate of the center pixel
    of the bounding box drawn around the basketball hoop. It also paints the center pixel coordinate
    on the image.
    """
    # Initialize w and box_center_x
    w = 0
    box_center_x = 0

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define range for orange color in HSV
    lower_orange = np.array([0, 100, 0], np.uint8)
    upper_orange = np.array([10, 255, 255], np.uint8)

    # Threshold the HSV image to get only orange colors
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Apply dilation and erosion to the mask
    kernel = np.ones((5, 5), np.uint8)
    
    mask = cv2.dilate(mask, kernel, iterations=1)
    mask = cv2.erode(mask, kernel, iterations=1)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img, img, mask=mask)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding box around the largest contour
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        # Calculate the x-coordinate of the center pixel of the bounding box
        box_center_x = x + (w // 2)
        box_center_y = y + (h // 2)

        cv2.rectangle(res, (x, y), (x + w, y + h), (255, 255, 0), 2)
        cv2.rectangle(og_Image, (cornerx + x, cornery + y), (cornerx + x + w, cornery + y + h), (0, 0, 0), 2)

        # Paint the center pixel coordinate on the image
        cv2.circle(res, (box_center_x, box_center_y), 1, (255, 255, 255), -1)
        
        # Get the dimensions of the image
        height, width = og_Image.shape[:2]

        # Calculate the center of the image
        center_x = width // 2

        # Paint the center pixel coordinate onto the original image
        cv2.circle(og_Image, (center_x, cornery + box_center_y), 2, (255, 255, 255), -1)
        cv2.putText(og_Image, 'CI', (center_x, cornery + box_center_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

        # Paint the center pixel coordinate onto the original image
        cv2.circle(og_Image, (cornerx + box_center_x, cornery + box_center_y), 2, (255, 255, 255), -1)
        cv2.putText(og_Image, 'CH', (cornerx + box_center_x, cornery + box_center_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)

    return w, (center_x - (cornerx + box_center_x))


def main():
    global calcDistanceAndVelocity_startTime
    detect_hoop_startTime = time.time()
    #while True:
        # Capture frame-by-frame
    ret, frame = cap.read()

    # if not ret:
    #     break

    # Your processing code here
    # For example, let's just display the frame
    og_Image = frame.copy()
    cropped_images, cornerx, cornery = detect_and_crop_object(frame)

    # Check if cropped_images is not empty
    if cropped_images:
        detect_hoop_endTime = time.time()
        detect_azimuth_startTime = time.time()
        hoop_width, hoop_center_x = find_basketball_hoop_width(cropped_images[0], og_Image, cornerx, cornery)
        #backboard_width = find_backboard_width(cropped_images[1])

        print("The width of the Basketball Hoop is:", hoop_width, "px")
        print("The difference between the center of hoop vs center of image:", hoop_center_x, "px [CI - CH]")
        #print("The width of the Backboard is:", backboard_width, "px")
        detect_azimuth_endTime = time.time()

        print(f"The hoop detection took {detect_hoop_endTime - detect_hoop_startTime} seconds to complete.")
        print(f"The azimuth calculation took {detect_azimuth_endTime - detect_azimuth_startTime} seconds to complete.")

        
        calcDistanceAndVelocity_startTime = time.time()
        distance_to_rim = calculate_distance_to_rim(hoop_width, camera_fov_degrees_h, sensor_width_mm, sensor_height_mm, known_rim_width_mm)
        print(f"The distance from the camera to the basketball rim is approximately {distance_to_rim:.2f} meters.")

        #angle_between_points = calculate_angle_between_points(hoop_center_x, camera_fov_degrees_h, distance_to_rim, sensor_width_mm, sensor_height_mm)
        #print(f"The angle between the two points is approximately {angle_between_points:.2f} degrees.")
        print(distance_to_rim)
        return distance_to_rim
    else:
        # print("hitdaelse")
        return -1

    # # Display the resulting frame
    # cv2.imshow('Frame', frame)

    # # Break the loop on 'q' key press
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    # When everything is done, release the capture and destroy the windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()