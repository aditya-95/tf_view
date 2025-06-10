from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from typing import Optional, List, Union

class Frame:
    def __init__(self, name:str, orientation:np.ndarray, position:np.ndarray, parent:Frame=None):
        self.name = name
        self.orientation = orientation
        self.position = position
        self.rotation_matrix = self.calculate_rotation_mat()
        self.children:list[Frame] = []
        self.parent = parent
        
        # frame transform
        self.tf = np.eye(4)
        self.tf[0:3, 0:3] = self.rotation_matrix 
        self.tf[0:3, 3] = self.position

        if parent:
            parent.add_child(self)

    def add_child(self, child:Frame):
        self.children.append(child)

    def print_tree(self):
        print(self.name)
        for child in self.children:
            child.print_tree()
    
    def update(self):
        self.rotation_matrix = self.calculate_rotation_mat()
        self.tf[0:3, 0:3] = self.rotation_matrix

    def calculate_rotation_mat(self) -> np.ndarray:
        # euler angles for rotation
        alpha   = self.orientation[2]   # yaw
        beta    = self.orientation[1]   # pitch
        gamma   = self.orientation[0]   # roll

        # from 'introduction to robotics' by John J. Craig
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
        ux = self.rotation_matrix[0:3, 0]
        uy = self.rotation_matrix[0:3, 1]
        uz = self.rotation_matrix[0:3, 2]

        if show_frame:
            ax.quiver(p[0], p[1], p[2], ux[0], ux[1], ux[2], color='r')
            ax.quiver(p[0], p[1], p[2], uy[0], uy[1], uy[2], color='g')
            ax.quiver(p[0], p[1], p[2], uz[0], uz[1], uz[2], color='b')
            ax.scatter(p[0], p[1], p[2], color='k', s=20)
        else:
            ax.scatter(p[0], p[1], p[2], color='k', s=20)


class Chain:
    def __init__(self, root_frame:Frame):
        self.root = root_frame
        self.transforms = self.get_paths()

    def get_paths(self):
        paths = []
        
        def dfs(node:Frame, path):
            if not node:
                return

            path.append(node)

            if not node.children:
                paths.append(path[:])
            else:
                for child in node.children:
                    dfs(child, path)
            path.pop()
        
        dfs(self.root, [])
        return paths
    
    def draw(self, ax:Axes3D, show_frames=True):
        transforms = self.transforms

        for path in transforms:
            t = np.eye(4)
            x = []
            y = []
            z = []
            for frame in path:
                t = t @ frame.tf
                frame.rotation_matrix = t[0:3, 0:3]
                frame.position = t[0:3, 3]
                plt.gca().set_aspect('equal', adjustable='box')
                frame.draw(ax, show_frames)
                x.append(frame.position[0])
                y.append(frame.position[1])
                z.append(frame.position[2])

            points = np.array([x, y, z]).T.reshape(-1, 1, 3)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            colors = ['#e8a730', '#008080', '#8B4513', '#BDB76B', '#708090']

            lc = Line3DCollection(segments, colors=colors, linewidth=7, alpha=0.8)
            ax.add_collection3d(lc)

    def update(self):
        self.transforms = self.get_paths()
        for chain in self.transforms:
            for frame in chain:
                frame.update()