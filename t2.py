import tf_view
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

world = tf_view.Frame(name='world', orientation=np.array([0, 0, 0]), position=np.array([0, 0, 0]))
base = tf_view.Frame(name='base', orientation=np.array([0, 0, 0]), position=np.array([0, 0, 0]), parent=world)
l1 = tf_view.Frame(name='l1', orientation=np.array([0, np.pi/2, 0]), position=np.array([0, 0, 2]), parent=base)
l2 = tf_view.Frame(name='l2', orientation=np.array([0, 0, 0]), position=np.array([0, 0, 1.5]), parent=l1)
l3 = tf_view.Frame(name='l3', orientation=np.array([0, 0, 0]), position=np.array([0, 0, 0.5]), parent=l2)

chain = tf_view.Chain(world)

fig = plt.figure(figsize=(14, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([0, 5])
ax.set_ylim([5, 0])
ax.set_zlim([0, 5])
ax.plot

chain.draw(ax)
plt.show()