import pygame
import numpy as np

#initialize pygame
pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("BEHOLD!")

vertices = np.array([
    [-1,-1,-1],
    [1,-1,-1],
    [1,1,-1], 
    [-1,1,-1],
    [-1,-1,1],
    [1,-1,1],
    [1,1,1],
    [-1,1,1]
])

#vertices that define the edges of the cube
edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)   
]

#rotation matrix for the x axis
def rotate_x(angle):
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)
    return np.array([
        [1, 0, 0],
        [0, cos_angle, -sin_angle],
        [0, sin_angle, cos_angle]
    ])

#rotation matrix for the y axis
def rotate_y(angle):
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)
    return np.array([
        [cos_angle, 0, sin_angle],
        [0, 1, 0],
        [-sin_angle, 0, sin_angle]
    ])

#rotation matrix for the z axis
def rotate_z(angle):
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)
    return np.array([
        [cos_angle, -sin_angle, 0],
        [sin_angle, cos_angle, 0],
        [0, 0, 1]
    ])

#convert 2d points to 3d points and returning and projecting 3d as 2d points
def project(points):
    scale = 100                         # scale for conversion b/w dimensions
    projection_matrix = np.array([      #matrix to discard the z axis
        [1,0,0],
        [0,1,0]
    ])

    projected_points = []
    for point in points:
        projected_point = np.dot(projection_matrix,point)
        x = int(projected_point[0] * scale) + width //2
        y = int(projected_point[1] * scale) + height //2
        projected_points.append((x,y))
    
    return projected_points
    
def main():
    clock = pygame.time.Clock()        #manage frame rate using pygame
    angle_x = angle_y = angle_z = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    angle_x += 0.1
                elif event.key == pygame.K_y:
                    angle_y += 0.1
                elif event.key == pygame.K_z:
                    angle_z += 0.1

        screen.fill((0,0,0))

        rotation_matrix = np.dot(rotate_x(angle_x), np.dot(rotate_y(angle_y), rotate_z(angle_z)))  #multiplying the idivisual matrices to compute overall rotation matrix
        rotated_vertices = np.dot(vertices, rotation_matrix)
        projected_vertices = project(rotated_vertices)    #projecting the rotated matrices to 2D

        for edge in edges:
            pygame.draw.line(screen, (0,255,0), projected_vertices[edge[0]], projected_vertices[edge[1]],1)
            pygame.display.flip()
            clock.tick(1000)  #60 fps

    pygame.quit()

if __name__ == "__main__":
    main()
