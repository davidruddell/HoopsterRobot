def main():
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            break

        # Your processing code here
        # For example, let's just display the frame
        og_Image = frame.copy()
        cropped_images, cornerx, cornery = detect_and_crop_object(frame)

        # Check if cropped_images is not empty
        if cropped_images:
            hoop_width, hoop_center_x = find_basketball_hoop_width(cropped_images[0], og_Image, cornerx, cornery)
            #backboard_width = find_backboard_width(cropped_images[1])

            print("The width of the Basketball Hoop is:", hoop_width, "px")
            print("The difference between the the center of hoop vs center of image:", hoop_center_x, "px [CI - CH]")
            #print("The width of the Backboard is:", backboard_width, "px")

            distance_to_rim = calculate_distance_to_rim(hoop_width, camera_fov_degrees_h, sensor_width_mm, sensor_height_mm, known_rim_width_mm)
            print(f"The distance from the camera to the basketball rim is approximately {distance_to_rim:.2f} meters.")

            #angle_between_points = calculate_angle_between_points(hoop_center_x, camera_fov_degrees_h, distance_to_rim, sensor_width_mm, sensor_height_mm)
            #print(f"The angle between the two points is approximately {angle_between_points:.2f} degrees.")
            print(distance_to_rim)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture and destroy the windows
    cap.release()
    cv2.destroyAllWindows()