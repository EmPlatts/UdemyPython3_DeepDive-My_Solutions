"""
PROJECT 1
Create a Polygon class and a Polygons sequence type.
"""
from numbers import Real
import math

class Polygon:
    """ A regular strictly convex polygon with:
            - n: edges (=n vertices)
            - R: circumradius
        Properties:
            - num_edges
            - circumradius
            - num_vertices
            - interior_angle
            - edge_length
            - apothem
            - area
            - perimeter
    """
    def __init__(self, n, R):
        if isinstance(n,int) and n>2:
            self._n = n
        else:
            raise ValueError("n must be an integer of at least 3.")
        if isinstance(R,Real) and R>0:
            self._R = R
        else:
            raise ValueError("R must be real and non-negative.")

    def __repr__(self):
        return(f'Polygon(n={self._n}, R={self._R})')

    @property
    def num_edges(self):
        return self._n
    
    @property
    def circumradius(self):
        return self._R

    @property
    def num_vertices(self):
        return self._n
    
    @property
    def interior_angle(self):
        return (self._n-2)*180/self._n

    @property
    def edge_length(self):
        return 2*self._R*math.sin(math.pi/self._n)

    @property
    def apothem(self):
        return self._R*math.cos(math.pi/self._n)
    
    @property
    def area(self):
        return 0.5*self._n*self.edge_length*self.apothem
    
    @property
    def perimeter(self):
        return self._n*self.edge_length

    def __eq__(self,other):
        if isinstance(other,Polygon):
            return (self.num_edges==other.num_edges and
                    self.circumradius==other.circumradius)
        else:
            return NotImplemented

    def __gt__(self,other):
        if isinstance(other,Polygon):
            return self.num_vertices>other.num_vertices
        else:
            return NotImplemented

class Polygons:
    """Creates a sequence of Polygon objects with num_edges=3 to num_edges=max_n
    and with a common circumradius R.
    
    """
    def __init__(self, max_n, R):
        if isinstance(max_n,int) and max_n>2:
            self._max_n = max_n
        else:
            raise ValueError("max_n must be an integer of at least 3.")
        if isinstance(R,Real) and R>0:
            self._R = R
        else:
            raise ValueError("R must be real and non-negative.")
        self._polygons = [Polygon(x,self._R) for x in range(3,self._max_n+1)]

    def __repr__(self):
        return f'Polygons(max_n={self._max_n}, R={self._R})'

    def __len__(self):
        return (self._max_n-2)

    def __getitem__(self,s):
        return self._polygons[s]

    @property
    def max_efficiency_poly(self): #could also use sorted() - see Fred's solutions
        efficiency_ratios = {x: Polygon(x,self._R).area/Polygon(x,self._R).perimeter \
                            for x in range(3,self._max_n+1)}
        return Polygon(max(efficiency_ratios, key=efficiency_ratios.get), self._R)