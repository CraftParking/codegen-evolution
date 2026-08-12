import math

import pymunk

GROUND_Y = 550
TORSO_WIDTH = 80
TORSO_HEIGHT = 20
TORSO_MASS = 5
LEG_MASS = 1
LEG_LENGTH = 40.0
LEG_THICKNESS = 4
MOTOR_MAX_FORCE = 20_000


def add_ground(space):
    ground = pymunk.Segment(space.static_body, (-1000, GROUND_Y), (100_000, GROUND_Y), 5)
    ground.friction = 1.0
    ground.elasticity = 0.0
    space.add(ground)
    return ground


def build_creature(space, genome, start_x=100):
    torso_y = GROUND_Y - LEG_LENGTH - TORSO_HEIGHT / 2 - 5

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

        leg_moment = pymunk.moment_for_segment(LEG_MASS, (0, 0), (0, LEG_LENGTH), LEG_THICKNESS)
        leg_body = pymunk.Body(LEG_MASS, leg_moment)
        leg_body.position = hip_world
        leg_shape = pymunk.Segment(leg_body, (0, 0), (0, LEG_LENGTH), LEG_THICKNESS)
        leg_shape.friction = 1.0
        space.add(leg_body, leg_shape)

        pivot = pymunk.PivotJoint(torso_body, leg_body, hip_world)
        limit = pymunk.RotaryLimitJoint(torso_body, leg_body, -1.3, 1.3)
        motor = pymunk.SimpleMotor(torso_body, leg_body, 0.0)
        motor.max_force = MOTOR_MAX_FORCE
        space.add(pivot, limit, motor)

        legs.append({"body": leg_body, "shape": leg_shape, "motor": motor, "gene": leg_gene})

    return {"torso": torso_body, "shape": torso_shape, "legs": legs}
