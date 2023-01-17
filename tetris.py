#!/usr/bin/env python3
import pygame
import random
from typing import Dict, List

def main():
    dim = 20
    square = (dim, dim)
    centers = []
    LEFT = 90
    RIGHT = -90
               
    # function to create a single block on its own Surface
    def create_tetronimos(x=0, y=0):# -> Dict[str, Dict[str, List[pygame.Surface], Tuple(int, int), pygame.Mask]: or something
        tetronimos = {
            "straight": {
                "size": (80, 80), 
                "color": (0, 255, 255), 
                "placements": [(x, y+dim), (x+dim, y+dim), (x+2*dim, y+dim), (x+3*dim, y+dim)]}, 
            "box": {
                "size": (80,60), 
                "color": (255, 255, 0),
                "placements": [(x+dim, y), (x+2*dim, y), (x+2*dim, y+dim), (x+dim, y+dim)]}, 
            "t": {
                "size": (60,60), 
                "color": (255, 165, 0), 
                "placements": [(x, y+dim), (x+dim, y), (x+dim, y+dim), (x+2*dim, y+dim)]}, 
            "left_l": {
                "size": (60, 60), 
                "color": (255, 0 , 255), 
                "placements": [(x, y), (x, y+dim), (x+dim, y+dim), (x+2*dim, y+dim)]}, 
            "right_l": {
                "size": (60, 60), 
                "color": (255, 0, 0), 
                "placements": [(x, y+dim), (x+dim, y+dim), (x+2*dim, y), (x+2*dim, y+dim)]}, 
            "left_s": {
                "size": (60, 60), 
                "color": (0, 255, 0), 
                "placements": [(x, y), (x+dim, y), (x+dim, y+dim), (x+2*dim, y+dim)]}, 
            "right_s": {
                "size": (60, 60), 
                "color": (0, 0, 255),
                "placements": [(x, y+dim), (x+dim, y+dim), (x+dim, y), (x+2*dim, y)]}}
        
        def create_block(block_color) -> pygame.Surface:
            # make block surface the same size as the block itself
            block_surface = pygame.Surface(square)
            
            desaturation_percent = 0.25
            
            # get edge shadow color 
            desaturated_block_color = [64 if n == 0 else int(n - (n * desaturation_percent)) 
                                       for n in block_color]

            # paint the block surface
            block_surface.fill(block_color)
            
            # make the block Rect, and draw on the shadow and border
            # block_rect = pygame.Rect((0,0), square)
            block_rect = block_surface.get_rect()
            pygame.draw.rect(block_surface, desaturated_block_color, block_rect, width=3)
            pygame.draw.rect(block_surface, (127,127,127), block_rect, width=1)
            
            return block_surface
        
        def get_centers(tet_types: List[str], tet_surfaces: List[pygame.Surface]):
            # dicts the name of the tet and the center of its bounding rect. If box, set center to (40,20).
            return [(40,20) if tet_type == "box" else surf.get_rect().center 
                                for tet_type, surf in zip(tet_types, tet_surfaces)]
                    # #{tet_type: tet_surface for tet_type, tet_surface in 
                    #     zip([tet_type for tet_type in tet_types], 
                    #         [(40,20) if tet_type == "box" else surf.get_rect().center 
                    #             for tet_type, surf in zip(tet_types, tet_surfaces)])}
        
        tetronimo_surfaces = []
        collision_masks = []
        for tet_data in tetronimos.values():
            tetronimo_surface = pygame.Surface(tet_data["size"], pygame.SRCALPHA)
            # tetronimo_surface.fill((200,200,200,0))
            block_surface = create_block(tet_data["color"])
            
            # draw the block Surface onto the tetronimo Surface
            # block_rects = []
            for placement in tet_data["placements"]:
                # block_rect = block_surface.get_rect()
                # block_rects.append(block_rect)
                tetronimo_surface.blit(block_surface, placement)
            
            # block_rects.append(tet_data["placements"])
            # block_rects = {k:tetronimos[k]["placements"] for k in tetronimos.keys()}
                
            tetronimo_surfaces.append(tetronimo_surface)
            collision_masks.append(pygame.mask.from_surface(tetronimo_surface))
            
        centers = get_centers(tetronimos.keys(), tetronimo_surfaces)
        
        tet_obj_list = zip(tetronimo_surfaces, centers, collision_masks)
        tet_objs = {}
        
        # tet_objs = {tetronimos.keys(): {"surface": surf, "center": center, "mask": mask for surf, center, mask in zip(tetronimo_surfaces, centers, collision_masks)}}
        # tetronimo_surfaces = {name: surf for name, surf in zip(tetronimos.keys(), tetronimo_surfaces)}
        
        for name, tetronimo_surface, cent, mask in zip(tetronimos.keys(), tetronimo_surfaces, centers, collision_masks):
            tet_objs[name] = {"surface": tetronimo_surface, "center": cent, "mask": mask}
        print(tet_objs)
        # collision_masks = [pygame.mask.from_surface(tetronimo_surface) for tetronimo_surface in tetronimo_surfaces.values()]
        return tet_objs #tetronimo_surfaces, centers, collision_masks
    
    def next_tetronimo(tetronimo_dict): # Dict[str, pygame.Surface]):
        tetronimo_choice = random.choice(list(tetronimo_dict.items()))
                                         #(tetronimo_dict.items()))
        print(tetronimo_choice)             
        
        
        return tetronimo_choice#, tetronimo_dict[tetronimo_choice]
    
    def rotation(name, tetronimo, direction):
        # name = tetronimo[0]
        if name == "box":
            # TODO: should rotate the hitbox? I guess? Still not sure why I did this beyond "that's how they do it in the real tetris"
            return name, tetronimo
        else:
            rotated_surf = pygame.transform.rotate(tetronimo, direction)
            
            return rotated_surf
        
    def collision(block_rects):
        for block_rect in block_rects:
            collision = block_rect.colliderect()
            if collision:
                if block_rect.colliderect().bottom:
                    if move_rect.bottom > screen.get_height():                  # if the tetronimo's bottom edge is lower than the play area
                        move_rect.bottom = screen.get_height()                  # move it back onto the play area
                        
                    stay_rect = move_rect                                   # save the position it was in when it collided
                    old_tetronimos.append((current_tetronimo[1], stay_rect))   # and add it to a list of placed tetronimos
                    current_tetronimo = next_tetronimo(tetronimo_dict)      # get the next random tetronimo
                    move_rect = current_tetronimo[1].get_rect()    
                    
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
    tetronimo_dict = create_tetronimos()
    old_tetronimos = []

    # get the first tetronimo
    name, current_tetronimo = next_tetronimo(tetronimo_dict)
    current_mask = current_tetronimo["mask"]
    print(current_tetronimo)
    initial_rect = current_tetronimo["surface"].get_rect()
    move_rect = initial_rect
    # TODO: List of block rects that gets updated first (for collision purposes) every interval
    # collide_rects = 

    # initialize game clock
    clock = pygame.time.Clock()
    
    # determines how fast the block moves downward (once per second on first level)    
    base_interval = 1000                                # one second in milliseconds
    interval = base_interval                            # set a variable for a changeable interval
    pygame.time.set_timer(pygame.USEREVENT, interval)   # start a timer and attatch it to an event
    
    screen_bottom_mask = pygame.mask.Mask((screen.get_width(), 1))#pygame.rect.Rect((0, screen.get_height()), (screen.get_width(), -20)), fill=True)
    # screen_bottom_mask.fill()

    # start the main loop
    done = False
    while not done:
        for event in pygame.event.get():                                    # event handler
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.USEREVENT:                            # if the timer is at 0
                move_rect.y += dim                                     # move tetronimo down one dim
                if current_mask.overlap(screen_bottom_mask, (0, screen.get_height() + 1)):                  # if the tetronimo's bottom edge is lower than the play area
                    move_rect.bottom = screen.get_height()                  # move it back onto the play area
                    stay_rect = move_rect                                   # save the position it was in when it collided
                    old_tetronimos.append((current_tetronimo["surface"], stay_rect))   # and add it to a list of placed tetronimos
                    name, current_tetronimo = next_tetronimo(tetronimo_dict)      # get the next random tetronimo
                    move_rect = current_tetronimo["surface"].get_rect()                # and its bounding rectangle
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:                              # if left arrow is pressed down
                    if move_rect.left <= 0:                                 # don't let it leave the play area to the left
                        move_rect.left = 0
                    else: 
                        move_rect.x -= dim                             # otherwise, move it one block to the left
                if event.key == pygame.K_RIGHT:                             # if right arrow is pressed down
                    if move_rect.right >= screen.get_width():               # don't let it leave the play area to the right
                        move_rect.right = screen.get_width()
                    else: 
                        move_rect.x += dim                             # otherwise, move it one block to the right
                if event.key == pygame.K_DOWN:                              # if down arrow is pressed down
                    interval = interval // 10                               # decrease the interval between automatic tetronimo downward motions
                    pygame.time.set_timer(pygame.USEREVENT, interval)       # and reset the timer
                if event.key == pygame.K_d:
                    current_tetronimo["surface"] = rotation(name, current_tetronimo["surface"], LEFT)
                if event.key == pygame.K_f:
                    current_tetronimo["surface"] = rotation(name, current_tetronimo["surface"], RIGHT)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:                              # if down arrow is released
                    interval = base_interval                                # return "speed" to base value
                    pygame.time.set_timer(pygame.USEREVENT, interval)       # and reset the timer

        # clear the screen
        screen.fill(bg_color)
        
        # draw tetronimos
        # ! DEBUG: Shows masks
        # outline = current_tetronimo["mask"].outline()
        # pygame.draw.polygon(current_tetronimo["surface"], (255,255,255), outline)
        screen.blit(current_tetronimo["surface"], move_rect)
        # current_tetronimo["mask"].fill()

        # screen.blit(current_tetronimo["mask"].
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