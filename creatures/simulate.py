import math

import pymunk

from creatures.body import GROUND_Y, add_ground, build_creature


def drive_motors(creature, t):
    for leg in creature["legs"]:
        gene = leg["gene"]
        leg["motor"].rate = gene["amplitude"] * math.sin(
            2 * math.pi * gene["frequency"] * t + gene["phase"]
        )


def evaluate(genome, sim_time=6.0, dt=1 / 60.0):
    space = pymunk.Space()
    space.gravity = (0, 900)
    add_ground(space)
    creature = build_creature(space, genome)
    torso = creature["torso"]
    start_x = torso.position.x

    t = 0.0
    for _ in range(int(sim_time / dt)):
        drive_motors(creature, t)
        space.step(dt)
        t += dt
        if torso.position.y > GROUND_Y - 5:
            break

    return torso.position.x - start_x
