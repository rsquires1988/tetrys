import pygame
import random
from textwrap import dedent
from tet_data import tets
from typing import Tuple, List, Dict

class Tetronimo:    
    def __init__(self, x: int=0, y: int=0, dim: int=20) -> type:
        self.name = self.get_random(list(tets(x, y, dim)))
        self.size: Tuple[int] = tets(x, y, dim)[self.name]["size"]
        self.color: Tuple[int] = tets(x, y, dim)[self.name]["color"]
        self.shape: List[Tuple[int]] = tets(x, y, dim)[self.name]["shape"]
        self.surface = self.get_surface(dim)
        self.mask = self.get_mask()
        self.center = self.get_center(self.name, self.surface, dim)
        print(self)

    def __str__(self) -> str:
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

    def get_random(self, tets: List[int]) -> str:
        '''Picks a random tetronimo's name'''
        tetronimo_choice = random.choice(tets)
        return tetronimo_choice
    
    def create_block(self, block_color: Tuple[int], dim: int) -> pygame.Surface:
        '''Makes block surface the same size as the block itself'''
        square = (dim, dim)
        block_surface = pygame.Surface(square)
        block_surface.fill(block_color)
        
        # get edge shadow color
        desaturation_percent = 0.25
        desaturated_block_color = [64 if n == 0 else int(n - (n * desaturation_percent)) for n in block_color]
        
        # paint the block surface, make the block Rect, and draw on the shadow and border
        block_rect = block_surface.get_rect()
        pygame.draw.rect(block_surface, desaturated_block_color, block_rect, width=dim//6)
        pygame.draw.rect(block_surface, (127,127,127), block_rect, width=1)
        
        return block_surface
    
    def get_surface(self, dim: int) -> pygame.Surface:
        tetronimo_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        # tetronimo_surface.fill((200,200,200,255))
        block_surface = self.create_block(self.color, dim)
            
        # draw the block Surfaces onto the tetronimo Surface
        for placement in self.shape:
            tetronimo_surface.blit(block_surface, placement)
            
        return tetronimo_surface
        
    def get_mask(self) -> pygame.Mask:
        return pygame.mask.from_surface(self.surface)
    
    def get_center(self, name: str, surface: pygame.Surface, dim: int) -> Tuple[int]:
        return (dim*2,dim) if name == "box" else surface.get_rect().center
    
# class TetSprite(pygame.sprite.Sprite):
#     def __init__(self, tetronimo):
#         super().__init__()
#         self.image = tetronimo
#         self.rect = self.image.get_rect()