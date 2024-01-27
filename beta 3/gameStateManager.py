class GameStateManager:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def add_state(self, state_name, state):
        self.states[state_name] = state

    def switch_state(self, new_state_name):
        if new_state_name in self.states:
            self.current_state = self.states[new_state_name]
        else:
            print(f"State \'{new_state_name}\' does not exist.")
        
    def get_state(self, state):
        if state in self.states:
            return self.states[state]
        else:
            print(f'State \'{state}\' does not exist')

    def update(self):
        if self.current_state:
            self.current_state.update()

    def handle_event(self, event):
        if self.current_state:
            self.current_state.handle_event(event)