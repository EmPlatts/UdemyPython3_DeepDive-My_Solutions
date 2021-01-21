l = [1,2,3,4,'python']

# Nested unpacking:
a, *b, (c, d, *e) = l
print(a, b, c, d, e)

# Slicing:
a, b, c, d, e = l[0], l[1:-1], l[-1][0], l[-1][1], list(l[-1][2:])
print(a, b, c, d, e)