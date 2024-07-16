import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



def transform_shape(shape, scale, orientation, position):
    # input: collection of points (n, 2)
    # original be centered at origin ?

    # Scale the shape
    scaled_shape = shape * scale

    # Rotate the shape
    rotation_matrix = np.array([
        [np.cos(orientation), -np.sin(orientation)],
        [np.sin(orientation), np.cos(orientation)]
    ])
    rotated_shape = np.dot(scaled_shape, rotation_matrix)

    # Translate the shape
    translated_shape = rotated_shape + position

    return translated_shape


def base_line(n_points=13):
    # 13 points including start, end
    line = np.column_stack(
        (
            np.linspace(-1, 1, n_points, endpoint=True), 
            np.zeros(n_points)
        )
    )
    line = line * 0.25
    return line

def base_circle(n_points=13):
    # 13 points including with START=END
    angles = np.linspace(0, 2 * np.pi, n_points, endpoint=True)
    circle = np.column_stack((np.cos(angles), np.sin(angles)))
    circle = circle * 0.25
    return circle

def gen_line(direction, rotation, position, n_points=13):
    # direction: 'forward' or 'backward'
    # rotation: 0 to 2*pi
    # position: position of midpoint - (0.25,0,25) - (0.75,0.75)

    base_l = base_line(n_points) # (n_points, 2)
    if direction == 'backward':
        line = base_l[::-1]
    else:    
        line = base_l
    
    line = transform_shape(line, 1, rotation, position)
    return line # (n_points, 2)

def gen_circle(direction, scale, position, n_points=13):
    # direction: 'ACW' or 'CW'
    # scale: 0.5 to 1
    # position: position of center - (0.25,0,25) - (0.75,0.75)

    base_c = base_circle(n_points) # (n_points, 2)
    if direction == 'CW':
        circle = base_c[::-1]
    else:    
        circle = base_c
    
    circle = transform_shape(circle, scale, 0, position)
    return circle # (n_points, 2)

def gen_stationary(point, n_points=13):
    # point: (2,)
    # repeat it n_points times
    pt = point.reshape(1,2)
    return np.repeat(pt, n_points, axis=0) #(n_points, 2)



def make_frame_wise(dot_wise):
    # for one data point
    # dot_wise: (4, n_points, 2)
    # return frame_wise: (n_points, 4, 2)
    return np.transpose(dot_wise, (1, 0, 2))


def gen_class(class_chara, n):
    # class_chara : list eg-[1,1,1,1]
    # 0=stationary, 1=line, 2=circle

    # for both line, circle
    min_pos = np.array([0.25, 0.25])
    max_pos = np.array([0.75, 0.75])

    min_scale, max_scale = 0.5, 1 # for circle

    # for stationary point
    min_pos_s = np.array([0, 0])
    max_pos_s = np.array([1, 1])

    data_pts = []
    for d in range(n):
        moving_dots = []
        for dot_chara in class_chara:
            if dot_chara==0:
                # genreate random stationary moving dot, add
                pt = np.random.uniform(min_pos_s, max_pos_s) #(2,)
                stationary = gen_stationary(pt)
                moving_dots.append(stationary)
            elif dot_chara==1:
                # generate random line moving dot, add
                direction = np.random.choice(['forward', 'backward'])
                rotation = np.random.uniform(0, 2 * np.pi)
                position = np.random.uniform(min_pos, max_pos)
                line = gen_line(direction, rotation, position)
                moving_dots.append(line)
            elif dot_chara==2:
                # generate random circle moving dot, add
                direction = np.random.choice(['ACW', 'CW'])
                scale = np.random.uniform(min_scale, max_scale)
                position = np.random.uniform(min_pos, max_pos)
                circle = gen_circle(direction, scale, position)
                moving_dots.append(circle)
        
        # (4,13,2) -> (13,4,2)
        moving_dots = make_frame_wise(np.array(moving_dots))
        data_pts.append(moving_dots)

    return np.array(data_pts) # (n,13,4,2)





# plot moving dots
def plot_moving_dots(moving_dots, ax):
    # different color to different dot
    # moving_dots: (n_points=n_frames, 4=n_dots, 2)
    colors = ['red', 'green', 'blue', 'yellow']
    for f in range(moving_dots.shape[0]): # each frame
        dots = moving_dots[f]
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.scatter(dots[:, 0], dots[:, 1], c=colors)
        # plt.show()
    



def plot_dots(dots, ax):
    # dots: (n_dots, 2) ndarray
    # plot in the passed axis
    ax.scatter(dots[:, 0], dots[:, 1], color='blue')

    # Label each point with its index
    for i, point in enumerate(dots):
        ax.text(point[0], point[1], str(i), fontsize=12, ha='right')

    # plt.show()


def animate_moving_dots(MD):
    # MD: (13,4,2)
    # animate one data-point
    fig, ax = plt.subplots()
    colors = ['red', 'green', 'blue', 'yellow']
    n_frames = MD.shape[0]
    for f in range(n_frames): # each frame
        dots = MD[f]
        # ax.clear()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.scatter(dots[:, 0], dots[:, 1], c=colors)
        plt.pause(0.2)
    plt.show()

    

###########################################################
# Test
# MD = gen_class( [0,2,2,0], 1 )[0]
# animate_moving_dots(MD)