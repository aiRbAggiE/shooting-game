import pygame
pygame.init()

# set up window with size
# in pygame, 0 0 is the TOP LEFT of the screen, instead of the middle of the screen
win = pygame.display.set_mode((800, 400))
screenWidth = 800
screenHeight = 400

# window name
pygame.display.set_caption('Fun Game')

# loading player images
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.png')
char = pygame.image.load('standing.png')

# set up clock, helping set up the FPS later
clock = pygame.time.Clock()

# loading sound effects and music
bulletSound = pygame.mixer.Sound('bullet.wav')
hitSound = pygame.mixer.Sound('hit.wav')
music = pygame.mixer.music.load('music.mp3')

# keep music continuously playing
pygame.mixer.music.play(-1)

# add score variable
score = 0


# use OOP to optimize the code
class Player(object):
    # set up character attribute
    def __init__(self, x, y, width, height):
        # starting position
        self.x = x
        self.y = y
        # width and height should equal to the dimension of the character animation image
        self.width = width
        self.height = height
        # velocity: move speed
        self.vel = 5
        # set variable for jump
        self.isJump = False
        self.jumpCount = 10
        # set variable to track moving direction in order to display animation image accurately
        self.left = False
        self.right = False
        self.walkCount = 0
        # tracking if the character is not moving
        self.standing = True
        # add rectangle hit box around the player character: (x, y, width, height)
        self.hitbox = (self.x + 15, self.y + 10, 28, 58)

    # create function to redraw game window every time the character moves
    def draw(self, win):
        # draw character with images
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        # while moving
        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        # while standing after moving
        else:
            # standing facing right after walking right
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            # standing facing left after walking left
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        # add green rectangle hit box around the player character: (x, y, width, height)
        self.hitbox = (self.x + 15, self.y + 10, 28, 58)
        # no longer need showing the hit box below: rect(Surface, color, Rect, width=0)
        # pygame.draw.rect(win, (0, 255, 0), self.hitbox, 2)

    def hit(self):
        # reset character
        self.x = 10
        self.y = 290
        self.walkCount = 0
        self.isJump = False
        self.jumpCount = 10

        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))

        # use built-in function to display the text in the center of the screen (x)
        win.blit(text, (screenWidth/2 - text.get_width()/2, 170))
        pygame.display.update()

        # pause the text display
        i = 0
        while i < 300:
            pygame.time.delay(5)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

    def win(self):
        font2 = pygame.font.SysFont('comicsans', 80)
        text = font2.render('WIN!', 1, (0, 70, 200))
        win.blit(text, (screenWidth/2 - text.get_width()/2, 170))
        pygame.display.update()


class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        # use facing = 1 or -1 to indicate direction
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        # draw bullet circle(Surface, color, pos, radius, width=0)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class Enemy(object):
    # loading enemy images
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    # set up enemy attribute
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.vel = 4
        self.walkCount = 0
        # path represents where we start and where we end
        self.path = [self.x, self.end]
        # add rectangle hit box around the enemy character: (x, y, width, height)
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        # add attributes to track enemy HP
        self.health = 9
        self.visible = True

    def move(self):
        # when enemy is moving right
        if self.vel > 0:
            # allow enemy to move
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            # otherwise, change direction
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def draw(self, win):
        # every time we draw enemy, move first before draw
        self.move()

        # if enemy has health
        if self.visible:
            # draw enemy with images
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            # when moving right
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            # when moving left
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            # draw a red health bar and a green health bar: rect(Surface, color, Rect, width=0)
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 40, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 4 * (1 + self.health), 10))

            # add red rectangle hit box around the enemy character: (x, y, width, height)
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            # no longer need showing the hit box below: rect(Surface, color, Rect, width=0)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')


def redrawGameWindow():
    # fill the screen with background image(file name, position)
    win.blit(bg, (0, 0))
    # score text
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (650, 25))

    # draw player character
    man.draw(win)

    if goblin.visible is True:
        # draw enemy character
        goblin.draw(win)
        # draw bullets
        for bullet in bullets:
            bullet.draw(win)
    else:
        man.win()

    pygame.display.update()


### MAIN LOOP ###

# set up font for display of the score: SysFont(name, size, bold=False, italic=False)
font = pygame.font.SysFont('comicsans', 30, True)

# create instances and pass in the arguments
man = Player(5, 290, 64, 64)
goblin = Enemy(35, 295, 64, 64, 730)

# create a list to store all bullets
bullets = []

# use shootloop in the main loop to add cool down function to shooting
shootloop = 0

run = True
while run:
    # set up FPS: how many frames you see per second
    clock.tick(27)

    # check character collision only if the goblin is visible
    if goblin.visible is True:
        if man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1] and man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5

    if shootloop > 0:
        shootloop += 1
    if shootloop > 3:
        shootloop = 0

    # check for a event
    for event in pygame.event.get():
        # if player click the exit button 'x'
        if event.type == pygame.QUIT:
            run = False

    # shoot
    if goblin.visible is True:
        for bullet in bullets:
            # check collision: bullet within enemy hit box
            if bullet.y + bullet.radius > goblin.hitbox[1] and bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    # play the hit sound effect
                    hitSound.play()

                    goblin.hit()
                    score += 10
                    bullets.pop(bullets.index(bullet))

            # shoot bullet which is in the screen
            if bullet.x < screenWidth and bullet.x > 0:
                bullet.x += bullet.vel
            # delete the bullet which is out of the screen
            else:
                bullets.pop(bullets.index(bullet))

    # move character
    keys = pygame.key.get_pressed()
    # set up boundaries for movement
    # track moving direction
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < screenWidth - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.walkCount = 0
        # adding standing status
        man.standing = True

    # set up jumping
    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.left = False
            man.right = False
            man.walkCount = 0
    # disable move up and down while jumping
    else:
        if man.jumpCount >= -10:
            # use neg here to jumping up once and falling down
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            # jumping up
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1

        else:
            man.isJump = False
            man.jumpCount = 10

    # shoot the bullet when goblin is visible
    if goblin.visible is True:
        if keys[pygame.K_SPACE] and shootloop == 0:
            # play the bullet sound effect
            bulletSound.play()

            if man.left:
                facing = -1
            else:
                facing = 1
            if len(bullets) < 5:
                # append bullet instance to the bullets array
                # round number x and y indicates that the bullet is shooting from the center of the character
                # 6 = radium; (0, 0, 0) = black
                bullets.append(
                    Projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))
            shootloop = 1

    redrawGameWindow()

pygame.quit()
