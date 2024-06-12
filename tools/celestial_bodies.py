class Body():
    def __init__(self, name, mu, soi, radius, mass, semimajor):
        self.name = name
        self.mu = mu
        self.soi = soi
        self.radius = radius
        self.mass = mass
        self.semimajor = semimajor

earth = Body("Earth", 398600, 925000, 6378, 5.974*10**24, 149.6*10**6)
mars = Body("Mars", 42828, 577000, 3396, 641.9*10**21, 227.9*10*6)