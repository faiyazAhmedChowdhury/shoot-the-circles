from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import time


W_Width, W_Height = 850, 900
flag = 0
bullet = []
score = 0
miss = 0
pause = False
gameover = 0
normal_bubble_count = 0  # Track the number of bubbles hit
game_over_printed = False


class Bubble:
    def __init__(self, existing_bubbles):
        self.x = self.generate_x(existing_bubbles)
        self.y = 330
        self.r = random.randint(20, 25)
        self.color = [1, 0.647, 0]
        self.active = True  # Bubble currently active

    def generate_x(self, existing_bubbles):
        while True:
            x = random.randint(-390, 390)
            # Check for overlap with bubbles
            if all(abs(x - b.x) >= b.r + 20 for b in existing_bubbles if b.active):
                return x

class SpecialBubble(Bubble):
    def __init__(self, existing_bubbles):
        super().__init__(existing_bubbles)
        self.original_r = self.r
        self.expand = True
        self.point_value = 3     # More points for hitting special bubble

    def update_size(self):
        """Update the radius to expand and shrink."""
        if self.expand:
            self.r += 0.5  # speed for size change
            if self.r >= self.original_r + 10:  # Max size
                self.expand = False
        else:
            self.r -= 0.5  # speed for size change
            if self.r <= self.original_r - 5:  # Min size
                self.expand = True

class Shooter:
    def __init__(self):
        self.x = 0
        self.color = [1, 1, 1]

# Initialize bubbles with a mix of normal and special ones
def initialize_bubbles():
    existing_bubbles = []
    for _ in range(5):
        bubble = Bubble(existing_bubbles)
        existing_bubbles.append(bubble)
    return existing_bubbles

bubble = initialize_bubbles()
shooter = Shooter()

#------------ Mid-Point Line Drawing Algorithm ---------------#

def plot_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def convert_to_zone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)

def originalzone(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)

def midpoint_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    zone = 0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx >= 0 and dy < 0:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy < 0:
            zone = 6

    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)

    x, y = x1, y1
    x0, y0 = originalzone(x, y, zone)
    plot_point(x0, y0)

    while x < x2:
        if d <= 0:
            d += incrE
            x += 1
        else:
            d += incrNE
            x += 1
            y += 1
        x0, y0 = originalzone(x, y, zone)
        plot_point(x0, y0)

#-------- Mid-Point Circle Drawing Algorithm -----------#

def midpointcircle(radius, centerX=0, centerY=0):
    glBegin(GL_POINTS)
    x = 0
    y = radius
    d = 1 - radius
    while y > x:
        glVertex2f(x + centerX, y + centerY)
        glVertex2f(x + centerX, -y + centerY)
        glVertex2f(-x + centerX, y + centerY)
        glVertex2f(-x + centerX, -y + centerY)
        glVertex2f(y + centerX, x + centerY)
        glVertex2f(y + centerX, -x + centerY)
        glVertex2f(-y + centerX, x + centerY)
        glVertex2f(-y + centerX, -x + centerY)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * x - 2 * y + 5
            y -= 1
        x += 1
    glEnd()

# Bullet drawing with midpoint circle
def draw_bullet():
    global bullet
    glPointSize(3)
    glColor3f(1, 0, 0)
    for i in bullet:
        midpointcircle(8, i[0], i[1])

# Bubble drawing function
def draw_bubble():
    global bubble
    glPointSize(3)
    for b in bubble:
        if isinstance(b, SpecialBubble):  # Special bubbles
            b.update_size()
            glColor3f(0.678, 1, 0.184)
        else:
            glColor3f(b.color[0], b.color[1], b.color[2])
        midpointcircle(b.r, b.x, b.y)


def draw_jet_plane(centerX, centerY, size):
    # Jet plane body
    body_length = size * 4
    body_width = size * 1.5
    wing_length = size * 5
    wing_width = size * 0.5
    tail_length = size * 1.5
    tail_width = size * 0.5

    # Coordinates for body
    left_body_x = centerX - body_width / 2
    right_body_x = centerX + body_width / 2
    bottom_body_y = centerY
    nose_y = centerY + body_length

    # Draw jet plane body (darker grey)
    glColor3f(0.5, 0.5, 0.5)
    midpoint_line(left_body_x, bottom_body_y, right_body_x, bottom_body_y)
    midpoint_line(left_body_x, bottom_body_y, centerX, nose_y)
    midpoint_line(right_body_x, bottom_body_y, centerX, nose_y)

    # Draw connected wings (grey)
    glColor3f(0.7, 0.7, 0.7)
    wing_y = bottom_body_y - wing_width

    midpoint_line(centerX - wing_length / 2, wing_y, left_body_x, bottom_body_y)
    midpoint_line(centerX + wing_length / 2, wing_y, right_body_x, bottom_body_y)
    midpoint_line(centerX - wing_length / 2, wing_y, centerX + wing_length / 2, wing_y)


    glColor3f(0.5, 0.5, 0.5)
    body_between_wings_y = bottom_body_y + body_length / 2
    midpoint_line(left_body_x, body_between_wings_y, right_body_x, body_between_wings_y)
    midpoint_line(left_body_x, body_between_wings_y, centerX, nose_y)
    midpoint_line(right_body_x, body_between_wings_y, centerX, nose_y)


    glColor3f(1.0, 0.5, 0.0)
    tail_y = bottom_body_y - tail_length

    # Left tail
    tail_left_x = centerX - tail_width
    midpoint_line(tail_left_x, tail_y, tail_left_x + tail_width, tail_y)
    midpoint_line(tail_left_x, tail_y, centerX, bottom_body_y)

    # Middle tail
    midpoint_line(centerX - tail_width / 2, tail_y, centerX + tail_width / 2, tail_y)
    midpoint_line(centerX - tail_width / 2, tail_y, centerX, bottom_body_y)

    # Right tail
    tail_right_x = centerX + tail_width
    midpoint_line(tail_right_x, tail_y, tail_right_x - tail_width, tail_y)
    midpoint_line(tail_right_x, tail_y, centerX, bottom_body_y)

# Update interface function
def interface():
    global shooter

    glPointSize(2)
    glColor3f(shooter.color[0], shooter.color[1], shooter.color[2])
    draw_jet_plane(centerX=shooter.x, centerY=-365, size=12)

    # Left button
    glPointSize(4)
    glColor3f(0, 0.8, 1)
    midpoint_line(-355, 350, -330, 350)
    glPointSize(3)
    midpoint_line(-355, 350, -345, 360)
    midpoint_line(-355, 350, -345, 340)

    # Right Cross Button
    glPointSize(4)
    glColor3f(0.9, 0, 0)
    midpoint_line(355, 362, 330, 338)
    midpoint_line(355, 338, 330, 362)

    # Middle Pause Button
    glPointSize(4)
    glColor3f(1 , .5, 0)
    if pause:
        midpoint_line(-10, 365, -10, 335)
        midpoint_line(-10, 365, 10, 350)
        midpoint_line(-10, 335, 10, 350)
    else:
        midpoint_line(-7, 365, -7, 335)
        midpoint_line(7, 365, 7, 335)




def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y
    return a, b

# Setting up keyboard, using space to shoot and a to move left and d to move right
def keyboardListener(key, x, y):
    global bullet, pause, gameover, shooter
    if key == b' ':
        if not pause and gameover < 3:
            bullet.append([shooter.x, -365])
    elif key == b'a' or key == b'A':
        if shooter.x > -390 and not pause:
            shooter.x -= 15  # Increased speed
    elif key == b'd' or key == b'D':
        if shooter.x < 390 and not pause:  # Adjusted for width
            shooter.x += 15  # Increased speed
    glutPostRedisplay()

# Mouse listener
def mouseListener(button, state, x, y):
    # print("coordinates : X", x)
    # print("coordinates : Y" ,y)
    global pause, gameover, shooter, score, bubble, bullet, miss, game_over_printed
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)

        # Restart button
        glPointSize(4)
        glColor3f(1, 1, 1)
        midpoint_line(-360, 345, -330, 365)
        if -390 < c_x < -345 and 370 < c_y < 415:
            pause = False
            print('Starting Over')
            bubble = initialize_bubbles()
            score = 0
            miss = 0
            gameover = 0
            bullet = []
            game_over_printed = False

        # Red cross button
        elif 355 < c_x < 385 and 375 < c_y < 410:
            game_over_printed = False
            print('Goodbye! Score:', score)# Terminate the program
            pause = True
            bubble = []
            glutDestroyWindow(glutGetWindow())
            # exit(0)
        # Pause button
        elif -15 < c_x < 15 and 375 < c_y < 415:
            pause = not pause
            print("Game Paused" if pause else "Game Resumed")
    glutPostRedisplay()

# Display function
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    interface()
    draw_bullet()
    #print(bool(glutLeaveMainLoop))
    draw_bubble()
    glutSwapBuffers()

# Main animation of falling bubbles from the top with delta timing
def animate():
    current_time = time.time()
    delta_time = current_time - animate.start_time if hasattr(animate, 'start_time') else 0
    animate.start_time = current_time

    global pause, bubble, shooter, gameover, score, bullet, miss, normal_bubble_count, game_over_printed
    if not pause and gameover < 3 and miss < 3:
        delidx = []
        for i in range(len(bullet)):
            if bullet[i][1] < 400:  # bullet still inside the screen
                bullet[i][1] += 10
            else:  # bullet goes outside the screen
                delidx.append(i)
                miss += 1
        for j in reversed(delidx):  # Remove from the end to avoid index issues
            del bullet[j]

        for i in range(len(bubble)):
            if bubble[i].active:  # Only update active bubbles
                bubble[i].y -= (10 + score * 5) * delta_time  # All bubbles move down
                if bubble[i].y <= -400:  # Bubble missed
                    miss += 1
                    bubble[i].active = False  # Mark the bubble as inactive

                    # Create a new bubble only if no other bubble is active in the same x position
                    if all(b.x != bubble[i].x or not b.active for b in bubble):
                        bubble[i] = SpecialBubble(bubble) if random.random() < 0.2 else Bubble(bubble)

                # Check collision with shooter
                if abs(bubble[i].y - -345) < (bubble[i].r) and abs(bubble[i].x - shooter.x) < (bubble[i].r + 20):
                    gameover += 3  # Game over

                for j in range(len(bullet)):  # collision with bullet and bubbles
                    if abs(bubble[i].y - bullet[j][1]) < (bubble[i].r + 15) and abs(bubble[i].x - bullet[j][0]) < (bubble[i].r + 20):
                        if isinstance(bubble[i], SpecialBubble):
                            score += bubble[i].point_value
                        else:
                            score += 1
                            normal_bubble_count += 1
                        print("Score:", score)
                        if normal_bubble_count >= 5:
                            bubble[i] = SpecialBubble(bubble)
                            normal_bubble_count = 0
                        else:
                            bubble[i] = Bubble(bubble)
                        bubble.sort(key=lambda b: b.y)
                        del bullet[j]
                        break

    if gameover >= 3 or miss >= 3 and not pause:
        if not game_over_printed:
            print("Game Over! Final Score:", score)
            game_over_printed = True
        pause = True
        bubble = []
        bullet = []

    time.sleep(1 / 1000)
    glutPostRedisplay()

# Initialization function
def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-400, 400, -400, 400, -1, 1)

# GLUT setup
glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"Assignment-02_22101848")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()
