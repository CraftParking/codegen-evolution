import math

import pymunk

GROUND_Y = 400
CEILING_Y = 20
TORSO_WIDTH = 80
TORSO_HEIGHT = 20
TORSO_MASS = 5
LEG_MASS = 1
THIGH_LENGTH = 35.0
SHIN_LENGTH = 35.0
LEG_THICKNESS = 4
MOTOR_MAX_FORCE = 20_000


def add_ground(space):
    ground = pymunk.Segment(space.static_body, (-1000, GROUND_Y), (100_000, GROUND_Y), 5)
    ground.friction = 1.0
    ground.elasticity = 0.0
    space.add(ground)
    return ground


def add_ceiling(space):
    # hard cap so no jump can ever go higher than the visible window
    ceiling = pymunk.Segment(space.static_body, (-1000, CEILING_Y), (100_000, CEILING_Y), 5)
    ceiling.friction = 0.0
    ceiling.elasticity = 0.0
    space.add(ceiling)
    return ceiling


def build_creature(space, genome, start_x=100):
    torso_y = GROUND_Y - (THIGH_LENGTH + SHIN_LENGTH) - TORSO_HEIGHT / 2 - 5

    # infinite moment of inertia: torso can translate but never rotate,
    # so leg motor reaction torque can't spin/roll it — only the legs move.
    torso_body = pymunk.Body(TORSO_MASS, math.inf)
    torso_body.position = (start_x, torso_y)
    torso_shape = pymunk.Poly.create_box(torso_body, (TORSO_WIDTH, TORSO_HEIGHT))
    torso_shape.friction = 0.5
    space.add(torso_body, torso_shape)

    num_legs = len(genome)
    legs = []
    for i, leg_gene in enumerate(genome):
        offset_x = -TORSO_WIDTH / 2 + (i + 0.5) * (TORSO_WIDTH / num_legs)
        hip_world = (
            torso_body.position.x + offset_x,
            torso_body.position.y + TORSO_HEIGHT / 2,
        )
        knee_world = (hip_world[0], hip_world[1] + THIGH_LENGTH)

        thigh_moment = pymunk.moment_for_segment(LEG_MASS, (0, 0), (0, THIGH_LENGTH), LEG_THICKNESS)
        thigh_body = pymunk.Body(LEG_MASS, thigh_moment)
        thigh_body.position = hip_world
        thigh_shape = pymunk.Segment(thigh_body, (0, 0), (0, THIGH_LENGTH), LEG_THICKNESS)
        thigh_shape.friction = 1.0
        space.add(thigh_body, thigh_shape)

        hip_pivot = pymunk.PivotJoint(torso_body, thigh_body, hip_world)
        hip_limit = pymunk.RotaryLimitJoint(torso_body, thigh_body, -1.3, 1.3)
        hip_motor = pymunk.SimpleMotor(torso_body, thigh_body, 0.0)
        hip_motor.max_force = MOTOR_MAX_FORCE
        space.add(hip_pivot, hip_limit, hip_motor)

        shin_moment = pymunk.moment_for_segment(LEG_MASS, (0, 0), (0, SHIN_LENGTH), LEG_THICKNESS)
        shin_body = pymunk.Body(LEG_MASS, shin_moment)
        shin_body.position = knee_world
        shin_shape = pymunk.Segment(shin_body, (0, 0), (0, SHIN_LENGTH), LEG_THICKNESS)
        shin_shape.friction = 1.0
        space.add(shin_body, shin_shape)

        knee_pivot = pymunk.PivotJoint(thigh_body, shin_body, knee_world)
        knee_limit = pymunk.RotaryLimitJoint(thigh_body, shin_body, -1.3, 1.3)
        knee_motor = pymunk.SimpleMotor(thigh_body, shin_body, 0.0)
        knee_motor.max_force = MOTOR_MAX_FORCE
        space.add(knee_pivot, knee_limit, knee_motor)

        legs.append(
            {
                "hip_body": thigh_body,
                "hip_shape": thigh_shape,
                "hip_motor": hip_motor,
                "knee_body": shin_body,
                "knee_shape": shin_shape,
                "knee_motor": knee_motor,
                "gene": leg_gene,
            }
        )

    return {"torso": torso_body, "shape": torso_shape, "legs": legs}
