import pygame
import random
from textwrap import dedent
from tet_data import tets
from typing import Tuple, List

placed_group = pygame.sprite.Group()
placed_blocks = pygame.sprite.Group()
falling_group = pygame.sprite.Group()

class Block(pygame.sprite.Sprite):
    def __init__(self, color, dim):
        super().__init__()
        self.square = (dim, dim)
        self.image, self.rect = self.create_block(color, dim)
        # self.image.fill(color)
        
    def create_block(self, color: Tuple[int], dim) -> pygame.Surface:
        '''Makes block surface the same size as the block itself'''
        block_surface = pygame.Surface(self.square)
        block_surface.fill(color)
        
        # get edge shadow color
        desaturation_percent = 0.25
        desaturated_color = [64 if n == 0 else int(n - (n * desaturation_percent)) for n in color]
        
        # paint the block surface, make the block Rect, and draw on the shadow and border
        block_rect = block_surface.get_rect()
        pygame.draw.rect(block_surface, desaturated_color, block_rect, width=dim//6)
        pygame.draw.rect(block_surface, (127,127,127), block_rect, width=1)
        
        return block_surface, block_rect
        
class Tetronimo(pygame.sprite.Sprite):#pygame.sprite.Group):    
    def __init__(self, x: int, y: int, dim: int) -> type:
        super().__init__()
        falling_group.add(self)
        self.dim = dim
        self.name = self.get_random(list(tets(x, y, self.dim)))
        self.size: Tuple[int] = tets(x, y, self.dim)[self.name]["size"]
        self.color: Tuple[int] = tets(x, y, self.dim)[self.name]["color"]
        self.shape: List[Tuple[int]] = tets(x, y, self.dim)[self.name]["shape"]
        self.blocks = self.get_blocks()
        self.image = self.get_surface()
        self.mask = self.get_mask()
        self.rect = self.image.get_rect()
        self.center = self.get_center(self.name)
        self.count = self.mask.count()

    def __str__(self) -> str:
        return dedent(f'''
                Dim: {self.dim}
                Name: {self.name}
                Size: {self.size}
                Color: {self.color}
                Shape: {self.shape}
                Image: {self.image}
                Mask: {self.mask}
                Rect: {self.rect}
                Center: {self.center}
                --------
                ''').strip()
        
    def update(self, move: Tuple[int]=(0,0), placed: bool=False, rotation: int=0) -> Tuple[int]:
        '''Catch-all Tetronimo updater.'''
        if move[0] or move[1]:
            self.rect.x += move[0]
            self.rect.y += move[1]
        if placed:
            falling_group.remove(self)
            placed_group.add(self)
            placed_blocks.add(self.blocks)
            self.mask = self.get_mask()
        if rotation:
            if self.name == "box":
                pass
            else:
                self.image = pygame.transform.rotate(self.image, rotation)
            self.mask = self.get_mask()

        location = self.rect.x, self.rect.y

        return location

    def get_random(self, tets: List[int]) -> str:
        '''Picks a random tetronimo's name'''
        tetronimo_choice = random.choice(tets)
        return tetronimo_choice
    
    def get_blocks(self):
        blocks = []
        for position in self.shape:
            blocks.append(Block(self.color, self.dim))
            blocks[-1].rect.topleft = position
            
        return blocks
    
    def get_surface(self) -> pygame.Surface:
        tetronimo_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        # ! DEBUG: Shows rotation boxes 
        # tetronimo_surface.fill((255,255,255,127))
            
        # draw the block Surfaces onto the tetronimo Surface
        for block in self.blocks:
            tetronimo_surface.blit(block.image, block.rect.topleft)
            
        return tetronimo_surface
        
    def get_mask(self) -> pygame.Mask:
        return pygame.mask.from_surface(self.image)
    
    def get_center(self, name: str) -> Tuple[int]:
        return (self.dim*2, self.dim) if name == "box" else self.rect.center