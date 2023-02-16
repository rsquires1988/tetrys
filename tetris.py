#!/usr/bin/env python3
import pygame
from tetronimo import Tetronimo, falling_group, placed_group

# Idea: Pinball tetris, allow partial rotations, gravity affects a tet after collision or table bump
#       Bumps left and right to settle tets
#       Bump too much and everything gets jumbled

placed_masks = []
    
def get_placed_mask(top=0, left=0):
    placed_rects = [sprite.rect for sprite in placed_group]
    placed_union = placed_rects[0].unionall(placed_rects[1:])
    placed_surface = pygame.Surface((placed_union.width, placed_union.height), pygame.SRCALPHA)
    placed_masks = [sprite.mask for sprite in placed_group]

    return placed_masks, (placed_union.left, placed_union.top), placed_union, placed_surface

def print_placed(call_loc, placed_mask, x, y, placed_union_rect, placed_surface, tet_left_corner, tet_top_corner):
    print("-----TET PLACED-----")
    print("Tets placed:", placed_group)
    print("List:", [sprite.rect for sprite in placed_group])
    print("Collision with:", call_loc)
    print("Union of placed rects:", placed_union_rect)
    print("Surface on which placed_union will be drawn:",placed_surface)
    print("Mask of surface containing all placed rects:",placed_mask)
    print("Tet top-left corner: (", tet_left_corner, ",", tet_top_corner,")")

def main():
    dim = 10
    x=0
    y=0
    LEFT = 90
    RIGHT = -90
    placed_rects = []

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

    placed_surface = []
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
                offset_x = falling_tet.rect.left
                offset_y = falling_tet.rect.top
                bits_mask = falling_tet.mask.count()

                if not bits_mask == falling_tet.mask.overlap_area(pygame.mask.from_surface(screen), (-offset_x, -offset_y)):
                    falling_tet.update(move=(0, -dim), placed=True)
                    placed_masks, pmloc, placed_rects, placed_surface = get_placed_mask()
                    call_loc = "wall"
                    print_placed(call_loc, placed_masks, pmloc[0], pmloc[1], placed_rects, placed_surface, offset_x, offset_y)
                    # screen.blit(placed_surface, (0,0))
                    falling_tet = Tetronimo(x,y,dim)
                elif placed_rects:
                    for sprite in placed_group:#for mask in placed_masks:
                        # NOTE: They're only colliding with their own sprites, not any sprite, and rotations seem to break it as well, still got some offset weirdness
                        tet_overlaps_placed = bits_mask == falling_tet.mask.overlap_area(sprite.mask, (sprite.rect.left - offset_x, sprite.rect.top - offset_y - dim))
                        if tet_overlaps_placed:
                            falling_tet.update(move=(0, -dim), placed=True)
                            placed_masks, pmloc, placed_rects, placed_surface = get_placed_mask()
                            call_loc="tet"
                            print_placed(call_loc, placed_masks, pmloc[0], pmloc[1], placed_rects, placed_surface, offset_x, offset_y)
                            falling_tet = Tetronimo(x,y,dim)
                            break
                    
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
        pygame.draw.polygon(falling_tet.image, (255,255,255), falling_tet.mask.outline())

        if placed_surface:
            for sprite in placed_group:
                pygame.draw.polygon(sprite.image, (0,0,0), sprite.mask.outline())#all_mask.outline())

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