import pygame, sys
import module
pygame.init()
screen = pygame.display.set_mode((512, 512))
pygame.display.set_caption('template')
clock = pygame.time.Clock()

class Class:
    def __init__(self):
        pass
    def loop(self):
        while True:
            break
instance = Class()

def loop():
    while True:
        break


def main():
    color = 0
    while True:
        screen.fill((color, color, color))
        color = min(255, color+1)
        loop()
        instance.loop()
        module.loop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    main()
