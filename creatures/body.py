import math

import pymunk

from creatures.genome import NUM_LEGS

GROUND_Y = 400
CEILING_Y = 20
CEILING_RADIUS = 5
TORSO_WIDTH = 80
TORSO_HEIGHT = 20
TORSO_MASS = 5
LEG_MASS = 1
THIGH_LENGTH = 35.0
SHIN_LENGTH = 35.0
LEG_THICKNESS = 4
MOTOR_MAX_FORCE = 20_000

CEILING_CATEGORY = 0b1
ALL_CATEGORIES = 0xFFFFFFFF
CREATURE_GROUP = 1
# legs ignore the ceiling entirely — only the torso is capped by it, so a leg
# motor can never fight a rigid ceiling constraint and jitter against it.
# shapes sharing a nonzero group never collide with each other, so a
# creature's own torso/thighs/shins can't tangle with one another either.
LEG_FILTER = pymunk.ShapeFilter(group=CREATURE_GROUP, mask=ALL_CATEGORIES & ~CEILING_CATEGORY)
TORSO_FILTER = pymunk.ShapeFilter(group=CREATURE_GROUP)

# collision alone can still let a fast-moving torso tunnel through the thin
# ceiling line in a single physics step; this is the hard, guaranteed floor
# on how high the torso's center can ever end up, enforced every step.
TORSO_MIN_Y = CEILING_Y + TORSO_HEIGHT / 2 + CEILING_RADIUS


def add_ground(space):
    ground = pymunk.Segment(space.static_body, (-1000, GROUND_Y), (100_000, GROUND_Y), 5)
    ground.friction = 1.0
    ground.elasticity = 0.0
    space.add(ground)
    return ground


def add_ceiling(space):
    # hard cap so no jump can ever go higher than the visible window
    ceiling = pymunk.Segment(space.static_body, (-1000, CEILING_Y), (100_000, CEILING_Y), CEILING_RADIUS)
    ceiling.friction = 0.0
    ceiling.elasticity = 0.0
    ceiling.filter = pymunk.ShapeFilter(categories=CEILING_CATEGORY)
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
    torso_shape.filter = TORSO_FILTER
    space.add(torso_body, torso_shape)

    legs = []
    for i in range(NUM_LEGS):
        offset_x = -TORSO_WIDTH / 2 + (i + 0.5) * (TORSO_WIDTH / NUM_LEGS)
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
        thigh_shape.filter = LEG_FILTER
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
        shin_shape.filter = LEG_FILTER
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
            }
        )

    return {"torso": torso_body, "shape": torso_shape, "legs": legs, "genome": genome}
