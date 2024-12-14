import pygame as pg
import random
import sys
pg.init()
pg.font.init()

WIDTH, HEIGHT = 800 * 1.2, 600 * 1.2
win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("QuHacks 2025")

bg_image = pg.image.load("background.png")
bg_image = pg.transform.scale(bg_image, (800 * 1.2, 600 * 1.2))

clock = pg.time.Clock()

health = 100
score = 0

font = pg.font.SysFont("comicsans", 20)

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width, self.height = 50, 50
        self.vel = 5
        self.dir = None
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.cooldown = 0
        self.bullets = pg.sprite.Group()

    def draw(self, win): 
        pg.draw.rect(win, "light green", self.rect)

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        keys = pg.key.get_pressed()
        if keys[pg.K_w] and self.y >= 130:
            self.y -= self.vel
            self.dir = "up"
        if keys[pg.K_s] and self.y <= 530:
            self.y += self.vel
            self.dir = "down"
        if keys[pg.K_a] and self.x >= 0:
            self.x -= self.vel
            self.dir = "left"
        if keys[pg.K_d] and self.x <= 900:
            self.x += self.vel
            self.dir = "right"
        if keys[pg.K_SPACE] and self.cooldown == 0:
            self.cooldown = 10
            self.bullets.add(Bullet(self.rect.centerx, self.rect.centery, self.dir))

        self.bullets.update()
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

class Bullet(pg.sprite.Sprite):
    global health
    def __init__(self, x, y, dir):
        super().__init__()
        self.x = x
        self.y = y
        self.dir = dir
        self.vel = 10
        self.rect = pg.Rect(self.x, self.y, 10, 10)

    def draw(self, win):
        pg.draw.rect(win, "black", self.rect)

    def update(self):
        if health <= 0:
            self.kill()
        if self.dir == "left":
            self.x -= self.vel
        elif self.dir == "right":
            self.x += self.vel
        elif self.dir == "up":
            self.y -= self.vel
        elif self.dir == "down":
            self.y += self.vel
        else:
            self.kill()
        self.rect = pg.Rect(self.x, self.y, 10, 10)
        if not win.get_rect().contains(self.rect):
            self.kill()

class Zombie(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width, self.height = 30, 30
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.vel = 2
    def draw(self, win): 
        pg.draw.rect(win, "dark green", self.rect)
    def pathfinder(self, player):
        vector = pg.math.Vector2(player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        if vector.length() > 0:
            vector.normalize()
            vector.scale_to_length(self.vel)
            self.rect.move_ip(vector)

def spawn_zombie():
    while True:
        x, y = random.randint(0, 900), random.randint(130, 530)
        if abs(x - player.rect.x) > 50 and abs(y - player.rect.y) > 50:
            return Zombie(x, y)

def draw(win):
    global health
    global score
    win.blit(bg_image, (0, 0))
    player.draw(win)
    health_text = font.render(f"health: {health}", True, "white")
    score_text = font.render(f"score: {score}", True, "white")

    win.blit(score_text, (100, 100))
    win.blit(health_text, (200, 100))

    for bullet in player.bullets:
        bullet.draw(win)

    for zombie in zombies:
        zombie.draw(win)
        if pg.sprite.collide_rect(player, zombie):
            text = font.render("", True, "red")
            if health > -2:
                health -= 1
            
        if health <= 0:
            text = font.render("Game Over! Your final score is: " + str(score), True, "red")
            win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        if health == -2:
            pg.time.wait(2000)
            sys.exit()

    pg.display.flip()

def update():
    global score
    global health
    player.update()

    for zombie in zombies:
        zombie.pathfinder(player)

    for bullet in player.bullets:
        if bullet.x <= 0 or bullet.x >= 800 * 1.2 or bullet.y <= 0 or bullet.y >= 600 * 1.2:
            bullet.kill()
    
    for bullet in player.bullets:
        for zombie in zombies:
            if bullet.rect.colliderect(zombie.rect) and health > 0:
                score += 1
                health += 1
                zombie.vel+=0.1
                player.vel+=0.1

player = Player(WIDTH // 2, HEIGHT // 2)

zombies = pg.sprite.Group()
zombies.add(spawn_zombie())

run = True
while run:
    clock.tick(60)
    update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    if run:
        player.update()
        for zombie in zombies:
            zombie.pathfinder(player)

        if pg.sprite.spritecollideany(player, zombies):
            game_over = True
    draw(win)
pg.quit()