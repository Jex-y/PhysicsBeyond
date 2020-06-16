from .vec3 import Vec3
from .body import Body
import numpy as np
import json

class Environment(object):
    """
    Class that allows for the simulation of multiple interacting bodies. 
    """
    def __init__(self,bodies=[],external_forces=[],gravity=False):
        """
        Environment object constructor
        bodies:             The bodies in the scope of the enviroment.                 [Body iterable]
        external_forces:    Forces that apply to every body in the enironemnt.         [Vec3 iterable]
        gravity:            Weather to calculate gravitational pull between bodies.    [boolean]
        timestep:           The timestep to use for the simulation.                    [float]
        Returns:            None
        """
        
        # Assert that the arguments are correct.
        assert all([isinstance(b, Body) for b in bodies])
        assert all([isinstance(f, Vec3) for f in external_forces])
        assert type(gravity) == bool
        
        self.bodies = bodies
        self.num_bodies = len(bodies)
        
        for (body_id, body) in enumerate(self.bodies):
            body.id = body_id
        
        for b in self.bodies:
            b.static_forces += external_forces
        
        self.gravity = gravity
                
        self.t = 0
            
    def __update_gravity(self):
        """
        Private method to update the calculation of the force of gravity between each body in the scope of the simulation. 
        """
        from scipy.constants import G
        for body_a in self.bodies:
            for body_b in self.bodies:
                if body_a == body_b:
                    break
                
                displacement_ab = body_b.pos - body_a.pos
                radius_ab = np.linalg.norm(displacement_ab)
                unit_ab = displacement_ab / radius_ab
                force_ab = (G * body_a.mass * body_b.mass)/(radius_ab**2) * unit_ab
                force_ba = -1* force_ab
                self.gravity_forces[body_a.id][body_b.id] = force_ab
                self.gravity_forces[body_b.id][body_a.id] = force_ba
    
    def run(self, tfinal=0, tinitial = 0, timestep = 1e-3, num_timesteps=None, timestep_callback=None, loop=False):
        """
        Public method to run the simulation of the enviroment.
        tfinal:           Time to simulate up to.            [float]
        tinital:          Time to start simulation at.       [float]
        timestep:         The timestep to use.               [float]
        num_timesteps:    The number of timesteps to use.    [int]
        loop:             Weather to loop infinitly          [bool]
        Returns:          Iterable of the bodies in the simulation. 
        
        If both num_timesteps and timestep are specified, num_timesteps will be used.
        tinital shoud only be used if the simulation is being continued from a prievious run.
        If loop is true then the simulation runs indefinitly e.g. if driving a continuous animation.
        """
        
        assert np.isreal(tinitial) and tinitial <= self.t
        assert np.isreal(timestep) or timestep
        assert np.issubdtype(type(num_timesteps), np.integer) or num_timesteps==None
        assert np.isreal(tfinal) and (tfinal > self.t or loop)

        if not num_timesteps:
            num_timesteps = int((tfinal-tinitial)/timestep)
        elif not loop:
            timestep = num_timesteps / (tfinal-tinitial)
        
        self.t = tinitial # Maybey if history implemented roll back bodies to tinital

        while self.t<tfinal or loop:
            if self.gravity:
                self.gravity_forces = [[Vec3(0,0,0) for _ in range(self.num_bodies)] for _ in range(self.num_bodies)]
                for i in range(self.num_bodies):
                    self.gravity_forces[i][i] = None
                self.__update_gravity()
                for body in self.bodies:
                    body.variable_forces = list(filter(None.__ne__,self.gravity_forces[body.id]))

            for body in self.bodies: # This part could be parellised, avoid race conditions though.
                body.tstep(timestep)

            if timestep_callback:
                timestep_callback()
            
            self.t += timestep
        
        return self.bodies

    def save(self,filepath):
        """
        Saves the environment state to a json file given in filepath
        filepath:   Path to save the json file
        Returns:    None
        """
        data = {}
        data["bodies"] = []
        for body in self.bodies:
            data["bodies"].append({
                "name"      :body.name,
                "mass"      :body.mass,
                "pos"       :body.pos.to_list(),
                "vel"       :body.vel.to_list(),
                "acc"       :body.acc.to_list(),
                "forces"    :[f.to_list() for f in body.static_forces]
            })

        data["state"] = {
            "gravity":self.gravity,
            "t":self.t
        }
        
        with open(filepath,'w') as json_out:
            json.dump(data, json_out)

    def load(self,filepath):
        """
        Loads the environment save state from a json file
        filepath:   The path to the json file containing the save state.
        Returns:    None
        Raises:
            FileNotFoundError if the filepath does not exsist. 

        Used over from_json if reseting environment that has already been initialised.
        """
        with open(filepath) as json_in:
            data = json.load(json_in)
        for body in data["bodies"]:
            self.bodies.append(Body(
                mass=           body["mass"],
                initial_pos=    Vec3.from_iterable(body["pos"]),
                initial_vel=    Vec3.from_iterable(body["vel"]),
                initial_acc=    Vec3.from_iterable(body["acc"]),
                forces=         [Vec3.from_iterable(f) for f in body["forces"]],
                name=           body["name"]
            ))

        self.gravity = data["state"]["gravity"]
        self.t = data["state"]["t"]

    @staticmethod
    def from_json(filepath):
        """
        Creates an environment object from a json file save state.
        filepath:   The path of the json save file. [String]
        Returns:    Environemnt Object
        Raises:
            FileNotFoundError if the filepath does not exsist. 
        """
        obj = Environment()
        obj.load(filepath)
        obj.num_bodies = len(obj.bodies)
        for i in range(obj.num_bodies):
            obj.bodies[i].id = i
        return obj