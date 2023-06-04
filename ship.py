import numpy as np
import copy


def _reader_(string, md=0):
    res = [float(_) for _ in string.split()]
    res.append(float(md))
    return res


def _angle_(a, b):
    mul_ = np.dot(a, b)
    l_a, l_b = 0, 0
    for _ in range(len(a)):
        l_a += a[_] * a[_]
        l_b += b[_] * b[_]
    if l_a * l_b != 0:
        return np.arccos(mul_ / (np.sqrt(l_a * l_b))) * 180 / np.pi
    else:
        return 0


def _plane_(a, b, c):
    d_x = (c[2] - a[2]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[2] - a[2])
    d_y = (c[0] - a[0]) * (b[2] - a[2]) - (c[2] - a[2]) * (b[0] - a[0])
    d_z = (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])
    _d_ = (-1) * (d_x * a[0] + d_y * a[1] + d_z * a[2])
    return [d_x, d_y, d_z, _d_]


def _push_rotation_(norm, fire, side):
    angle = _angle_(norm, fire)
    cr_mul = np.cross(norm, fire)
    z = cr_mul[2]
    r = 1
    if z * side <= 0:
        r = -1
    return angle * r


def main():
    with open("input.txt", mode="rt") as f:
        v = _reader_(f.readline())
        a = _reader_(f.readline())
        m = _reader_(f.readline(), 1)
        w = _reader_(f.readline())
    a_real_z = (-1) * (m[0] * a[0] + m[1] * a[1]) / m[2]
    a_real = [a[0], a[1], a_real_z]
    push_left = np.cross(m, a_real)
    push_right = np.cross(a_real, m)

    mast_angle = _angle_([0, 0, 1], m)
    side = 0
    angle_pushka = 0

    # construct the plane
    p_1 = [v[0], v[1], v[2]]
    p_2 = [v[0] + push_right[0], v[1] + push_right[1], v[2] + push_right[2]]
    p_3 = [v[0] + a_real[0], v[1] + a_real[1], v[2] + a_real[2]]

    pl = _plane_(p_1, p_2, p_3)
    z_fight = 0

    if pl[2] != 0:
        z_fight = (-1) * (w[0] * pl[0] + w[1] * pl[1] + pl[3]) / pl[2]
    if z_fight >= 0:
        fire = [w[0] - v[0], w[1] - v[1], z_fight]

        l_fire = _push_rotation_(push_left, fire, -1)
        r_fire = _push_rotation_(push_right, fire, 1)

        if -60 < l_fire < 60:
            angle_pushka = l_fire
            side = 1
        elif -60 < r_fire < 60:
            angle_pushka = r_fire
            side = -1

    with open("output.txt", "w") as out:
        out.write(str(side) + '\n' + str(angle_pushka) + '\n' + str(mast_angle) + '\n' + "bye")


main()
