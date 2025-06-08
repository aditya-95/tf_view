import tf_view
import importlib; importlib.reload(tf_view)
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

f1 = tf_view.Frame('f1', np.array([0, 0, np.pi/4]), np.array([0, 0, 0]))
f2 = tf_view.Frame('f2', np.array([0, 0, 0]), np.array([2, 0, 2]))
f3 = tf_view.Frame('f3', np.array([0, 0, 0]), np.array([2, 0, 0]))
f4 = tf_view.Frame('f4', np.array([0, 0, 0]), np.array([2, 0, 0]))
f5 = tf_view.Frame('f5', np.array([0, 0, 0]), np.array([2, 0, 0]))

chain = tf_view.Chain('robot')
chain.add_frame(f1)
chain.add_frame(f2)
chain.add_frame(f3)
chain.add_frame(f4)
chain.add_frame(f5)

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([0, 10])
ax.set_ylim([10, 0])
ax.set_zlim([0, 10])
ax.plot

chain.draw(ax)
plt.show()