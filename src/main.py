from settings import *

# used to contain game assets that will be used everywhere
class Game:
    """Central game object containing essential game components"""
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.mouse = pygame.mouse
        self.font = pygame.font.Font(
            join('assets', 'fonts', 'MerriweatherSans-Medium.ttf'))
        self.dt = 0
        self.on = True

class MainMenu:
    def handle_events(self, game, state_stack):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.on = False


# the pattern:
# you have a state stack, and in it are objects that represent game states.
# for example, for the game you have the game state class and you import it here
# and here in the main menu class when the player presses the button that opens the
# game, you would append the game object to the state stack and yea
def main():
    game = Game()
    state_stack = [MainMenu()]

    while game.on:
        game.dt = game.clock.tick(FPS) / 1000

        top_state = state_stack[-1]
        top_state.handle_events(game, state_stack)
        top_state.update(game, state_stack)
        top_state.draw(game, state_stack)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
