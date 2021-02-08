import pygame, pymunk, sys
# Initial setting
pygame.init()
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 60
# Mouse trigger
mouse_trigger = False
# Screen setting
screen_width, screen_height = 800, 480
screen = pygame.display.set_mode((screen_width, screen_height))
window_name = "Pymunk"
pygame.display.set_caption(window_name)
# Color
color_bg = (50, 60, 50)
color_ball = (190, 200, 230)
color_payer = (240, 250, 10)
color_line = (210, 190, 189)
color_score = (240, 20, 20)
# Window collide area
left = 3
right = screen_width - left
top = 3
bottom = screen_height - top
middle_x = screen_width / 2
middle_y = screen_height / 2
center = (middle_x, middle_y)
h = abs(top - bottom)
w = abs(left - right)
# Player control
player_up = False
player_down = False
player_left = False
player_right = False
class Ball():
    def __init__(self):
        self.body = pymunk.Body()
        self.body.position = center
        self.body.velocity = 5, -10
        self.radius = 10
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = 1
        self.shape.elasticity = 1
        space.add(self.body, self.shape)
        self.shape.collision_type = 1
    def draw(self):
        x, y = self.body.position
        pygame.draw.circle(screen, color_ball, (int(x), int(y)), self.radius)
    def reset(self, space, arbiter, data):
        self.body.position = center
        self.body.velocity = 5, -10
        return False
class Wall():
    def __init__(self, p1 ,p2, collision_number = None):
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, 10)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)
        if collision_number:
            self.shape.collision_type = collision_number

    def draw(self, color = color_line, width = 5):
        pygame.draw.line(screen, color, self.shape.a, self.shape.b, width)
class Player():
    def __init__(self, position_x):
        self.body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
        self.body.position = position_x, middle_y
        self.radius = 15
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)
    def draw(self):
        pygame.draw.circle(screen, color_payer, self.body.position, self.radius)
    def move(self, direction):
        v_x, v_y = self.body.velocity
        x, y = self.body.position
        directions = ("UP", "DOWN", "LEFT", "RIGHT")
        velocity = 20
        if direction == directions[0]:
            self.body.velocity = v_x, -velocity
        if direction == directions[1]:
            self.body.velocity = v_x, velocity
        if direction == directions[2]:
            self.body.velocity = -velocity, v_y
        if direction == directions[3]:
            self.body.velocity = velocity, v_y
        # Active area
        if y <= top + self.radius and direction == directions[0]:
            self.body.velocity = v_x, 0
        if y >= bottom - self.radius and direction == directions[1]:
            self.body.velocity = v_x, 0
        if x <= middle_x + self.radius and direction == directions[2]:
            self.body.velocity = 0,v_y
        if x >= right - self.radius and direction == directions[3]:
            self.body.velocity = 0, v_y
    def stop(self):
        self.body.velocity = 0, 0

def airhockey():
    global mouse_trigger, quit_game
    quit_game = False
    ball = Ball()
    player_1 = Player(left+15)
    player_2 = Player(right-15)
    wall_left = Wall([left, top], [left, bottom])
    wall_right = Wall([right, top], [right, bottom])
    wall_top = Wall([left, top], [right, top])
    wall_bottom = Wall([left, bottom], [right, bottom])
    # Score
    score_1 = Wall([right, top + h/3], [right, bottom - h/3], 2)
    score_2 = Wall([left, top + h/3], [left, bottom - h/3], 2)
    scored = space.add_collision_handler(1, 2)
    scored.begin = ball.reset
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Control player
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            #print("up")
            player_2.move("UP")
        else:
            player_2.stop()
        if key[pygame.K_DOWN]:
            #print("down")
            player_2.move("DOWN")
        if key[pygame.K_LEFT]:
            #print("left")
            player_2.move("LEFT")
        if key[pygame.K_RIGHT]:
            #print("right")
            player_2.move("RIGHT")
        # Draw object
        screen.fill(color_bg)
        wall_left.draw()
        wall_right.draw()
        wall_top.draw()
        wall_bottom.draw()
        ball.draw()
        player_1.draw()
        player_2.draw()
        pygame.draw.aaline(screen, color_line, (screen_width / 2, 0), (screen_width / 2, screen_height))
        # Score
        score_1.draw(color=color_score, width=10)
        score_2.draw(color=color_score, width=10)
        # Update
        pygame.display.flip()
        space.step(1/FPS)
if __name__ == "__main__":
    airhockey()

