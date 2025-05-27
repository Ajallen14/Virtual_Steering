import math
import keyinput
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize video capture
cap = cv2.VideoCapture(0)

# Configuration parameters
STEERING_SENSITIVITY = 65  # Adjust this value based on your needs
CIRCLE_RADIUS = 150
LINE_THICKNESS = 15

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Image processing
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        imageHeight, imageWidth, _ = image.shape

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        co = []  # Coordinates list
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                
                for point in mp_hands.HandLandmark:
                    if str(point) == "HandLandmark.WRIST":
                        normalizedLandmark = hand_landmarks.landmark[point]
                        pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(
                            normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)

                        try:
                            co.append(list(pixelCoordinatesLandmark))
                        except:
                            continue

        # Steering logic
        if len(co) == 2:
            xm, ym = (co[0][0] + co[1][0]) / 2, (co[0][1] + co[1][1]) / 2  # Midpoint
            
            try:
                m = (co[1][1] - co[0][1]) / (co[1][0] - co[0][0])  # Slope
            except ZeroDivisionError:
                continue

            # Calculate intersection points with circle
            a = 1 + m ** 2
            b = -2 * xm - 2 * co[0][0] * (m ** 2) + 2 * m * co[0][1] - 2 * m * ym
            c = xm ** 2 + (m ** 2) * (co[0][0] ** 2) + co[0][1] ** 2 + ym ** 2 - 2 * co[0][1] * ym - 2 * co[0][1] * co[0][0] * m + 2 * m * ym * co[0][0] - CIRCLE_RADIUS ** 2
            
            try:
                xa = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
                xb = (-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
                ya = m * (xa - co[0][0]) + co[0][1]
                yb = m * (xb - co[0][0]) + co[0][1]
            except:
                continue

            # Calculate perpendicular line
            if m != 0:
                ap = 1 + ((-1/m) ** 2)
                bp = -2 * xm - 2 * xm * ((-1/m) ** 2) + 2 * (-1/m) * ym - 2 * (-1/m) * ym
                cp = xm ** 2 + ((-1/m) ** 2) * (xm ** 2) + ym ** 2 + ym ** 2 - 2 * ym * ym - 2 * ym * xm * (-1/m) + 2 * (-1/m) * ym * xm - CIRCLE_RADIUS ** 2
                
                try:
                    xap = (-bp + (bp ** 2 - 4 * ap * cp) ** 0.5) / (2 * ap)
                    xbp = (-bp - (bp ** 2 - 4 * ap * cp) ** 0.5) / (2 * ap)
                    yap = (-1 / m) * (xap - xm) + ym
                    ybp = (-1 / m) * (xbp - xm) + ym
                except:
                    continue

            # Draw steering elements
            cv2.circle(img=image, center=(int(xm), int(ym)), radius=CIRCLE_RADIUS, 
                      color=(195, 255, 62), thickness=LINE_THICKNESS)
            cv2.line(image, (int(xa), int(ya)), (int(xb), int(yb)), 
                    (195, 255, 62), LINE_THICKNESS)

            # Calculate distance between hands
            distance = math.sqrt((co[0][0] - co[1][0]) ** 2 + (co[0][1] - co[1][1]) ** 2)
            
            # Determine steering direction
            keyinput.release_key('a')
            keyinput.release_key('d')
            keyinput.release_key('s')
            
            if co[0][0] > co[1][0] and co[0][1] > co[1][1] and co[0][1] - co[1][1] > STEERING_SENSITIVITY:
                print("Turn left.")
                keyinput.press_key('a')
                cv2.putText(image, "Turn left", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.line(image, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), LINE_THICKNESS)

            elif co[1][0] > co[0][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > STEERING_SENSITIVITY:
                print("Turn left.")
                keyinput.press_key('a')
                cv2.putText(image, "Turn left", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.line(image, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), LINE_THICKNESS)

            elif co[0][0] > co[1][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > STEERING_SENSITIVITY:
                print("Turn right.")
                keyinput.press_key('d')
                cv2.putText(image, "Turn right", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.line(image, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), LINE_THICKNESS)

            elif co[1][0] > co[0][0] and co[0][1] > co[1][1] and co[0][1] - co[1][1] > STEERING_SENSITIVITY:
                print("Turn right.")
                keyinput.press_key('d')
                cv2.putText(image, "Turn right", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.line(image, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), LINE_THICKNESS)
            
            else:
                print("Keeping straight")
                keyinput.press_key('w')
                cv2.putText(image, "Keep straight", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                if ybp > yap:
                    cv2.line(image, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), LINE_THICKNESS)
                else:
                    cv2.line(image, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), LINE_THICKNESS)

        elif len(co) == 1:
            print("Keeping back")
            keyinput.release_key('a')
            keyinput.release_key('d')
            keyinput.release_key('w')
            keyinput.press_key('s')
            cv2.putText(image, "Keeping back", (50, 50), font, 1.0, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the image
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

        # Exit condition
        if cv2.waitKey(5) & 0xFF == ord('q'):
            # Release all keys before exiting
            keyinput.release_key('a')
            keyinput.release_key('d')
            keyinput.release_key('w')
            keyinput.release_key('s')
            break

# Cleanup
cap.release()
cv2.destroyAllWindows()