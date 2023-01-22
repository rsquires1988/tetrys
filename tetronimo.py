import pygame
import random
from textwrap import dedent
from tet_data import tets
from typing import Tuple, List, Dict

# class TetSprite(pygame.sprite.Sprite):
#     def __init__(self, tet, group):
#         super(pygame.sprite.Sprite, self).__init__()
#         # self.tetronimo = tet
#         self._Sprite__g = group
#         self.rect = tet.get_rect()

placed_group = pygame.sprite.Group()
falling_group = pygame.sprite.Group()

class Tetronimo(pygame.sprite.Sprite):    
    def __init__(self, x: int, y: int, dim: int) -> type:
        super().__init__()
        falling_group.add(self)
        self.group = falling_group
        self.name = self.get_random(list(tets(x, y, dim)))
        self.size: Tuple[int] = tets(x, y, dim)[self.name]["size"]
        self.color: Tuple[int] = tets(x, y, dim)[self.name]["color"]
        self.shape: List[Tuple[int]] = tets(x, y, dim)[self.name]["shape"]
        self.image = self.get_surface(dim)
        self.mask = self.get_mask()
        self.rect = self.image.get_rect()
        self.center = self.get_center(self.name, dim)
        # self.tet_sprite = TetSprite(self.surface, group)
        # self.image = self.surface

        print(self)

    def __str__(self) -> str:
        return dedent(f'''
                Group: {self.group}
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
        
    def update(self):
        self.group.remove(self)
        placed_group.add(self)
        print(placed_group)


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
        return pygame.mask.from_surface(self.image)
    
    def get_center(self, name: str, dim: int) -> Tuple[int]:
        return (dim*2,dim) if name == "box" else self.rect.center
    
    def rotation(self, direction):
        if self.name == "box":
            # TODO: should rotate the hitbox? I guess? Still not sure why I did this beyond "that's how they do it in the real tetris"
            pass
        else:
            self.image = pygame.transform.rotate(self.image, direction)
            # self.rect = self.image.get_rect()
            
    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
    
