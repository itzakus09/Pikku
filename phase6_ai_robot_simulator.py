import cv2
import pygame
import sys

# ---------------- CAMERA SETUP ----------------
face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cam = cv2.VideoCapture(0)

# ---------------- PYGAME ROBOT SIM ----------------
pygame.init()
WIDTH, HEIGHT = 500, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PHASE 6 - AI Robot Simulator")

robot_x, robot_y = WIDTH//2, HEIGHT//2
speed = 4

font = pygame.font.SysFont("arial", 24)

# ---------------- MAIN LOOP ----------------
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            cam.release()
            cv2.destroyAllWindows()
            sys.exit()

    ret, frame = cam.read()
    if not ret:
        break

    h, w, _ = frame.shape
    center_x = w // 2

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray, 1.3, 5)

    direction = "STOP"

    for (x, y, fw, fh) in faces:
        face_center = x + fw // 2

        if face_center < center_x - 40:
            direction = "LEFT"
        elif face_center > center_x + 40:
            direction = "RIGHT"
        else:
            direction = "FORWARD"

        cv2.rectangle(frame, (x,y), (x+fw,y+fh), (0,255,0), 2)
        cv2.putText(frame, direction, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)

    cv2.line(frame, (center_x,0), (center_x,h), (255,0,0), 2)
    cv2.imshow("AI Vision", frame)

    # ---------------- ROBOT MOVEMENT ----------------
    if direction == "FORWARD":
        robot_y -= speed
    elif direction == "LEFT":
        robot_x -= speed
    elif direction == "RIGHT":
        robot_x += speed

    robot_x = max(0, min(WIDTH, robot_x))
    robot_y = max(0, min(HEIGHT, robot_y))

    # ---------------- DRAW ROBOT ----------------
    screen.fill((240,240,240))
    pygame.draw.rect(screen, (0,0,255), (robot_x, robot_y, 25, 25))

    text = font.render("DIR: " + direction, True, (255,0,0))
    screen.blit(text, (10,10))

    pygame.display.update()

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()
pygame.quit()