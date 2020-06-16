import numpy as np

class Vec3(np.ndarray):
    
    def __new__(cls, i, j, k, dtype=np.float64):
        """
        Vector 3 object
        i, j, k:    Components of the vector 3                                   [instance of dtype]
        dtype:      The datatype that should be used to store the components.    [type]
        Returns:    Vec3 object
        """
        obj = np.array([[i,j,k]],dtype=dtype).T.view(cls)
        return obj
    
    def __repr__(self):
        """
        Returns a string representation of the Vec3 object.
        Returns:    String
        """
        return "Vec3[{0:.2f},{1:.2f},{2:.2f}]".format(self[0][0],self[1][0],self[2][0])
    
    def __str__(self):
        """
        Returns a string representation of the Vec3 object to print, returns same as __repr__
        Returns:    String
        """
        return self.__repr__()

    @classmethod
    def from_iterable(cls, iter, dtype=np.float64):
        """
        Returns a Vec3 object created from an iterable
        iter:   Iterable to form the Vec3 from                              [iterable]
        dtype:  The datatype used to store the components of the vector     [type]
        Returns: Vec3 object
        """
        obj = np.array([iter],dtype=dtype).T.view(cls)
        assert obj.shape == (3,1)
        return obj

    def to_list(self):
        """
        Returns a flat list representation of the vector
        Returns: list
        """
        return list([self[i][0] for i in range(3)])