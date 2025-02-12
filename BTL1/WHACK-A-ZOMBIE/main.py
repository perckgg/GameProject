from GameDesign import *


if __name__ == "__main__":
    
    #initialize pygame
    pg.init()

    #create screen
    pg.display.set_caption("Whacking zombies")

    clock = pg.time.Clock()  

    #Game loop 
    running = True
    game = Game()
    while running:
        Game.system_events = pg.event.get()

        if(game.update() == pg.QUIT):
            break

        game.render()
        game.clean()
        pg.display.flip()
        clock.tick(60)
        
pg.quit()

