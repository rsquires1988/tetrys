#!/usr/bin/env python3
import pygame
from tetronimo import Tetronimo, falling_group, placed_group
from typing import Dict, List

def main():
    dim = 20
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
    # boundaries_mask = pygame.mask.Mask((screen.get_width(), screen.get_height()))
    # boundaries_mask.draw(pygame.draw.rect(screen), (screen.get_height() - dim, screen.get_width() + dim))
    
    # # create the tetronimos
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
                # here there be monsters
                # wait I GET IT
                # it's necessary to align the mask with the screen surface because the overlap_area 
                # method compares the bits of the two masks, and if the two masks are not aligned, 
                # the bits won't match up and the comparison will return zero.
                # The offset_x and offset_y variables are used to specify the position of the 
                # falling_tet's mask relative to the screen surface, so that the two masks are aligned 
                # and the comparison can be made correctly.
                falling_tet.move(0, dim) 
                print(falling_tet)
                offset_x = -falling_tet.rect.left
                offset_y = -falling_tet.rect.top
                bits_mask = falling_tet.mask.count()
                # sprite_masks = [sprite.mask for sprite in placed_group.sprites()]
                # def get_mask_rect(mask, top=0, left=0):
                #     rect_list = mask.get_bounding_rects()
                #     mask_rect_union = rect_list[0].unionall(rect_list)
                #     mask_rect_union.move_ip(top, left)
                #     return mask_rect_union

                if not bits_mask == falling_tet.mask.overlap_area(pygame.mask.from_surface(screen), (offset_x, offset_y)):
                    falling_tet.move(0,-dim)
                    falling_tet.update(placed=True)
                    falling_tet = Tetronimo(x,y,dim)
                # for mask in sprite_masks:
                #     mask_rect_union = get_mask_rect(mask)
                #     offset_x = -mask_rect_union.left
                #     offset_y = -mask_rect_union.top
                #     if not bits_mask == falling_tet.mask.overlap_area(mask, (offset_x, offset_y)):
                #         falling_tet.move(0,-dim)
                #         falling_tet.update(placed=True)
                #         falling_tet = Tetronimo(x,y,dim)
                #     else:
                #         pass
                
                # if pygame.sprite.spritecollide(falling_tet, placed_group, False):
                #     print("collision")
                
                # for sprite in placed_group:
                #     if falling_tet.mask.overlap_mask(sprite.mask, (offset_x, offset_y)):
                #         print("collision")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # here too
                    falling_tet.move(-dim,0)
                    offset_x = -falling_tet.rect.left
                    offset_y = 0
                    bits_mask = falling_tet.mask.count()
                    if not bits_mask == falling_tet.mask.overlap_area(pygame.mask.from_surface(screen), (offset_x, offset_y)):
                        falling_tet.move(dim,0)
                        falling_tet.update()
                if event.key == pygame.K_RIGHT:
                    # also here
                    falling_tet.move(dim,0)
                    offset_x = -falling_tet.rect.left
                    offset_y = 0
                    bits_mask = falling_tet.mask.count()
                    if not bits_mask == falling_tet.mask.overlap_area(pygame.mask.from_surface(screen), (offset_x, offset_y)):
                        falling_tet.move(-dim,0)
                        falling_tet.update()
                if event.key == pygame.K_DOWN: 
                    interval = interval // 10 
                    pygame.time.set_timer(pygame.USEREVENT, interval)
                if event.key == pygame.K_d:
                    falling_tet.update(rotation=LEFT)
                    # kick stuff goes here
                    # falling_tet.rotate(LEFT)
                if event.key == pygame.K_f:
                    falling_tet.update(rotation=RIGHT)
                    # kick stuff goes here
                    # falling_tet.rotate(RIGHT)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    interval = base_interval
                    pygame.time.set_timer(pygame.USEREVENT, interval)

        # clear the screen
        screen.fill(bg_color)
        
        # draw tetronimos
        # ! DEBUG: Shows masks
        # outline = falling_tet.mask.outline()
        # pygame.draw.polygon(falling_tet.image, (255,255,255), falling_tet.mask.outline())
        falling_group.draw(screen)
        # screen.blit(falling_tet.image, falling_tet.rect)
        # current_tetronimo["mask"].fill()
        # screen.blit(current_tetronimo["mask"].
        
        placed_group.draw(screen)
        pygame.display.flip()
        
        # cap the framerate at 60
        clock.tick(60)
        
    # close the window and quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()