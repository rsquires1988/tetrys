def tets(x=0, y=0, dim=20):
    return {
        "straight": {
            "size": (80, 80), 
            "color": (0, 255, 255), 
            "shape": [(x, y+dim), (x+dim, y+dim), (x+2*dim, y+dim), (x+3*dim, y+dim)]}, 
        "box": {
            "size": (80,60), 
            "color": (255, 255, 0),
            "shape": [(x+dim, y), (x+2*dim, y), (x+2*dim, y+dim), (x+dim, y+dim)]}, 
        "t": {
            "size": (60,60), 
            "color": (255, 165, 0), 
            "shape": [(x, y+dim), (x+dim, y), (x+dim, y+dim), (x+2*dim, y+dim)]}, 
        "left_l": {
            "size": (60, 60), 
            "color": (255, 0 , 255), 
            "shape": [(x, y), (x, y+dim), (x+dim, y+dim), (x+2*dim, y+dim)]}, 
        "right_l": {
            "size": (60, 60), 
            "color": (255, 0, 0), 
            "shape": [(x, y+dim), (x+dim, y+dim), (x+2*dim, y), (x+2*dim, y+dim)]}, 
        "left_s": {
            "size": (60, 60), 
            "color": (0, 255, 0), 
            "shape": [(x, y), (x+dim, y), (x+dim, y+dim), (x+2*dim, y+dim)]}, 
        "right_s": {
            "size": (60, 60), 
            "color": (0, 0, 255),
            "shape": [(x, y+dim), (x+dim, y+dim), (x+dim, y), (x+2*dim, y)]}
    }