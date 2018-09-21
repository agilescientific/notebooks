from matplotlib.colors import LinearSegmentedColormap as LSC
from math import pi
import numpy as np

def helix(start=0.5, rot=-1.5, gamma=1.0, reverse=False, n=256, min_sat=1.2, max_sat=1.2, min_light=0, max_light=1, **kwargs):
    
    # Override start and rot if start_hue and end_hue are set.
    if kwargs is not None:
        if 'start_hue' in kwargs:
            start = (kwargs.get('start_hue') / 360. - 1.) * 3.
        if 'end_hue' in kwargs:
            rot = kwargs.get('end_hue') / 360. - start / 3. - 1.
        if 'sat' in kwargs:
            minSat = kwargs.get('sat')
            maxSat = kwargs.get('sat')

    # Set up the parameters.
    fract = np.linspace(min_light, max_light, n)
    angle = 2.0 * pi * (start / 3.0 + rot * fract + 1.)
    fract = fract**gamma

    satar = np.linspace(min_sat, max_sat, n)
    amp = satar * fract * (1. - fract) / 2.

    # Compute the RGB vectors according to main equations.
    red = fract + amp * (-0.14861 * np.cos(angle) + 1.78277 * np.sin(angle))
    grn = fract + amp * (-0.29227 * np.cos(angle) - 0.90649 * np.sin(angle))
    blu = fract + amp * (1.97294 * np.cos(angle))

    # Find where RBB are outside the range [0,1], clip.
    red[np.where((red > 1.))] = 1.
    grn[np.where((grn > 1.))] = 1.
    blu[np.where((blu > 1.))] = 1.

    red[np.where((red < 0.))] = 0.
    grn[np.where((grn < 0.))] = 0.
    blu[np.where((blu < 0.))] = 0.

    # Optional color reverse.
    if reverse is True:
        red = red[::-1]
        blu = blu[::-1]
        grn = grn[::-1]

    # Put in to tuple & dictionary structures needed.
    rr = []
    bb = []
    gg = []
    for k in range(0, int(n)):
        rr.append((float(k) / (n - 1.), red[k], red[k]))
        bb.append((float(k) / (n - 1.), blu[k], blu[k]))
        gg.append((float(k) / (n - 1.), grn[k], grn[k]))

    cdict = {'red': rr, 'blue': bb, 'green': gg}
    
    return LSC('cubehelix_map', cdict)