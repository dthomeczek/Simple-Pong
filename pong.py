import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15
INITIAL_BALL_SPEED = 5
BALL_SPEED_INCREMENT = 0.5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
clock = pygame.time.Clock()

# Set up the window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    def draw(self):
        pygame.draw.rect(window, WHITE, self.rect)

    def move(self, dy):
        self.rect.y += dy
        # Keep paddle within the screen bounds
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
    
# Ball class
class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.vx = INITIAL_BALL_SPEED  # Initial ball velocity along x-axis
        self.vy = INITIAL_BALL_SPEED  # Initial ball velocity along y-axis

    def draw(self):
        pygame.draw.rect(window, WHITE, self.rect)

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        # Check for collision with top or bottom of the window
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vy = -self.vy

# Paddle positions
paddle_1 = Paddle(50, HEIGHT//2 - PADDLE_HEIGHT//2)
paddle_2 = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)

# Ball position
ball = Ball(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2)

# Score variables
score_1 = 0
score_2 = 0
font = pygame.font.Font(None, 50)

# Score limit
SCORE_LIMIT = 11

# Add this updated ai_move() function
def ai_move(ball, paddle):
    # Only make a prediction if the ball is moving towards the AI paddle
    if ball.vx > 0:
        # Calculate the predicted y-coordinate where the ball will intersect the paddle's x-coordinate
        predict_y = ball.rect.y + ((paddle.rect.x - ball.rect.x) * ball.vy / ball.vx)
        
        # Limit the predicted y-coordinate within the height of the window
        predict_y = min(max(predict_y, PADDLE_HEIGHT // 2), HEIGHT - PADDLE_HEIGHT // 2)
        
        # Move the paddle towards the predicted y-coordinate, considering the direction of the ball's movement
        if paddle.rect.centery < predict_y:
            paddle.move(5)
        elif paddle.rect.centery > predict_y:
            paddle.move(-5)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    # Move paddles
    if keys[pygame.K_UP]:
        paddle_1.move(-5)
    if keys[pygame.K_DOWN]:
        paddle_1.move(5)
    
    # AI player movement
    ai_move(ball, paddle_2)

    # Clear the screen
    window.fill(BLACK)

    # Draw paddles and ball
    paddle_1.draw()
    paddle_2.draw()
    ball.draw()

    # Move the ball
    ball.move()

# Check for collision with paddles
    if ball.rect.colliderect(paddle_1.rect):
        ball.vx = -ball.vx
        # Increase ball speed each time it hits a paddle
        ball.vx += BALL_SPEED_INCREMENT
        ball.vy += BALL_SPEED_INCREMENT
    elif ball.rect.colliderect(paddle_2.rect):
        ball.vx = -ball.vx
        # Increase ball speed each time it hits a paddle
        ball.vx -= BALL_SPEED_INCREMENT
        ball.vy -= BALL_SPEED_INCREMENT

    # Check for scoring
    if ball.rect.left <= 0:
        score_2 += 1
        ball.rect.x = WIDTH//2 - BALL_SIZE//2
        ball.rect.y = HEIGHT//2 - BALL_SIZE//2
        ball.vx = INITIAL_BALL_SPEED  # Reset ball speed
        ball.vy = INITIAL_BALL_SPEED  # Reset ball speed
    elif ball.rect.right >= WIDTH:
        score_1 += 1
        ball.rect.x = WIDTH//2 - BALL_SIZE//2
        ball.rect.y = HEIGHT//2 - BALL_SIZE//2
        ball.vx = INITIAL_BALL_SPEED  # Reset ball speed
        ball.vy = INITIAL_BALL_SPEED  # Reset ball speed


    # Display scores
    score_text = font.render(f"{score_1}   {score_2}", True, WHITE)
    window.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

    # Check for score limit
    if score_1 >= SCORE_LIMIT or score_2 >= SCORE_LIMIT:
        # Display winner
        winner_text = font.render("Player 1 Wins!" if score_1 >= SCORE_LIMIT else "Player 2 Wins!", True, WHITE)
        window.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2 - winner_text.get_height()//2))
        pygame.display.flip()
        pygame.time.delay(3000)  # Delay for 3 seconds before quitting
        pygame.quit()
        sys.exit()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)