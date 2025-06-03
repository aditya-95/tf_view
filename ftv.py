import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from typing import Optional, List, Union

class Frame:
    def __init__(self, name:str, orientation:np.ndarray, position:np.ndarray):
        self.name = name
        self.orientation = orientation
        self.position = position
        self.rotation_matrix = self.calculate_rotation_mat()
        
    def calculate_rotation_mat(self) -> np.ndarray:
        alpha   = self.orientation[2]
        beta    = self.orientation[1]
        gamma   = self.orientation[0]

        r11 = np.cos(alpha) * np.cos(beta)
        r12 = (np.cos(alpha) * np.sin(beta) * np.sin(gamma)) - (np.sin(alpha) * np.cos(gamma))
        r13 = (np.cos(alpha) * np.sin(beta) * np.cos(gamma)) + (np.sin(alpha) * np.sin(gamma))

        r21 = np.sin(alpha) * np.cos(beta)
        r22 = (np.sin(alpha) * np.sin(beta) * np.sin(gamma)) + (np.cos(alpha) * np.cos(gamma))
        r23 = (np.sin(alpha) * np.sin(beta) * np.cos(gamma)) - (np.cos(alpha) * np.sin(gamma))

        r31 = -np.sin(beta)
        r32 = np.cos(beta) * np.sin(gamma)
        r33 = np.cos(beta) * np.cos(gamma)

        rotation_matrix = np.array([[r11, r12, r13],
                                    [r21, r22, r23],
                                    [r31, r32, r33]])
        return rotation_matrix
    
    def draw(self, ax:Axes3D, show_frame=True):
        p = self.position
        ux = self.rotation_matrix[0][:]
        uy = self.rotation_matrix[1][:]
        uz = self.rotation_matrix[2][:]

        if show_frame:
            ax.quiver(p[0], p[1], p[2], ux[0], ux[1], ux[2], color='r')
            ax.quiver(p[0], p[1], p[2], uy[0], uy[1], uy[2], color='g')
            ax.quiver(p[0], p[1], p[2], uz[0], uz[1], uz[2], color='b')
            ax.scatter(p[0], p[1], p[2], color='k', s=20)
        else:
            ax.scatter(p[0], p[1], p[2], color='k', s=20)

class Chain:
    def __init__(self, name: str):
        self.name = name
        self.chain = []
    
    def add_frame(self, frame:Frame):
        self.chain.append(frame)

    def draw(self, ax:Axes3D, show_frames=True):
        x = []
        y = []
        z = []

        temp_chain = self.chain
        T = np.eye(4)

        for frame in temp_chain:
            T_current = np.eye(4)
            T_current[0:3, 0:3] = frame.rotation_matrix
            T_current[0:3, 3] = frame.position

            T = T @ T_current
            frame.position = T[0:3, 3]
            frame.rotation_matrix = T[0:3, 0:3]

            frame.draw(ax, show_frames)
            x.append(frame.position[0])
            y.append(frame.position[1])
            z.append(frame.position[2])

        points = np.array([x, y, z]).T.reshape(-1, 1, 3)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        colors = ['orange', 'black']

        lc = Line3DCollection(segments, colors=colors, linewidth=5)
        ax.add_collection3d(lc)
    
    def get_transform_wrt_base(self) -> np.ndarray:
        T = np.eye(4)
        for i in range(len(self.chain)):
            T_next = np.eye(4)
            T_next[0:3, 0:3] = self.chain[i].rotation_matrix
            T_next[0:3, 3] = self.chain[i].position

            T = T @ T_next
        return T