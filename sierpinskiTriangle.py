import random
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt


def sierpinski(p0, vs, f, inum):
    p = [(0,0)]
    current_point = p0
    for _ in range(inum):
        vslist = vs.tolist()
        random_vertex_x_value = random.choice(vslist[0])
        random_vertex_y_value = vs[1][vslist[0].index(random_vertex_x_value)]
        random_vertex = (random_vertex_x_value,random_vertex_y_value)
        new_point = [(f*(random_vertex[0]-current_point[0]))+current_point[0], (f*(random_vertex[1]-current_point[1]))+current_point[1]]
        current_point = new_point
        p.append(current_point)
    return np.array(p)
    pass


def init_test_data():
    vs = [[-sqrt(3)/2, sqrt(3)/2, 0], [-1/2, -1/2, 1]]
    p0 = [0, 0]
    f = 1/2
    return f, np.array(p0), np.array(vs)


def check_return(sierpinski_pts):
    if type(sierpinski_pts) != np.ndarray:
        raise RuntimeError("Expected sierpinski to return an np.ndarray!")
    try:
        if sierpinski_pts.shape[1] != 2:
            raise
    except Exception:
        raise RuntimeError("Expected sierpinski to have shape '(n,2)'\n"
                           f"Instead has shape {sierpinski_pts.shape}")
    return sierpinski_pts


def test_1():
    """Purely graphical"""
    print('**************************************')
    print("Graphical test")
    print('**************************************')
    f, p0, vs = init_test_data()
    for n in 1000, 10000, 100000:
        xs, ys = check_return(sierpinski(p0, vs, f, n)).transpose()
        fig = plt.figure()
        plt.plot(xs, ys, linestyle='', marker='.', markersize=0.5, figure=fig)
        fig.gca().set_title(f"Sierpinski Triangle - Chaos Game n={n}")
        fig.savefig(f"test-{n}.pdf")
        plt.show()
    return 0


def test_2():
    """Test if points exist in expected locations"""
    print('**************************************')
    print("Value test, checking if points exist")
    print('**************************************')
    f, p0, vs = init_test_data()
    n = 1000000
    random.seed(101)
    ps = np.around(check_return(sierpinski(p0, vs, f, n)), decimals=3)
    # convert to string for more stable representation
    ps = [[str(x), str(y)] for [x, y] in ps]
    count = 0
    if ['0.0', '0.0'] in ps:
        count += 5
    if ['0.3', '-0.364'] in ps:
        count += 5
    if ['-0.17', '0.321'] in ps:
        count += 5
    if ['-0.783', '-0.358'] in ps:
        count += 5
    return count


def is_empty_function(func):
    # https://stackoverflow.com/a/24689937/1371191

    def empty_func():
        pass

    def empty_func_with_doc():
        """Empty function with docstring."""
        pass

    return func.__code__.co_code == empty_func.__code__.co_code \
        or func.__code__.co_code == empty_func_with_doc.__code__.co_code


def test_required(fns):
    for fnname in fns:
        if fnname not in globals():
            raise RuntimeError(f'missing function {fnname}')
        elif (is_empty_function(globals()[fnname])):
            raise RuntimeError(f'fill in {fnname}!')


def main(week, tests):
    import os
    import re
    import traceback

    f = os.path.basename(__file__)
    r = re.compile('^([a-zA-Z]]+).py$')
    m = r.match(f)
    count = 0
    for test, requirements in tests:
        try:
            test_required(requirements)
            count += test()
        except Exception:
            traceback.print_exc()


if __name__ == '__main__':
    tests = [(test_1, ['sierpinski']),
             (test_2, ['sierpinski'])]
    main(7, tests)
