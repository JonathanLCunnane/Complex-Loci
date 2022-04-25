from math import pi


def __parse_circle(params: tuple[str, dict[str, float]]):
    """
    A post intepretation parsing check, to check if the circle's parameters are valid.
    """
    if params[1]["radius"] <= 0 or params[1]["radius"] >= 1073741824 or params[1]["center"][0] >= 1073741824 or params[1]["center"][1] >= 1073741824 or params[1]["center"][0] <= -1073741824 or params[1]["center"][1] <= -1073741824:
        return None
    return params


def __parse_perp_bisector(params: tuple[str, dict[str, float]]):
    """
    A post intepretation parsing check, to check if the perpendicular bisector's parameters are valid.
    """
    if params[1]["point_a"][0] >= 1073741824 or params[1]["point_a"][0] <= -1073741824 or params[1]["point_a"][1] >= 1073741824 or params[1]["point_a"][1] <= -1073741824 or params[1]["point_b"][0] >= 1073741824 or params[1]["point_b"][0] <= -1073741824 or params[1]["point_b"][1] >= 1073741824 or params[1]["point_b"][1] <= -1073741824:
        return None
    return params


def __parse_half_line(params: tuple[str, dict[str, float]]):
    """
    A post intepretation parsing check, to check if the half line's parameters are valid.
    """
    if params[1]["point"][0] >= 1073741824 or params[1]["point"][0] <= -1073741824 or params[1]["point"][1] >= 1073741824 or params[1]["point"][1] <= -1073741824:
        return None
    return params


def __point_from_string(regexgroup: str) -> tuple[float, float]:
    # check for empty value
    if regexgroup == "z" or regexgroup == None:
        regexgroup = "z+0+0j"
    # firstly replace i's with j's
    for char in ["i", "I"]:
        regexgroup = regexgroup.replace(char, "j")
    # if point is in the form |z \pm point|
    if regexgroup[0] == "z":
        regexgroup = regexgroup[1:]
        coeff = -1
    # if point is in the form |point \pm z|
    else:
        # if point is in the form |point - z|
        if regexgroup[-2] == "-":
            coeff = 1
        # if point is in the form |point + z|
        else:
            coeff = -1
        regexgroup = regexgroup[:-2]
    regexgroup = complex(regexgroup)
    return (coeff*regexgroup.real, coeff*regexgroup.imag)


def circle_locus(regexgroups: tuple[str]) -> tuple[str, dict[str, float]]:
    center = __point_from_string(regexgroups[1])
    # if the circle is in the form |z| = 4
    if regexgroups[13]:
        radius = float(regexgroups[14])
    # any other form
    else:
        radius = float(regexgroups[12])
    circle = ("circle", {"radius": radius, "center": tuple(center)})
    return __parse_circle(circle)


def perp_bisector_locus(regexgroups: tuple[str]) -> tuple[str, dict[str, float]]:
    # find point a and point b
    # if a is in the form |z \pm point|
    a = __point_from_string(regexgroups[1])
    b = __point_from_string(regexgroups[12])
    # check if the points are the same
    if a == b:
        return None
    return __parse_perp_bisector(("perpendicular_bisector", {"point_a": a, "point_b": b}))


def half_line_locus(regexgroups: tuple[str]) -> tuple[str, dict[str, float]]:
    # find the point where the half line originates from
    point = __point_from_string(regexgroups[1])
    # find the angle of the half line between -pi and pi
    theta = float(regexgroups[12])
    while theta > pi or theta <= -pi:
        if theta < 0:
            theta += 2*pi
        else:
            theta -= 2*pi
    return __parse_half_line(("half_line", {"point": point, "theta": theta}))
