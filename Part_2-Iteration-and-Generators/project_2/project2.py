"""
PROJECT 2
Refactor Polygon class to make calculated propetries lazy and refactor the 
Polygons sequence type to be an iterator.
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
        self._interior_angle = None
        self._edge_length = None
        self._apothem = None
        self._area = None
        self._perimeter = None


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
        if self._interior_angle is None:
            self._interior_angle = (self._n-2)*180/self._n
        return self._interior_angle

    @property
    def edge_length(self):
        if self._edge_length is None:
            self._edge_length = 2*self._R*math.sin(math.pi/self._n)
        return self._edge_length

    @property
    def apothem(self):
        if self._apothem is None:
            self._apothem = self._R*math.cos(math.pi/self._n)
        return self._apothem
    
    @property
    def area(self):
        if self._area is None:
            self._area = 0.5*self._n*self.edge_length*self.apothem
        return self._area
    
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

class PolygonIter:
    def __init__(self,_max_n,_R):
        if not isinstance(_max_n,int) and _max_n<3:
            raise ValueError("max_n must be an integer of at least 3.")
        self._max_n = _max_n
        self._R = _R
        self._i = 3 #Polygon starts at 3

    def __iter__(self):
            return self

    def __next__(self):
        if self._i>=self._max_n+1:
            raise StopIteration
        else:
            result = Polygon(self._i,self._R)
            self._i+=1
            return result

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
    
    def __len__(self):
        return (self._max_n-2)

    def __repr__(self):
        return f'Polygons(max_n={self._max_n}, R={self._R})'

    def __iter__(self):
        return PolygonIter(self._max_n,self._R)

    @property
    def max_efficiency_poly(self): #using sorted() now, as in see Fred's solutions
        sorted_efficiency_ratios = sorted(PolygonIter(self._max_n,self._R), 
                                    key = lambda p: p.area/p.perimeter,
                                    reverse=True)
        return sorted_efficiency_ratios[0]
