import time

import pygame,random
from sys import exit
pygame.init()

width = 1000
height = 800
window = pygame.display.set_mode((1000,800))
window.fill("White")
pygame.display.set_caption("frogger")
clock = pygame.time.Clock()

coin_image = pygame.image.load("coinimage.png")
coin_surface = pygame.transform.scale(coin_image,(50,50))

road_image = pygame.image.load("road.png")
road_surface = pygame.transform.scale(road_image,(1000,50))

grass_image = pygame.image.load("grassimage.png")
grass_surface = pygame.transform.scale(grass_image,(1000,50))

carimage = pygame.image.load("carimage.png")
car_surface = pygame.transform.scale(carimage,(50,50))

waterimage = pygame.image.load("waterimage.png")
water_surface = pygame.transform.scale(waterimage,(1000,50))

logimage = pygame.image.load("logimage.png")
log_surface = pygame.transform.scale(logimage,(150,50))

font = pygame.font.Font(None,50)

lanes = [0,50,100,150,200,250,300,350,400,450,500,650,700,750,]
xcoords = [0,50,100,150,200,250,300,350,400,450,500,650,700,750,800,850,900,950,]


logarray =[150,400,650]
logrects = []
logspeeds = []

carrects = []
carspeeds = []
roadarray = [0,50,200,250,350,450,500,550,700,750]

def createcar(roadarray):
    for i in range(len(roadarray)):
        carposy = roadarray[i]
        carposx = random.randrange(20,width-50)
        speed = 0
        while (speed == 0) or (-5 < speed < 5):
            speed = random.randrange(-10,5)
        carrects.append(pygame.Rect(carposx,carposy,20,45))
        carspeeds.append(speed)

def createlog(logarray):
    for i in range(len(logarray)):
        logy = logarray[i]
        logx = random.randrange(145,width-145)
        logspeed = 0
        while (logspeed == 0) or (-5 < logspeed < 5):
            logspeed = random.randrange(-10,5)
        logrects.append(pygame.Rect(logx,logy,145,45))
        logspeeds.append(logspeed)


coincollected = 0
coinrects = []
def createcoin():
    coinxrandom = random.randrange(0, len(xcoords))
    coinx = xcoords[coinxrandom]
    coinyrandom = random.randrange(0, len(lanes))
    coiny = lanes[coinyrandom]
    coinrects.append(pygame.Rect(coinx, coiny, 50, 50))


for i in range(3):
    createcoin()
createcar(roadarray)
createlog(logarray)

frog_image = pygame.image.load("bluefrog.png")
frog_surface = pygame.transform.scale(frog_image,(80,50))
frogxpos = 400
frogypos = 800
frog_rect = pygame.Rect(frogxpos, frogypos, 45, 45)



running = True
grasscount = 0
xspeed = 50
yspeed = 50
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                frogxpos -= xspeed
            elif event.key == pygame.K_d:
                frogxpos += xspeed
            elif event.key == pygame.K_w:
                frogypos -= yspeed
            elif event.key == pygame.K_s:
                frogypos += yspeed

    frog_rect.x = frogxpos
    frog_rect.y = frogypos


    grasspos = [100, 300, 600]
    for i in grasspos:
        window.blit(grass_surface, (0, i))

    waterpos = [150,400,650]
    for i in waterpos:
        window.blit(water_surface, (0, i))



    roadpos = 0
    while roadpos <= 800:
        for i in grasspos:
            if roadpos == i:
                roadpos += 50
        for j in waterpos:
            if roadpos == j:
                roadpos += 50

        window.blit(road_surface, (0, roadpos))
        roadpos += 50

    for i in range(len(carrects)):
        carrects[i].x += carspeeds[i]

        if carrects[i].x <= -20 or carrects[i].x - 55 >= width:
            carspeeds[i] = carspeeds[i] * -1

        if frog_rect.colliderect(carrects[i]):
            frogxpos = carrects[i].x
            pygame.quit()
            exit()

    for i in range(len(logrects)):
        logrects[i].x += logspeeds[i]

        if logrects[i].x <= -20 or logrects[i].x + 130 >= width:
            logspeeds[i] = logspeeds[i] * -1

        if frog_rect.colliderect(logrects[i]):
            frogxpos = logrects[i].x + 40
            frogxpos = frogxpos

        if frogypos == logrects[i].y and frogxpos != logrects[i].x + 40:
            frogypos = logrects[i].y
            pygame.quit()
            exit()

    for i in range(len(coinrects)):
        if frog_rect.colliderect(coinrects[i]):
            coincollected += 1
            coinrects.pop(i)
            createcoin()

    coincollected_surface = font.render(f'{coincollected} coins collected', True, (0, 100, 0))
    window.blit(coincollected_surface,(0,105))

    for i in range(len(coinrects)):
        window.blit(coin_surface,coinrects[i].topleft)

    for i in range(len(logrects)):
        window.blit(log_surface,logrects[i].topleft)

    for i in range(len(carrects)):
        window.blit(car_surface,carrects[i].topleft)


    window.blit(frog_surface, (frogxpos, frogypos))
    pygame.display.update()
    clock.tick(60)