import pygame
import pymunk

from creatures.body import GROUND_Y, SHIN_LENGTH, THIGH_LENGTH, add_ceiling, add_ground, build_creature
from creatures.evolve_creatures import run
from creatures.simulate import check_stuck, clamp_to_ceiling, drive_motors, make_stuck_tracker

WIDTH, HEIGHT = 900, 500
CAMERA_X = 200
TICK_SPACING = 50


def to_screen(point, camera_offset):
    x, y = point
    return int(x - camera_offset + CAMERA_X), int(y)


def render(genome, sim_time=15.0, dt=1 / 60.0):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("evolved walking creature")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    space = pymunk.Space()
    space.gravity = (0, 900)
    add_ground(space)
    add_ceiling(space)
    creature = build_creature(space, genome)
    torso = creature["torso"]
    start_x = torso.position.x
    tracker = make_stuck_tracker(torso)

    t = 0.0
    running = True
    while running and t < sim_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        drive_motors(creature, t)
        space.step(dt)
        clamp_to_ceiling(creature)
        t += dt

        if check_stuck(torso, tracker):
            # matches evaluate()'s stop condition — don't keep playing past
            # the point evolution never actually got credit/blame for.
            print("creature stopped making progress, ending playback")
            running = False

        camera_offset = torso.position.x

        screen.fill((20, 20, 30))
        pygame.draw.line(screen, (80, 200, 80), (0, GROUND_Y), (WIDTH, GROUND_Y), 3)

        # tick marks scroll past as the creature moves, so progress is visible
        first_tick = int((camera_offset - CAMERA_X) // TICK_SPACING) * TICK_SPACING
        for world_x in range(first_tick, first_tick + WIDTH + TICK_SPACING, TICK_SPACING):
            sx, sy = to_screen((world_x, GROUND_Y), camera_offset)
            pygame.draw.line(screen, (60, 120, 60), (sx, sy - 8), (sx, sy + 8), 2)

        for leg in creature["legs"]:
            thigh_body = leg["hip_body"]
            hip = thigh_body.local_to_world((0, 0))
            knee = thigh_body.local_to_world((0, THIGH_LENGTH))
            pygame.draw.line(
                screen, (200, 160, 60), to_screen(hip, camera_offset), to_screen(knee, camera_offset), 5
            )

            shin_body = leg["knee_body"]
            knee = shin_body.local_to_world((0, 0))
            foot = shin_body.local_to_world((0, SHIN_LENGTH))
            pygame.draw.line(
                screen, (220, 190, 100), to_screen(knee, camera_offset), to_screen(foot, camera_offset), 5
            )

        corners = [torso.local_to_world(v) for v in creature["shape"].get_vertices()]
        pygame.draw.polygon(screen, (80, 160, 230), [to_screen(c, camera_offset) for c in corners])

        distance = torso.position.x - start_x
        text = font.render(f"distance: {distance:.0f}", True, (230, 230, 230))
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    print("evolving creatures... press Ctrl+C to stop and see the best one so far")
    best_genome, best_distance = run(generations=None)
    print(f"\nbest distance traveled: {best_distance:.1f}")
    print("opening a window to show it walking...")
    render(best_genome)
