import math

import pymunk

from creatures.body import GROUND_Y, TORSO_MIN_Y, add_ceiling, add_ground, build_creature
from creatures.brain import forward


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


def evaluate(genome, sim_time=6.0, dt=1 / 60.0):
    space = pymunk.Space()
    space.gravity = (0, 900)
    add_ground(space)
    add_ceiling(space)
    creature = build_creature(space, genome)
    torso = creature["torso"]
    start_x = torso.position.x

    t = 0.0
    for _ in range(int(sim_time / dt)):
        drive_motors(creature, t)
        space.step(dt)
        clamp_to_ceiling(creature)
        t += dt
        if torso.position.y > GROUND_Y - 5:
            break

    return torso.position.x - start_x
