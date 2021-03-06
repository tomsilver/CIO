import numpy as np
from world import World, Circle, Contact, Position
from params import Params, StageWeights
from CIO import visualize_result, CIO
from util import save_run
import argparse
from collections import OrderedDict

def main(args):
    if args.debug:
        import pdb; pdb.set_trace()
    # objects
    radius = 5.0
    manip_obj = Circle(radius, Position(5.0,radius))
    finger0 = Circle(1.0, Position(-5.0, -5.0))
    finger1 = Circle(1.0, Position(15.0, -5.0))

    # initial contact information
    contact_state = OrderedDict([(finger0, Contact(f=(0.0, 0.0), ro=(-7., -7.), c=.5)),
                                 (finger1, Contact(f=(0.0, 0.0), ro=(7., -7.), c=.5))])
    goals = [Position(5.0, 20.0)]

    world = World(manip_obj, [finger0, finger1], contact_state)

    stage_weights=[StageWeights(w_CI=0.1, w_physics=0.1, w_kinematics=0.0, w_task=1.0),
                    StageWeights(w_CI=10.**1, w_physics=10.**0, w_kinematics=0., w_task=10.**1)]
    p = Params(world, K=10, delT=0.05, delT_phase=0.5, mass=1.0,
                    mu=0.9, lamb=10**-3, stage_weights=stage_weights)

    if args.single:
        stage_info = CIO(goals, world, p, single=True)
    else:
        stage_info = CIO(goals, world, p)

    if args.save:
        save_run(args.save, p, world, stage_info)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--single', action='store_true')
    parser.add_argument('--save', type=str)
    args = parser.parse_args()
    main(args)
