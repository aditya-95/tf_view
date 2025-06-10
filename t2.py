import tf_view
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
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


fig.subplots_adjust(left=0.1, bottom=0.30)
ax_slider1 = fig.add_axes((0.1, 0.1, 0.8, 0.01))
ax_slider2 = fig.add_axes((0.1, 0.2, 0.8, 0.01))

base_slider = Slider(ax_slider1, 'base', -np.pi, np.pi, valinit=0.0)
l1_slider = Slider(ax_slider2, 'l1', -np.pi, np.pi, valinit=np.pi/2)

chain.draw(ax)

def update_base(val):
    base.orientation = np.array([0, 0, val])
    chain.update()

    ax.cla()
    ax.set_xlim([0, 5])
    ax.set_ylim([5, 0])
    ax.set_zlim([0, 5])
    
    chain.draw(ax)

    fig.canvas.draw_idle()

def update_l1(val):
    l1.orientation = np.array([0, val, 0])
    chain.update()

    ax.cla()
    ax.set_xlim([0, 5])
    ax.set_ylim([5, 0])
    ax.set_zlim([0, 5])
    
    chain.draw(ax)

    fig.canvas.draw_idle()

base_slider.on_changed(update_base)
l1_slider.on_changed(update_l1)

plt.show()