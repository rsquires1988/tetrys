from typing import Dict

def tets(x: int, y: int, dim: int) -> Dict:
    return {
        "straight": {
            "size": (dim*4, dim*4), 
            "color": (0, 255, 255), 
            "shape": [(x, y+dim), (x+dim, y+dim), (x+2*dim, y+dim), (x+3*dim, y+dim)]}, 
        "box": {
            "size": (dim*4,dim*3), 
            "color": (255, 255, 0),
            "shape": [(x+dim, y), (x+2*dim, y), (x+2*dim, y+dim), (x+dim, y+dim)]}, 
        "t": {
            "size": (dim*3,dim*3), 
            "color": (255, 165, 0), 
            "shape": [(x, y+dim), (x+dim, y), (x+dim, y+dim), (x+2*dim, y+dim)]}, 
        "left_l": {
            "size": (dim*3,dim*3), 
            "color": (255, 0 , 255), 
            "shape": [(x, y), (x, y+dim), (x+dim, y+dim), (x+2*dim, y+dim)]}, 
        "right_l": {
            "size": (dim*3,dim*3), 
            "color": (255, 0, 0), 
            "shape": [(x, y+dim), (x+dim, y+dim), (x+2*dim, y), (x+2*dim, y+dim)]}, 
        "left_s": {
            "size": (dim*3,dim*3), 
            "color": (0, 255, 0), 
            "shape": [(x, y), (x+dim, y), (x+dim, y+dim), (x+2*dim, y+dim)]}, 
        "right_s": {
            "size": (dim*3,dim*3), 
            "color": (0, 0, 255),
            "shape": [(x, y+dim), (x+dim, y+dim), (x+dim, y), (x+2*dim, y)]}
    }