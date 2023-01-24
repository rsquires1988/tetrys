#!/usr/bin/env python3
import pygame
from tetronimo import Tetronimo, falling_group, placed_group

# Idea: Pinball tetris, allow partial rotations, gravity affects a tet after collision or table bump
#       Bumps left and right to settle tets
#       Bump too much and everything gets jumbled

def main():
    dim = 20
    x=0
    y=0
    LEFT = 90
    RIGHT = -90

    # initialize pygame
    pygame.init()

    # set the window size
    size = (10*dim, 20*dim)
    screen = pygame.display.set_mode(size)

    # set the title of the window
    pygame.display.set_caption("Tetrys")

    # set the color of the background and fill the screen surface with it
    bg_color = (175, 175, 175)
    screen.fill(bg_color)
    
    # create a tetronimo
    falling_tet = Tetronimo(x,y,dim)

    # initialize game clock
    clock = pygame.time.Clock()
    
    # determines how fast the block moves downward (once per second on first level)    
    base_interval = 1000                                # one second in milliseconds
    interval = base_interval                            # set a variable for a changeable interval
    pygame.time.set_timer(pygame.USEREVENT, interval)   # start a timer and attatch it to an event

    offset_x = 0
    offset_y = 0
    # start the main loop
    done = False
    while not done:
        for event in pygame.event.get():    # event handler
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.USEREVENT: 
                falling_tet.update(move=(0, dim))
                print(falling_tet)
                offset_x = -falling_tet.rect.left
                offset_y = -falling_tet.rect.top
                bits_mask = falling_tet.mask.count()
                if not bits_mask == falling_tet.mask.overlap_area(pygame.mask.from_surface(screen), (offset_x, offset_y)):
                    falling_tet.update(move=(0, -dim), placed=True)
                    falling_tet = Tetronimo(x,y,dim)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    falling_tet.update(move=(-dim,0))
                    offset_x = -falling_tet.rect.left
                    offset_y = 0
                    bits_mask = falling_tet.mask.count()
                    if not bits_mask == falling_tet.mask.overlap_area(pygame.mask.from_surface(screen), (offset_x, offset_y)):
                        falling_tet.update(move=(dim,0))
                if event.key == pygame.K_RIGHT:
                    falling_tet.update(move=(dim,0))
                    offset_x = -falling_tet.rect.left
                    offset_y = 0
                    bits_mask = falling_tet.mask.count()
                    if not bits_mask == falling_tet.mask.overlap_area(pygame.mask.from_surface(screen), (offset_x, offset_y)):
                        falling_tet.update(move=(-dim,0))
                if event.key == pygame.K_DOWN: 
                    interval = interval // 10 
                    pygame.time.set_timer(pygame.USEREVENT, interval)
                if event.key == pygame.K_d:
                    falling_tet.update(rotation=LEFT)
                    # kick stuff goes here
                if event.key == pygame.K_f:
                    falling_tet.update(rotation=RIGHT)
                    # kick stuff goes here
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    interval = base_interval
                    pygame.time.set_timer(pygame.USEREVENT, interval)

        # clear the screen
        screen.fill(bg_color)
        
        # ! DEBUG: Shows masks
        # pygame.draw.polygon(falling_tet.image, (255,255,255), falling_tet.mask.outline())
        
        # draw falling and placed tetronimos
        falling_group.draw(screen)
        placed_group.draw(screen)
        pygame.display.flip()
        
        # cap the framerate at 60
        clock.tick(60)
        
    # close the window and quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()