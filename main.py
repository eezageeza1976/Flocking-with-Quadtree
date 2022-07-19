import pygame as pg
import boids
import consts
from obsticle import Obsticle
from boids import Boid 
from quadtree import Point, Rectangle, Quadtree




def windowSetup():
    window = pg.display.set_mode((consts.WIN_WIDTH, consts.WIN_HEIGHT))
    window.fill(consts.BLACK)
    return window

screen = windowSetup()

def main():
    running = True
    flock_list = []
    obsticle_list = []
    root = Rectangle(Point(consts.WIN_WIDTH/2, consts.WIN_HEIGHT/2), consts.WIN_WIDTH, consts.WIN_HEIGHT)
    show_rect = False
    
    for i in range(100):
        flock_list.append(Boid())
        
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return pg.K_ESCAPE
                elif event.key == pg.K_o:  #Turns rectangle draw on/off                  
                    if not show_rect:
                        show_rect = True
                    elif show_rect:
                        show_rect = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                 obsticle_list.append(Obsticle(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]))
        
        screen.fill(consts.BLACK)
        
        qTree = Quadtree(root, screen)

        for point in flock_list:
            qTree.insert(point, show_rect)
        
        boids.update(flock_list, qTree, obsticle_list)        
        boids.draw(screen, flock_list, obsticle_list)
        
        pg.display.flip()
        del qTree

# run the App
if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()