import taichi as ti

ti.init(arch=ti.cpu)

# Simulation parameters
res = 100
width, height, depth = res, res, res
dx = 1.0 / res
pixels = ti.Vector.field(3, dtype=ti.uint8, shape=(width, height))
density = ti.field(dtype=ti.f32, shape=(width, height, depth))
velocity = ti.Vector.field(3, dtype=ti.f32, shape=(width, height, depth))
new_density = ti.field(dtype=ti.f32, shape=(width, height, depth))
new_velocity = ti.Vector.field(3, dtype=ti.f32, shape=(width, height, depth))

# Initialize GUI
gui = ti.GUI("Water Simulator", (width, height))

@ti.kernel
def initialize():
    for i, j, k in density:
        density[i, j, k] = 0.0
        new_density[i, j, k] = 0.0
        velocity[i, j, k] = ti.Vector([0.0, 0.0, 0.0])
        new_velocity[i, j, k] = ti.Vector([0.0, 0.0, 0.0])

@ti.kernel
def add_density(pos_x: ti.f32, pos_y: ti.f32, pos_z: ti.f32, amount: ti.f32):
    i, j, k = int(pos_x), int(pos_y), int(pos_z)
    new_density[i, j, k] += amount

@ti.kernel
def add_velocity(pos_x: ti.f32, pos_y: ti.f32, pos_z: ti.f32, amount: ti.template()):
    i, j, k = int(pos_x), int(pos_y), int(pos_z)
    new_velocity[i, j, k] += amount

@ti.kernel
def advect(field: ti.template(), new_field: ti.template(), velocity: ti.template()):
    for i, j, k in field:
        coord = ti.Vector([i, j, k]) - velocity[i, j, k]
        coord = ti.min(ti.max(coord, [0.5, 0.5, 0.5]), [width - 0.5, height - 0.5, depth - 0.5])
        i_f, j_f, k_f = coord  # Floating-point indices
        i0, j0, k0 = int(i_f), int(j_f), int(k_f)
        i1, j1, k1 = i0 + 1, j0 + 1, k0 + 1
        s, t, u = i_f - i0, j_f - j0, k_f - k0
        field[i, j, k] = (1 - s) * (1 - t) * (1 - u) * new_field[i0, j0, k0] + \
                         s * (1 - t) * (1 - u) * new_field[i1, j0, k0] + \
                         (1 - s) * t * (1 - u) * new_field[i0, j1, k0] + \
                         s * t * (1 - u) * new_field[i1, j1, k0] + \
                         (1 - s) * (1 - t) * u * new_field[i0, j0, k1] + \
                         s * (1 - t) * u * new_field[i1, j0, k1] + \
                         (1 - s) * t * u * new_field[i0, j1, k1] + \
                         s * t * u * new_field[i1, j1, k1]

@ti.kernel
def update():
    for i, j, k in density:
        velocity[i, j, k] = new_velocity[i, j, k]
        density[i, j, k] = new_density[i, j, k]

@ti.kernel
def render():
    for i, j, k in pixels:
        pixels[i, j] = [int(density[i, j, res // 2] * 255)] * 3

def main():
    initialize()

    while gui.running:
        for e in gui.get_events(ti.GUI.PRESS):
            if e.key == ti.GUI.ESCAPE:
                gui.running = False
            elif e.key == 'c':
                initialize()

        if gui.get_event(ti.GUI.LMB):
            mx, my = gui.event.pos
            add_density(mx, my, res // 2, 500.0)

        if gui.get_event(ti.GUI.RMB):
            mx, my = gui.event.pos
            add_velocity(mx, my, res // 2, ti.Vector([0.0, 10.0, 0.0]))

        advect(density, new_density, velocity)
        advect(velocity, new_velocity, velocity)
        update()
        render()

        gui.set_image(pixels.to_numpy())
        gui.show()

if __name__ == '__main__':
    main()
