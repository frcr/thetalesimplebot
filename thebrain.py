import pinky

class TheBrain:
    def __init__(self, email, password):
        self.pinky = pinky.Pinky(email, password)

    def take_over_the_world(self):
        # unconditional help
        energy = self.pinky.energy_levels()
        if (not self.pinky.is_alive()) or energy['max'] - energy['value'] < 8:
            self.pinky.intervention()
        elif (energy['max'] - energy['value'] < 30):
            if self.pinky.action() == 3 and self.pinky.health_percentage() <40:
                self.pinky.intervention()
        elif (energy['max'] - energy['value'] < 50):
            if self.pinky.action() == 3 and self.pinky.health_percentage() <15:
                self.pinky.intervention()