from .vec3 import Vec3
import numpy as np

class Body(object):
    """
    Object modelling a massive body
    """
    
    def __str__(self):
        """
        Returns a printable representation of the body object. 
        Returns: string
        """
        return """
        Body Instance {0}:
        mass          = {1}
        position      = {2}
        velocity      = {3}
        acceleration  = {4}
        forces        = {5}
        id            = {6}
        """.format(
            self.name,
            self.mass,
            self.pos,
            self.vel,
            self.acc,
            self.static_forces + self.variable_forces,
            self.id)
    
    def __repr__(self):
        """
        Returns a string representation of the body object.
        Returns: string
        """
        return "\nBody<{0}>(mass={1},pos={2},vel={3},acc={4},id={5})".format(
            self.name,
            self.mass,
            self.pos,
            self.vel,
            self.acc,
            self.id)
    
    def __init__(
        self, mass=1,
        initial_pos=Vec3(0,0,0), 
        initial_vel=Vec3(0,0,0), 
        initial_acc=Vec3(0,0,0),
        forces=[],
        name=""):
        
        """ 
        Body object constructor
        mass:        The mass of the body                     [float]
        initial_pos: The position of the body as t = 0        [Vec3]
        initial_vel: The velocity of the body at t = 0        [Vec3]
        initial_acc: The acceleration of the body at t = 0    [Vec3]
        forces:      The forces acting upon the body          [Vec3 iterable]
        name:        The name of the body                     [String]
        Returns:     None
        """
        
        # Assert that the arguments are correct.
        assert np.isreal(mass)
        assert isinstance(initial_pos, Vec3)
        assert isinstance(initial_vel, Vec3)
        assert isinstance(initial_acc, Vec3)
        assert all([isinstance(f, Vec3) for f in forces])
        
        self.mass = mass
        self.pos = initial_pos
        self.vel = initial_vel
        self.acc = initial_acc
        self.static_forces = forces
        self.variable_forces = []
        self.name = name
        self.id = None
        
    def tstep(self,timestep=1e-3):
        """
        Update each variable
        timestep:    The timestep to use                               [float]
        Returns:     (new position, new velocity, new acceleration)
        """
        sum_force = np.sum(self.static_forces + self.variable_forces, axis=0)
        self.acc = sum_force * (1 / self.mass)
        self.vel += self.acc*timestep
        self.pos += self.vel*timestep
        return (self.pos, self.vel, self.acc)
    