#!/usr/bin/env python3
import pygame
import random
from typing import List

def main():
    side_len = 20
    
    # function to create a single block on its own Surface
    def create_block(block_color):
        # make block surface the same size as the block itself
        block_surface = pygame.Surface((side_len,side_len))
        
        # give block a background color
        block_surface.fill((0,0,0))
        
        # make the block Rect, using the color passed in from a tetronimo function
        block_rect = pygame.Rect((0,0), (side_len, side_len))
        pygame.draw.rect(block_surface, block_color, block_rect, width=2)
        
        return block_surface
    
    # function to create a right facing "L" tetronimo
    def create_right_l_tetronimo(x=0,y=0):
        block_color = (255, 0, 0)   # red
        
        # coordinates used to position the indivdual blocks to make the shape of the full tetronimo
        block_positions = [(x,y), (x, y+side_len), (x, y+2*side_len), (x+side_len, y+2*side_len)]
        
        # make surface to combine all blocks into one asset, and give it a transparent background
        tetronimo_surface = pygame.Surface((40, 60), pygame.SRCALPHA)
        tetronimo_surface.fill((200,200,200,255)) # DEBUG: shows rect of tetronimo surface when last int is non-zero
        
        # make each block in the tetronimo
        for block_position in block_positions:
            block_surface = create_block(block_color)
            
            # draw the block Surface onto the tetronimo Surface
            tetronimo_surface.blit(block_surface, block_position)
            
        return tetronimo_surface
        
    # function to create a box-shaped tetronimo
    def create_box_tetronimo(x=0,y=0):
        block_color = (255, 255, 0) # yellow
        block_positions = [(x,y), (x, y+side_len), (x+side_len, y+side_len), (x+side_len, y)]
        
        tetronimo_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        
        for block_position in block_positions:
            block_surface = create_block(block_color)
            tetronimo_surface.blit(block_surface, block_position)
            
        return tetronimo_surface
    
    # function to create a left facing "S" tetronimo
    def create_left_s_tetronimo(x=0,y=0):
        block_color = (0, 255, 0)   # green
        block_positions = [(x+side_len,y), (x+side_len, y+side_len), (x, y+side_len), (x, y+2*side_len)]
        
        tetronimo_surface = pygame.Surface((40, 60), pygame.SRCALPHA)
        
        for block_position in block_positions:
            block_surface = create_block(block_color)
            tetronimo_surface.blit(block_surface, block_position)
            
        return tetronimo_surface
        
    # function to create a right facing "S" tetronimo
    def create_right_s_tetronimo(x=0,y=0):
        block_color = (0, 0, 255)   # blue
        block_positions = [(x,y), (x, y+side_len), (x+side_len, y+side_len), (x+side_len, y+2*side_len)]
        
        tetronimo_surface = pygame.Surface((40, 60), pygame.SRCALPHA)
        
        for block_position in block_positions:
            block_surface = create_block(block_color)
            tetronimo_surface.blit(block_surface, block_position)
            
        return tetronimo_surface
    
    # function to create a straight tetronimo
    def create_straight_tetronimo(x=0,y=0):
        block_color = (0, 255, 255) # cyan
        block_positions = [(x,y), (x, y+side_len), (x, y+2*side_len), (x, y+3*side_len)]
        
        tetronimo_surface = pygame.Surface((20, 80), pygame.SRCALPHA)
        
        for block_position in block_positions:
            block_surface = create_block(block_color)
            tetronimo_surface.blit(block_surface, block_position)
            
        return tetronimo_surface
            
    # function to create a left facing "L" tetronimo
    def create_left_l_tetronimo(x=0,y=0):
        block_color = (255, 0, 255) # violet
        block_positions = [(x+side_len,y), (x+side_len, y+side_len), (x+side_len, y+2*side_len), (x, y+2*side_len)]
        
        tetronimo_surface = pygame.Surface((40, 60), pygame.SRCALPHA)
        
        for block_position in block_positions:
            block_surface = create_block(block_color)
            tetronimo_surface.blit(block_surface, block_position)
            
        return tetronimo_surface
    
    # function to create a "T" tetronimo
    def create_t_tetronimo(x=0,y=0):
        block_color = (255, 165, 0) # orange
        block_positions = [(x+side_len,y), (x, y+side_len), (x+side_len, y+side_len), (x+2*side_len, y+side_len)]
    
        tetronimo_surface = pygame.Surface((60, 40), pygame.SRCALPHA)
        
        for block_position in block_positions:
            block_surface = create_block(block_color)
            tetronimo_surface.blit(block_surface, block_position)
            
        return tetronimo_surface
    
    def next_tetronimo(tetronimo_list: List[pygame.Surface]):
        tetronimo_choice = random.choice(tetronimo_list)
        
        return tetronimo_choice
        # draw tetronimos
        
    
    # initialize pygame
    pygame.init()

    # set the window size
    size = (200, 400)
    screen = pygame.display.set_mode(size)

    # set the title of the window
    pygame.display.set_caption("Tetris")

    # set the color of the background
    bg_color = (100, 100, 100)
    
    right_l_tetronimo = create_right_l_tetronimo()
    box_tetronimo = create_box_tetronimo()
    left_l_tetronimo = create_left_l_tetronimo()
    right_s_tetronimo = create_right_s_tetronimo()
    straight_tetronimo = create_straight_tetronimo()
    left_s_tetronimo = create_left_s_tetronimo()
    t_tetronimo = create_t_tetronimo()
    
    # tetronimo_list = [create_right_l_tetronimo(), create_box_tetronimo(), create_left_l_tetronimo(),
    #                   create_right_s_tetronimo(), create_straight_tetronimo(),
    #                   create_left_s_tetronimo(), create_t_tetronimo()]
    tetronimo_list = [right_l_tetronimo, box_tetronimo, left_l_tetronimo, right_s_tetronimo,
                      straight_tetronimo, left_s_tetronimo, t_tetronimo]
    
    current_tetronimo = next_tetronimo(tetronimo_list)
    move_rect = current_tetronimo.get_rect()
    
    # tetronimo_list.append(create_right_l_tetronimo())
    # box_tetronimo = create_box_tetronimo()
    # create_left
    # screen.blit(right_l_tetronimo, move_rect)
    # # screen.blit(create_right_l_tetronimo(), (40, 40))
    # screen.blit(create_box_tetronimo(), (80, 40))
    # screen.blit(create_left_s_tetronimo(), (120, 40))
    # screen.blit(create_right_s_tetronimo(), (40, 120))
    # screen.blit(create_straight_tetronimo(), (80, 120))
    # screen.blit(create_left_l_tetronimo(), (120, 120))
    # screen.blit(create_t_tetronimo(), (80, 200))
    # move_rect = right_l_tetronimo.get_rect()
    
    # initialize game clock
    clock = pygame.time.Clock()
    
    # DEBUG:
    # frame_count = 0
    # start_time = time.time()
    
    # determines how fast the block moves downward (once per second)

    # speed = 1
    
    base_interval = 1000
    interval = base_interval # milliseconds
    # remaining_time = interval
    pygame.time.set_timer(pygame.USEREVENT, interval)

    # start the main loop
    done = False
    while not done:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.USEREVENT:    # timer is at 0
                # DEBUG:
                # if interval < 0:
                #     pygame.time.set_timer(pygame.USEREVENT, interval)
                move_rect.y += side_len             # move tetronimo down one side_len
                if move_rect.bottom > screen.get_height():
                    stay_rect=move_rect
                    screen.blit(current_tetronimo, stay_rect)
                    current_tetronimo = next_tetronimo(tetronimo_list)
                    move_rect = current_tetronimo.get_rect()
            elif event.type == pygame.KEYDOWN:
                # screen.fill(bg_color)
                if event.key == pygame.K_LEFT:
                    move_rect.x -= side_len
                if event.key == pygame.K_RIGHT:
                    move_rect.x += side_len
                if event.key == pygame.K_DOWN:
                    interval = interval // 10       # divide length of interval by 10, thereby increasing how fast the tetronimo drops
                    pygame.time.set_timer(pygame.USEREVENT, interval)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    interval = base_interval        # return "speed" to standard
                    pygame.time.set_timer(pygame.USEREVENT, interval)

        # clear the screen
        screen.fill(bg_color)
        
        
        # draw tetronimos
        screen.blit(current_tetronimo, move_rect)
        
        # update the display
        pygame.display.flip()
        
        # DEBUG:
        # frame_count += 1
        # elapsed_time = time.time() - start_time
        #
        # if elapsed_time >= 1:
        #     frame_rate = frame_count / elapsed_time
        #     print(f"Frame rate: {frame_rate:.2f} fps")
        #     frame_count = 0
        #     start_time = time.time()
        

        # DEBUG: 
        # if interval != 1000:
        #     interval = 1000
        #     pygame.time.set_timer(pygame.USEREVENT, interval)
        
        # cap framerate to limit speed that the player can move side to side
        clock.tick(60)

    # close the window and quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()