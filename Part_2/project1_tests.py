from project1 import Polygon, Polygons
import math

# Testing
def test_polygon():
    rel_tol = 0.001
    abs_tol = 0.001

    try:
        p = Polygon(2,10)
        assert False, ('Creating a polygon with two sides.'
                        'Exception expected, not received.')
    except ValueError:
        pass

    n = 3
    R = 1
    p = Polygon(n,R)
    assert str(p) == 'Polygon(n=3, R=1)', f'actual: {str(p)}'
    assert p.num_vertices == n, (f'actual: {p.num_vertices},'
                                   f' expected: {n}')
    assert p.num_edges == n, f'actual: {p.num_edges}, expected: {n}'
    assert p.circumradius == R, f'actual: {p.circumradius}, expected: {n}'

    n = 4
    R = 1
    p = Polygon(n, R)
    assert p.interior_angle == 90, (f'actual: {p.interior_angle}, expected: 90')
    assert math.isclose(p.area, 2, rel_tol=abs_tol, abs_tol=abs_tol), (
            f'actual: {p.area}, expected: 2.0')
    
    assert math.isclose(p.edge_length, math.sqrt(2), rel_tol=rel_tol, abs_tol=abs_tol), (
            f'actual: {p.edge_length}, expected: {math.sqrt(2)}')
    
    assert math.isclose(p.perimeter, 4*math.sqrt(2), rel_tol=rel_tol, abs_tol=abs_tol), (
            f'actual: {p.perimeter}, expected: {4*math.sqrt(2)}')
    
    assert math.isclose(p.apothem, 0.707, rel_tol=rel_tol, abs_tol=abs_tol), (
            f'actual: {p.perimeter}, expected: 0.707')
    
    p = Polygon(6, 2)
    assert math.isclose(p.edge_length, 2, rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.apothem, 1.73205, rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.area, 10.3923, rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.perimeter, 12, rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.interior_angle, 120, rel_tol=rel_tol, abs_tol=abs_tol)
    
    p = Polygon(12, 3)
    assert math.isclose(p.edge_length, 1.55291, rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.apothem, 2.89778, rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.area, 27, rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.perimeter, 18.635, rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.interior_angle, 150, rel_tol=rel_tol, abs_tol=abs_tol)
    
    p1 = Polygon(3, 10)
    p2 = Polygon(10, 10)
    p3 = Polygon(15, 10)
    p4 = Polygon(15, 100)
    p5 = Polygon(15, 100)
    
    assert p2 > p1
    assert p2 < p3
    assert p3 != p4
    assert p1 != p4
    assert p4 == p5

test_polygon()


def test_polygons():
    try:
        p = Polygons(2,10)
        assert False, ('Creating a polygon with two sides.'
                        'Exception expected, not received.')
    except ValueError:
        pass

    p = Polygons(5,1)
    assert str(p) == 'Polygons(max_n=5, R=1)', f'actual: {str(p)}'
    assert len(p) == 3
    assert p.max_efficiency_poly == Polygon(5,1), f'actual: {str(p.max_efficiency_poly)}'
    assert p[0] == Polygon(3,1), f'actual: {str(p[0])}'
    assert p[-1] == Polygon(5,1), f'actual: {str(p[0])}'

test_polygons()