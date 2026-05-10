class State():
    def __init__(self, game):
    
        self.game = game
        self.prev_state = None

    def update(self, delta_time, actions):
        pass

    def render(self, screen):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, delta_time, actions):
        self.game.reset_keys()

    def render(self, display):
        display.fill(255, 255, 255)
        self.game.draw_text(display, "Game States Demo", (0,0,0), self.game.GAME_W/2, self.game.GAME_H/2)