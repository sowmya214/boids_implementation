import tkinter
import random
import math
import time
import Boid


def initialise_canvas(window, screen_size):
    canvas = tkinter.Canvas(window, width=screen_size, height=screen_size)
    canvas.pack()
    window.resizable(False, False)
    return canvas


def create_boids(canvas, no_of_boids):
    list_of_boids = []
    for n in range(no_of_boids):
        boid = Boid.Boid("boid" + str(n))
        list_of_boids.append(boid)
        boid.draw_boid(canvas)
    return list_of_boids


def separation(nearest_neighbour, boid):
    # move 1: move away from nearest - separation
    # calculate angle between boid and nearest boid, then angle it in the opposite direction
    if nearest_neighbour is not None and boid.euclidean_distance(nearest_neighbour) < 35:
        if nearest_neighbour.x - boid.x == 0.0:
            angle = math.atan((nearest_neighbour.y - boid.y) / 0.0001)
        else:
            angle = math.atan((nearest_neighbour.y - boid.y) / (nearest_neighbour.x - boid.x))
        boid.angle -= angle


def alignment(neighbours, boid):
    # move 2: orient towards the neighbours - alignment
    # calculate average angle of neighbours and move in that direction
    average_neighbours_angle = 0.0
    if neighbours:
        for neighbour_boid in neighbours:
            average_neighbours_angle += neighbour_boid.angle
        average_neighbours_angle /= len(neighbours)
        boid.angle -= (average_neighbours_angle-boid.angle)/100.0
        boid.angle = average_neighbours_angle


def cohesion(neighbours, boid):
    # move 3: move together - cohesion
    if neighbours:
        avg_x = 0.0
        avg_y = 0.0
        for neighbour_boid in neighbours:
            avg_x += neighbour_boid.x
            avg_y += neighbour_boid.y
        avg_x /= len(neighbours)
        avg_y /= len(neighbours)
        if avg_x - boid.x == 0.0:
            angle = math.atan((avg_y - boid.y) / 0.00001)
        else:
            angle = math.atan((avg_y - boid.y) / (avg_x - boid.x))
        boid.angle -= angle / 20.0


def boid_behaviours(canvas, list_of_boids, screen_size):
    # find neighbours
    for boid in list_of_boids:
        neighbours = []
        for b in list_of_boids:
            # if b is nearby current boid, then it is a neighbour and make sure neighbor boid is not
            # current boid
            if boid.euclidean_distance(b) < 75 and (not boid.euclidean_distance(b) == 0):
                neighbours.append(b)
        nearest_neighbour = None
        # finding nearest neighbour
        if neighbours:
            shortest_distance = 999999999
            for neighbour_boid in neighbours:
                d = boid.euclidean_distance(neighbour_boid)
                if d < shortest_distance:
                    shortest_distance = d
                    nearest_neighbour = neighbour_boid

        separation(nearest_neighbour, boid)
        alignment(neighbours, boid)
        cohesion(neighbours, boid)

    for boid in list_of_boids:
        boid.flock(canvas, screen_size)
    canvas.after(100, boid_behaviours, canvas, list_of_boids, screen_size)


def main():
    screen_size = 1000
    no_of_boids = 100
    window = tkinter.Tk()
    canvas = initialise_canvas(window, screen_size)
    list_of_boids = create_boids(canvas, no_of_boids)
    boid_behaviours(canvas, list_of_boids, screen_size)
    window.mainloop()


main()
