def circle_locus(regexgroups: tuple[str]) -> tuple[str, dict[str, float]]:
    center = [0, 0]
    radius = 1
    # check if the circle is in the form |* \pm z| or in the form |z \pm *|
    # firstly, if it is in the form |z| = num
    if regexgroups[13] != None:
        if regexgroups[13][:3] == "|z|":
            center = [0, 0]
            radius = float(regexgroups[14])
    # if in the form |z \pm *|
    elif regexgroups[1] != None:
        if regexgroups[1].startswith("z"):
            # taking into account the sign after z
            if regexgroups[8] == "-":
                coeff = -1
            elif regexgroups[8] == "+":
                coeff = 1
            # finding the (a \pm bi) values of a and b
            if regexgroups[10] != None: 
                center[0] = coeff*-float(regexgroups[10])
                coeff = 1
            if regexgroups[11] != None:
                y = regexgroups[11][:-1]
                if y == "+":
                    center[1] = -1
                elif y == "-":
                    center[1] = 1
                elif y == "":
                    y = 1
                    center[1] = coeff*-float(y)
                else:
                    center[1] = coeff*-float(y)
            radius = float(regexgroups[12])
        # if in the form |* \pm z|
    else:
        # if in the form |* p z|
        if regexgroups[1][-2] == "-":
            coeff = 1
        # if in the form |* m z|
        else:
            coeff = -1
        if regexgroups[4] != None: 
            center[0] = coeff*float(regexgroups[4])
        if regexgroups[5] != None:
            y = regexgroups[5][:-1]
            if y == "" or y == "+":
                center[1] = coeff * 1
            elif y == "-":
                center[1] = coeff * -1
            else:
                center[1] = coeff*float(y)
        radius = float(regexgroups[12])
    # if radius is zero
    if radius <= 0 or radius >= 1073741824 or center[0] >= 1073741824 or center[1] >= 1073741824 or center[0] <= -1073741824 or center[1] <= -1073741824:
        return None
    return ("circle", {"radius": radius, "center": tuple(center)})