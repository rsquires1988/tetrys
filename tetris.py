#!/usr/bin/env python3
import pygame
import random
from typing import List

def main():
    side_len = 20
    
    # function to create a single block on its own Surface
    def create_tetronimos(x=0, y=0):
        tetronimos = {
            "straight": {
                "size": (20, 80), 
                "color": (0, 255, 255), 
                "positions": [(x,y), (x, y+side_len), (x, y+2*side_len), (x, y+3*side_len)]}, 
            "box": {
                "size": (40,40), 
                "color": (255, 255, 0),
                "positions": [(x,y), (x, y+side_len), (x+side_len, y+side_len), (x+side_len, y)]}, 
            "t": {
                "size": (60,40), 
                "color": (255, 165, 0), 
                "positions": [(x+side_len,y), (x, y+side_len), (x+side_len, y+side_len), (x+2*side_len, y+side_len)]}, 
            "left_l": {
                "size": (40, 60), 
                "color": (255, 0 , 255), 
                "positions": [(x+side_len,y), (x+side_len, y+side_len), (x+side_len, y+2*side_len), (x, y+2*side_len)]},
            "right_l": {
                "size": (40, 60), 
                "color": (255, 0, 0), 
                "positions": [(x,y), (x, y+side_len), (x, y+2*side_len), (x+side_len, y+2*side_len)]}, 
            "left_s": {
                "size": (40, 60), 
                "color": (0, 255, 0), 
                "positions": [(x+side_len,y), (x+side_len, y+side_len), (x, y+side_len), (x, y+2*side_len)]}, 
            "right_s": {
                "size": (40, 60), 
                "color": (0, 0, 255),
                "positions": [(x,y), (x, y+side_len), (x+side_len, y+side_len), (x+side_len, y+2*side_len)]}}
        
        def create_block(block_color):
            # make block surface the same size as the block itself
            block_surface = pygame.Surface((side_len,side_len))
            
            desaturation_percent = 0.25
            # give block a background color (Programmer's note: Next time, please, just hardcode them in)
            desaturated_block_color = [64 if n == 0 else int(n - (n * desaturation_percent)) for n in block_color]
            # desaturated_block_color = [min(int(n + (255 * desaturation_percent)), 255) if n < 128 
            #                            else max(int(n - (n * desaturation_percent)), 0) for n in block_color]
            # print(f'{desaturated_block_color}')
            block_surface.fill(block_color)
            
            # make the block Rect, using the color passed in from a tetronimo function
            block_rect = pygame.Rect((0,0), (side_len, side_len))
            pygame.draw.rect(block_surface, desaturated_block_color, block_rect, width=3)
            pygame.draw.rect(block_surface, (127,127,127), block_rect, width=1)
            
            return block_surface
        
        tetronimo_surfaces = []
        for tetronimo in tetronimos.values():
            tetronimo_surface = pygame.Surface(tetronimo["size"], pygame.SRCALPHA)
            # tetronimo_surface.fill((200,200,200,255))
            block_surface = create_block(tetronimo["color"])

            # draw the block Surface onto the tetronimo Surface
            for position in tetronimo["positions"]:
                tetronimo_surface.blit(block_surface, position)
                
            tetronimo_surfaces.append(tetronimo_surface)
        
        return tetronimo_surfaces
    
    def next_tetronimo(tetronimo_list: List[pygame.Surface]):
        tetronimo_choice = random.choice(tetronimo_list)
        
        return tetronimo_choice
    
    # initialize pygame
    pygame.init()

    # set the window size
    size = (200, 400)
    screen = pygame.display.set_mode(size)

    # set the title of the window
    pygame.display.set_caption("Tetris")

    # set the color of the background
    bg_color = (175, 175, 175)
    
    # create the tetronimos
    tetronimo_list = create_tetronimos()
    old_tetronimos = []
    
    # get the first tetronimo
    current_tetronimo = next_tetronimo(tetronimo_list)
    move_rect = current_tetronimo.get_rect()

    # initialize game clock
    clock = pygame.time.Clock()
    
    # determines how fast the block moves downward (once per second on first level)    
    base_interval = 1000                                # one second in milliseconds
    interval = base_interval                            # set a variable for a changeable interval
    pygame.time.set_timer(pygame.USEREVENT, interval)   # start a timer and attatch it to an event

    # start the main loop
    done = False
    while not done:
        for event in pygame.event.get():                                    # event handler
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.USEREVENT:                            # if the timer is at 0
                move_rect.y += side_len                                     # move tetronimo down one side_len
                if move_rect.bottom > screen.get_height():                  # if the tetronimo's bottom edge is lower than the play area
                    move_rect.bottom = screen.get_height()                  # move it back onto the play area
                    stay_rect = move_rect                                   # save the position it was in when it collided
                    old_tetronimos.append((current_tetronimo, stay_rect))   # and add it to a list of placed tetronimos
                    current_tetronimo = next_tetronimo(tetronimo_list)      # get the next random tetronimo
                    move_rect = current_tetronimo.get_rect()                # and its bounding rectangle
                # if move_rect.bottom > 
            elif event.type == pygame.KEYDOWN:
                # screen.fill(bg_color)
                if event.key == pygame.K_LEFT:                              # if left arrow is pressed down
                    if move_rect.left <= 0:                                 # don't let it leave the play area to the left
                        move_rect.left = 0
                    else: 
                        move_rect.x -= side_len                             # otherwise, move it one block to the left
                if event.key == pygame.K_RIGHT:                             # if right arrow is pressed down
                    if move_rect.right >= screen.get_width():               # don't let it leave the play area to the right
                        move_rect.right = screen.get_width()
                    else: 
                        move_rect.x += side_len                             # otherwise, move it one block to the right
                if event.key == pygame.K_DOWN:                              # if down arrow is pressed down
                    interval = interval // 10                               # decrease the interval between automatic tetronimo downward motions
                    pygame.time.set_timer(pygame.USEREVENT, interval)       # and reset the timer
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:                              # if down arrow is released
                    interval = base_interval                                # return "speed" to base value
                    pygame.time.set_timer(pygame.USEREVENT, interval)       # and reset the timer

        # clear the screen
        screen.fill(bg_color)
        
        # draw tetronimos
        screen.blit(current_tetronimo, move_rect)
        for old_tetronimo, stay_rect in old_tetronimos:
            screen.blit(old_tetronimo, stay_rect)
        
        # update the display
        pygame.display.flip()
        
        # cap the framerate at 60
        clock.tick(60)
        
    # close the window and quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()