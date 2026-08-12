import math

import pymunk

from creatures.body import TORSO_MIN_Y, add_ceiling, add_ground, build_creature
from creatures.brain import forward

# a stuck/collapsed creature has stopped making forward progress, whatever
# it's doing with its legs while it flails — that's a more robust signal than
# torso height, since a genuinely walking creature's height swings a lot too
# (~60 units per stride is normal) so a height threshold alone misfires.
STUCK_CHECK_STEPS = 60
STUCK_MIN_PROGRESS = 3.0


def drive_motors(creature, t):
    genome = creature["genome"]
    num_legs = len(creature["legs"])
    for i, leg in enumerate(creature["legs"]):
        thigh = leg["hip_body"]
        shin = leg["knee_body"]
        inputs = [
            math.sin(t),
            math.cos(t),
            thigh.angle,
            thigh.angular_velocity,
            shin.angle - thigh.angle,
            shin.angular_velocity - thigh.angular_velocity,
            i / num_legs,
        ]
        hip_rate, knee_rate = forward(genome, inputs)
        leg["hip_motor"].rate = hip_rate
        leg["knee_motor"].rate = knee_rate


def clamp_to_ceiling(creature):
    torso = creature["torso"]
    if torso.position.y < TORSO_MIN_Y:
        torso.position = (torso.position.x, TORSO_MIN_Y)
        vx, vy = torso.velocity
        torso.velocity = (vx, max(vy, 0.0))


def make_stuck_tracker(torso):
    return {"checkpoint_x": torso.position.x, "steps_since_check": 0}


def check_stuck(torso, tracker):
    """True once STUCK_CHECK_STEPS have passed with under STUCK_MIN_PROGRESS
    of net horizontal movement — i.e. it's no longer going anywhere."""
    tracker["steps_since_check"] += 1
    if tracker["steps_since_check"] < STUCK_CHECK_STEPS:
        return False
    progressed = abs(torso.position.x - tracker["checkpoint_x"])
    tracker["checkpoint_x"] = torso.position.x
    tracker["steps_since_check"] = 0
    return progressed < STUCK_MIN_PROGRESS


def evaluate(genome, sim_time=6.0, dt=1 / 60.0):
    space = pymunk.Space()
    space.gravity = (0, 900)
    add_ground(space)
    add_ceiling(space)
    creature = build_creature(space, genome)
    torso = creature["torso"]
    start_x = torso.position.x
    tracker = make_stuck_tracker(torso)

    t = 0.0
    for _ in range(int(sim_time / dt)):
        drive_motors(creature, t)
        space.step(dt)
        clamp_to_ceiling(creature)
        t += dt
        if check_stuck(torso, tracker):
            break

    return torso.position.x - start_x
