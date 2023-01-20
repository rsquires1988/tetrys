import pygame
import random
from textwrap import dedent
from tet_data import tets
from typing import List, Dict

class Tetronimo:    
    def __init__(self, x=0, y=0, dim=20): # -> Dict[str, Dict[str, List[pygame.Surface], Tuple(int, int), pygame.Mask]: or something
        self.name = self.get_random(list(tets()))
        self.size = tets()[self.name]["size"]
        self.color = tets()[self.name]["color"]
        self.shape = tets()[self.name]["shape"]
        self.surface = self.get_surface(square=(dim, dim))
        self.mask = self.get_mask()
        self.center = self.get_center(self.name, self.surface)
        print(self)

    def __str__(self):
        return dedent(f'''
                Name: {self.name}
                Size: {self.size}
                Color: {self.color}
                Shape: {self.shape}
                Surface: {self.surface}
                Mask: {self.mask}
                Center: {self.center}
                --------
                ''').strip()

    def get_random(self, tet_data): # Dict[str, pygame.Surface]):
        '''Picks a random tetronimo's name'''
        tetronimo_choice = random.choice(tet_data)
        return tetronimo_choice
    
    def create_block(self, block_color, square) -> pygame.Surface:
        '''Makes block surface the same size as the block itself'''
        block_surface = pygame.Surface(square)
        block_surface.fill(block_color)
        
        # get edge shadow color
        desaturation_percent = 0.25
        desaturated_block_color = [64 if n == 0 else int(n - (n * desaturation_percent)) for n in block_color]
        
        # paint the block surface, make the block Rect, and draw on the shadow and border
        block_rect = block_surface.get_rect()
        pygame.draw.rect(block_surface, desaturated_block_color, block_rect, width=3)
        pygame.draw.rect(block_surface, (127,127,127), block_rect, width=1)
        
        return block_surface
    
    def get_surface(self, square):
        tetronimo_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        # tetronimo_surface.fill((200,200,200,255))
        block_surface = self.create_block(self.color, square)
            
        # draw the block Surfaces onto the tetronimo Surface
        for placement in self.shape:
            tetronimo_surface.blit(block_surface, placement)
            
        return tetronimo_surface
        
    def get_mask(self):
        return pygame.mask.from_surface(self.surface)
    
    def get_center(self, name, surface):
        return (40,20) if name == "box" else surface.get_rect().center