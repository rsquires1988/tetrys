#!/usr/bin/env python3
import pygame
from tetronimo import Tetronimo, placed_group#, TetSprite
from typing import Dict, List

def main():
    dim = 50
    x=0
    y=0
    LEFT = 90
    RIGHT = -90
        
    # def collision(block_rects):
    #     for block_rect in block_rects:
    #         collision = block_rect.colliderect()
    #         if collision:
    #             if block_rect.colliderect().bottom:
    #                 if move_rect.bottom > screen.get_height():                  # if the tetronimo's bottom edge is lower than the play area
    #                     move_rect.bottom = screen.get_height()                  # move it back onto the play area
                        
    #                 stay_rect = move_rect                                       # save the position it was in when it collided
    #                 old_tetronimos.append((current_tetronimo[1], stay_rect))    # and add it to a list of placed tetronimos
    #                 current_tetronimo = next_tetronimo(tetronimo_dict)          # get the next random tetronimo
    #                 move_rect = current_tetronimo[1].get_rect()    
                    
    # initialize pygame
    pygame.init()

    # set the window size
    size = (10*dim, 20*dim)
    screen = pygame.display.set_mode(size)

    # set the title of the window
    pygame.display.set_caption("Tetrys")

    # set the color of the background
    bg_color = (175, 175, 175)
    screen.fill(bg_color)
    
    # # create the tetronimos
    # tetronimo_dict = create_tetronimos()
    old_tetronimos = []
    
    # falling_tetronimo = 
    falling_tet = Tetronimo(x,y,dim)
    # falling_group.add(falling_tet)
    # falling_tet = TetSprite(falling_tet, falling_tetronimo_sprite_group)

    # falling_tetronimo_sprite_group.add(falling_tet)
    # initial_rect = falling_tetronimo.surface.get_rect()
    # move_rect = initial_rect

    # # get the first tetronimo
    # outline = current_mask.outline()
    # # tet_group = pygame.sprite.Group()
    # # tet_sprite = pygame.sprite.Sprite(falling_tetronimo.surface)

    # # TODO: List of block rects that gets updated first (for collision purposes) every interval
    # # collide_rects = 

    # initialize game clock
    clock = pygame.time.Clock()
    
    # determines how fast the block moves downward (once per second on first level)    
    base_interval = 1000                                # one second in milliseconds
    interval = base_interval                            # set a variable for a changeable interval
    pygame.time.set_timer(pygame.USEREVENT, interval)   # start a timer and attatch it to an event
    
    # # screen_bottom_mask = pygame.mask.Mask((screen.get_width(), 1)) #pygame.rect.Rect((0, screen.get_height()), (screen.get_width(), -20)), fill=True)
    # # screen_bottom_mask.fill()

    # start the main loop
    done = False
    while not done:
        for event in pygame.event.get():    # event handler
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.USEREVENT:                                                # if the timer is at 0
                falling_tet.move(0, dim) # move_rect.y += dim                                                           # move tetronimo down one dim
                print(falling_tet)
                if falling_tet.rect.bottom > screen.get_height(): #current_mask.outline() not in screen:#.area():# current_mask.overlap(screen_bottom_mask, (0, screen.get_height() + 1)): #any in falling_tetronimo.mask.outline() not in screen: # any in current_mask.outline() > screen.get_height():      # if the tetronimo's bottom edge is lower than the play area
                    falling_tet.rect.bottom = screen.get_height()                                      # move it back onto the play area
                    # stay_sprite = falling_tet                                                # save the position it was in when it collided
                    falling_tet.update()
                    # old_tetronimos.append((falling_tet.image, falling_tet.rect))
                    falling_tet = Tetronimo(x,y,dim)# and add it to a list of placed tetronimos
                    # falling_tet = TetSprite(falling_tet, falling_tetronimo_sprite_group)                                         # get the next random tetronimo
                    # move_rect = falling_tetronimo.surface.get_rect()                            # and its bounding rectangle
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:                                                  # if left arrow is pressed down
                    if falling_tet.rect.left <= 0:                                                     # don't let it leave the play area to the left
                        falling_tet.rect.left = 0
                    else: 
                        falling_tet.move(-dim,0)                                              # otherwise, move it one block to the left
                if event.key == pygame.K_RIGHT:                                                 # if right arrow is pressed down
                    if falling_tet.rect.right >= screen.get_width():                                   # don't let it leave the play area to the right
                        falling_tet.rect.right = screen.get_width()
                    else: 
                        falling_tet.move(dim,0)                                              # otherwise, move it one block to the right
                if event.key == pygame.K_DOWN:                                                  # if down arrow is pressed down
                    interval = interval // 10                                                   # decrease auto-drop timing interval by a factor of 10
                    pygame.time.set_timer(pygame.USEREVENT, interval)                           # and reset the timer
                if event.key == pygame.K_d:
                    falling_tet.rotation(LEFT)
                if event.key == pygame.K_f:
                    falling_tet.rotation(RIGHT)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:                                                  # if down arrow is released
                    interval = base_interval                                                    # return "speed" to base value
                    pygame.time.set_timer(pygame.USEREVENT, interval)                           # and reset the timer

        # clear the screen
        screen.fill(bg_color)
        
        # draw tetronimos
        # ! DEBUG: Shows masks
        # outline = current_tetronimo["mask"].outline()
        # pygame.draw.polygon(falling_tetronimo.surface, (255,255,255), outline)
        screen.blit(falling_tet.image, falling_tet.rect)
        # current_tetronimo["mask"].fill()
        # screen.blit(current_tetronimo["mask"].
        
        placed_group.draw(screen)
        # for old_tetronimo, stay_rect in old_tetronimos:
        #     screen.blit(old_tetronimo, stay_rect)
        # update the display
        pygame.display.flip()
        
        # cap the framerate at 60
        clock.tick(60)
        
    # close the window and quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()