#!/usr/bin/env python3
import pygame
from tetronimo import Tetronimo, falling_group, placed_group, placed_blocks

# placed_masks = []

# Checks for collision between falling_tet and the edges of the screen or any tetronimos in the placed_group
def collision(screen, falling_tet):
    return falling_tet.count != falling_tet.mask.overlap_area(pygame.mask.from_surface(screen), (-falling_tet.rect.left, -falling_tet.rect.top)) or \
        pygame.sprite.spritecollide(falling_tet, placed_group, False, pygame.sprite.collide_mask)

# def get_placed_mask(top=0, left=0):
#     # BUG: placed_rects is required to prevent an exception on first placement, and therefore must be updated whenever something is placed
#     # FIXME: probably just check if placed_group, if not, updating this in the "if placed" update() call should help, + clean the code up
#     # NOTE: The rest is just being printed for debugging so should be safe to relocate and print using Tetronimo's __str__(), along with print_placed()
#     placed_rects = [sprite.rect for sprite in placed_group]
#     placed_union = placed_rects[0].unionall(placed_rects[1:])
#     placed_surface = pygame.Surface((placed_union.width, placed_union.height), pygame.SRCALPHA)
#     #placed_masks = [sprite.mask for sprite in placed_group]

#     return (placed_union.left, placed_union.top), placed_union, placed_surface#, placed_masks

# def print_placed(call_loc, placed_mask, x, y, placed_union_rect, placed_surface, tet_left_corner, tet_top_corner):
#     print("-----TET PLACED-----")
#     print("Tets placed:", placed_group)
#     print("List:", [sprite.rect for sprite in placed_group])
#     print("Collision with:", call_loc)
#     print("Union of placed rects:", placed_union_rect)
#     print("Surface on which placed_union will be drawn:",placed_surface)
#     print("Mask of surface containing all placed rects:",placed_mask)
#     print("Tet top-left corner: (", tet_left_corner, ",", tet_top_corner,")")

def main():
    dim = 30
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
    
    rows = []
    for i in range(dim*20-dim, 0, -dim):
        rows.append(screen.subsurface(0, i, dim * 10, dim))
        
    print(rows)
    # start the main loop
    running = True
    while running:
        # ? Seems to slow down the game (more calculations happening), might be necessary in the future
        # ? event = pygame.event.poll()
        for event in pygame.event.get():    # event handler
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT: 
                falling_tet.update(move=(0, dim))
                if collision(screen, falling_tet):
                    falling_tet.update(move=(0, -dim), placed=True)
                    falling_tet = Tetronimo(x,y,dim)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    falling_tet.update(move=(-dim,0))
                    if collision(screen, falling_tet):
                        falling_tet.update(move=(dim,0))
                if event.key == pygame.K_RIGHT:
                    falling_tet.update(move=(dim,0))
                    if collision(screen, falling_tet):
                        falling_tet.update(move=(-dim,0))
                if event.key == pygame.K_DOWN:
                    falling_tet.update(move=(0,dim))
                    interval = interval // 10 
                    pygame.time.set_timer(pygame.USEREVENT, interval)
                    if collision(screen, falling_tet):
                        falling_tet.update(move=(0,-dim), placed=True)
                        falling_tet = Tetronimo(x,y,dim)
                if event.key == pygame.K_s:
                    falling_tet.update(rotation=LEFT)
                    # kick stuff goes here
                if event.key == pygame.K_d:
                    falling_tet.update(rotation=RIGHT)
                    # kick stuff goes here
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    interval = base_interval
                    pygame.time.set_timer(pygame.USEREVENT, interval)

        # for i, row in enumerate(rows, 0):
        #     ? if block count * 10 != row.count
        #         print(f"Row {i} has 10 blocks")
        # clear the screen
        screen.fill(bg_color)
        
        # ! DEBUG: Shows masks
        # pygame.draw.polygon(falling_tet.image, (255,255,255), falling_tet.mask.outline())

        # if placed_group:
        #     for sprite in placed_group:
        #         pygame.draw.polygon(sprite.image, (0,0,0), sprite.mask.outline())

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