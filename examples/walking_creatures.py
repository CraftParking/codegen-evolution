import pygame
import pymunk

from creatures.body import GROUND_Y, add_ground, build_creature
from creatures.evolve_creatures import run
from creatures.simulate import drive_motors

WIDTH, HEIGHT = 900, 500
CAMERA_X = 200


def to_screen(point, camera_offset):
    return int(point.x - camera_offset + CAMERA_X), int(point.y)


def render(genome, sim_time=15.0, dt=1 / 60.0):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("evolved walking creature")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0, 900)
    add_ground(space)
    creature = build_creature(space, genome)
    torso = creature["torso"]

    t = 0.0
    running = True
    while running and t < sim_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        drive_motors(creature, t)
        space.step(dt)
        t += dt

        camera_offset = torso.position.x

        screen.fill((20, 20, 30))
        pygame.draw.line(screen, (80, 200, 80), (0, GROUND_Y), (WIDTH, GROUND_Y), 3)

        for leg in creature["legs"]:
            leg_body = leg["body"]
            a = leg_body.local_to_world((0, 0))
            b = leg_body.local_to_world((0, leg["gene"]["length"]))
            pygame.draw.line(
                screen, (200, 160, 60), to_screen(a, camera_offset), to_screen(b, camera_offset), 5
            )

        corners = [torso.local_to_world(v) for v in creature["shape"].get_vertices()]
        pygame.draw.polygon(screen, (80, 160, 230), [to_screen(c, camera_offset) for c in corners])

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    print("evolving creatures... (takes a few seconds)")
    best_genome, best_distance = run()
    print(f"\nbest distance traveled: {best_distance:.1f}")
    print("opening a window to show it walking...")
    render(best_genome)
