if __name__ == "__main__":
	print("main.py should be started instead")
	exit()


import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import maths
import controller

play_icon = "⏵"
pause_icon = "⏸"


# Create window
window = tk.Tk()
window.title("PP GUI")
window.iconbitmap("")
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", exit)
left_frame = tk.Frame()
left_frame.pack(side=tk.LEFT)
right_frame = tk.Frame()
right_frame.pack(side=tk.RIGHT, padx=10, anchor=tk.N)
time_control_frame = tk.Frame(left_frame)
time_control_frame.pack(side=tk.BOTTOM, padx=5, pady=2, fill=tk.X)
time_control_frame.columnconfigure(3, weight=1)


# Create figure
figure = plt.Figure(figsize=(8, 4.5))

# Add figure to window
canvas = FigureCanvasTkAgg(figure, left_frame)
canvas.get_tk_widget().pack(side=tk.TOP)

# Create and initialise plots
ax = figure.add_subplot(111)
ax.set_xlim(maths.x_min, maths.x_max)
ax.set_ylim(maths.E_min, maths.E_max)
ax.set_ylabel('Energy (eV)')
ax.set_xlabel('Position (nm)')
ax.set_facecolor((1, 1, 1, 0))

ax2 = ax.twinx()
ax2.set_ylim(maths.psi_min, maths.psi_max)
ax2.set_ylabel('Wave function')
ax2.set_zorder(-1)

maths.calculate_energy()
energy_plt, = ax.plot(maths.energy[0], maths.energy[1], 'g--', linewidth=1, label="Energy")

maths.calculate_potential()
potential_plt, = ax.plot(maths.potential[0], maths.potential[1], 'b', linewidth=1, label="Potential")

maths.calculate_wave_function()
show_abs = tk.BooleanVar(value=False)
wave_function_abs = None
show_real = tk.BooleanVar(value=True)
wave_function_real = None
show_imaginary = tk.BooleanVar(value=False)
wave_function_imaginary = None
show_color_mesh = tk.BooleanVar(value=False)
wave_function_color_mesh = None


def plot_wave_function_abs():
	global wave_function_abs
	if show_abs.get():
		wave_function_abs, = ax2.plot(maths.psi[0], np.absolute(maths.psi[1]), 'k', linewidth=1, label="Probability density")
	elif wave_function_abs is not None:
		wave_function_abs.remove()
	plt.draw()
	canvas.draw()


def plot_wave_function_real():
	global wave_function_real
	if show_real.get():
		wave_function_real, = ax2.plot(maths.psi[0], np.real(maths.psi[1]), 'r', linewidth=.5, label="Real part")
	elif wave_function_real is not None:
		wave_function_real.remove()
	plt.draw()
	canvas.draw()


def plot_wave_function_imaginary():
	global  wave_function_imaginary
	if show_imaginary.get():
		wave_function_imaginary, = ax2.plot(maths.psi[0], np.imag(maths.psi[1]), 'b', linewidth=.5, label="Imaginary part")
	elif wave_function_imaginary is not None:
		wave_function_imaginary.remove()
	plt.draw()
	canvas.draw()


def plot_color_mesh(psi=maths.psi):
	global wave_function_color_mesh
	if show_color_mesh.get():
		x_array = np.array([psi[0], psi[0]])

		y0 = np.zeros(len(psi[0]))
		y = [abs(i) for i in psi[1]]
		y_array = np.array([y0, y])

		psi_array = np.array([psi[1], psi[1]])
		angle = np.angle(psi_array)

		wave_function_color_mesh = ax2.pcolormesh(x_array, y_array, angle, cmap=plt.cm.hsv, vmin=-np.pi, vmax=np.pi)
	elif wave_function_color_mesh is not None:
		wave_function_color_mesh.remove()
	plt.draw()
	canvas.draw()


plot_wave_function_abs()
plot_wave_function_real()
plot_wave_function_imaginary()
plot_color_mesh(maths.psi)

ax.legend()
figure.tight_layout()

# Creating sliders
E_slider = tk.Scale(right_frame, from_=maths.E_limit, to=maths.E_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Energy (eV)", showvalue=0)
V_0_slider = tk.Scale(right_frame, from_=maths.E_min, to=maths.E_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Potential before barrier (eV)", showvalue=0)
V_barrier_slider = tk.Scale(right_frame, from_=maths.E_min, to=maths.E_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Barrier potential (eV)", showvalue=0)
V_1_slider = tk.Scale(right_frame, from_=maths.E_min, to=maths.E_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Potential after barrier (eV)", showvalue=0)
barrier_start_slider = tk.Scale(right_frame, state="disabled", from_=maths.x_min, to=maths.x_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Barrier start (nm) [disabled]", showvalue=0)
barrier_end_slider = tk.Scale(right_frame, from_=maths.x_min, to=maths.x_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Barrier end (nm)", showvalue=0)
wave_number_slider = tk.Scale(right_frame, from_=maths.k_0_min, to=maths.k_0_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Wave number", showvalue=0)
gaussian_slider = tk.Scale(right_frame, from_=maths.a_min, to=maths.a_max, resolution=0.01, orient=tk.HORIZONTAL, length=200, label="Gaussian distribution factor", showvalue=0)

# Creating text boxes
E_textbox = tk.Entry(right_frame, width=10)
V_0_textbox = tk.Entry(right_frame, width=10)
V_barrier_textbox = tk.Entry(right_frame, width=10)
V_1_textbox = tk.Entry(right_frame, width=10)
barrier_start_textbox = tk.Entry(right_frame, width=10, state="disabled")
barrier_end_textbox = tk.Entry(right_frame, width=10)
wave_number_textbox = tk.Entry(right_frame, width=10)
gaussian_textbox = tk.Entry(right_frame, width=10)

# Creating radio buttons
wave_packet_bool = tk.BooleanVar(value=maths.wave_packet)
plane_wave = tk.Radiobutton(right_frame, text="Plane wave", variable=wave_packet_bool, val=False)
wave_packet = tk.Radiobutton(right_frame, text="Wave packet", variable=wave_packet_bool, val=True)

# Creating reset button
reset_button = tk.Button(right_frame, text="Reset")

# Creating checkboxes
abs_checkbox = tk.Checkbutton(right_frame, text="Probability density", variable=show_abs, command=plot_wave_function_abs)
real_checkbox = tk.Checkbutton(right_frame, text="Real part", variable=show_real, command=plot_wave_function_real)
imaginary_checkbox = tk.Checkbutton(right_frame, text="Imaginary", variable=show_imaginary, command=plot_wave_function_imaginary)
color_mesh_checkbox = tk.Checkbutton(right_frame, text="Phase colours", variable=show_color_mesh, command=plot_color_mesh)

# Time controls
t_label = tk.Label(time_control_frame, text="Time")
t_play_pause = tk.Button(time_control_frame, text=play_icon)
t_stop = tk.Button(time_control_frame, text="⏹")
t_slider = tk.Scale(time_control_frame, from_=maths.t_min, to=maths.t_max, resolution=0.01, orient=tk.HORIZONTAL, showvalue=0)
t_textbox = tk.Entry(time_control_frame, width=10)

# Adding all to view
t_label.grid(row=0, column=0)
t_play_pause.grid(row=0, column=1)
t_stop.grid(row=0, column=2)
t_slider.grid(row=0, column=3, sticky=tk.EW)
t_textbox.grid(row=0, column=4)

E_slider.grid(row=0, column=0)
E_textbox.grid(row=0, column=1, sticky="sew")
V_0_slider.grid(row=1, column=0)
V_0_textbox.grid(row=1, column=1, sticky="sew")
V_barrier_slider.grid(row=2, column=0)
V_barrier_textbox.grid(row=2, column=1, sticky="sew")
V_1_slider.grid(row=3, column=0)
V_1_textbox.grid(row=3, column=1, sticky="sew")
barrier_start_slider.grid(row=4, column=0)
barrier_start_textbox.grid(row=4, column=1, sticky="sew")
barrier_end_slider.grid(row=5, column=0)
barrier_end_textbox.grid(row=5, column=1, sticky="sew")
wave_number_slider.grid(row=6, column=0)
wave_number_textbox.grid(row=6, column=1, sticky="sew")
gaussian_slider.grid(row=7, column=0)
gaussian_textbox.grid(row=7, column=1, sticky="sew")
reset_button.grid(row=8, column=1, sticky=tk.EW, pady=10)
plane_wave.grid(row=9, column=0, sticky=tk.W)
wave_packet.grid(row=10, column=0, sticky=tk.W)
real_checkbox.grid(row=11, column=0, sticky=tk.W)
imaginary_checkbox.grid(row=12, column=0, sticky=tk.W)
abs_checkbox.grid(row=11, column=1, sticky=tk.W)
color_mesh_checkbox.grid(row=12, column=1, sticky=tk.W)


def on_closing():
	controller.playing = False
	exit()


def initialise():
	# Bind plot actions with corresponding functions
	figure.canvas.mpl_connect('button_press_event', controller.button_press_callback)
	figure.canvas.mpl_connect('button_release_event', controller.button_release_callback)
	figure.canvas.mpl_connect('motion_notify_event', controller.motion_notify_callback)

	# Binding command to sliders
	E_slider.configure(command=controller.update_e)
	V_0_slider.configure(command=controller.update_v_0)
	V_barrier_slider.configure(command=controller.update_v_barrier)
	V_1_slider.configure(command=controller.update_v_1)
	barrier_start_slider.configure(command=controller.update_barrier_start)
	barrier_end_slider.configure(command=controller.update_barrier_end)
	wave_number_slider.configure(command=controller.update_wave_number)
	gaussian_slider.configure(command=controller.update_a)
	t_slider.configure(command=controller.update_t)

	# Binding button actions
	reset_button.configure(command=controller.reset_values)
	t_play_pause.configure(command=controller.play_pause)
	t_stop.configure(command=controller.stop)

	# Binding radio button actions
	plane_wave.configure(command=controller.change_wave_type)
	wave_packet.configure(command=controller.change_wave_type)

	# Binding textbox actions
	E_textbox.bind("<Return>", controller.update_e_from_tb)
	V_0_textbox.bind("<Return>", controller.update_v_0_from_tb)
	V_barrier_textbox.bind("<Return>", controller.update_v_barrier_from_tb)
	V_1_textbox.bind("<Return>", controller.update_v_1_from_tb)
	barrier_start_textbox.bind("<Return>", controller.update_barrier_start_from_tb)
	barrier_end_textbox.bind("<Return>", controller.update_barrier_end_from_tb)
	wave_number_textbox.bind("<Return>", controller.update_wave_number_from_tb)
	gaussian_textbox.bind("<Return>", controller.update_a_from_tb)
	t_textbox.bind("<Return>", controller.update_t_from_tb)

	# Setting default values
	controller.update_textbox(E_textbox, maths.E)
	controller.update_textbox(V_0_textbox, maths.V_0)
	controller.update_textbox(V_barrier_textbox, maths.V_barrier)
	controller.update_textbox(V_1_textbox, maths.V_1)
	controller.update_textbox(barrier_start_textbox, maths.barrier_start)
	controller.update_textbox(barrier_end_textbox, maths.barrier_end)
	controller.update_textbox(wave_number_textbox, maths.k_0)
	controller.update_textbox(gaussian_textbox, maths.a)
	controller.update_textbox(t_textbox, maths.t)

	E_slider.set(maths.E)
	V_0_slider.set(maths.V_0)
	V_barrier_slider.set(maths.V_barrier)
	V_1_slider.set(maths.V_1)
	barrier_start_slider.set(maths.barrier_start)
	barrier_end_slider.set(maths.barrier_end)
	wave_number_slider.set(maths.k_0)
	gaussian_slider.set(maths.a)
	t_slider.set(maths.t)

	if maths.wave_packet:
		gaussian_slider.configure(state="normal")
		gaussian_textbox.configure(state="normal")
	else:
		gaussian_slider.configure(state="disabled")
		gaussian_textbox.configure(state="disabled")

	window.protocol("WM_DELETE_WINDOW", on_closing)

	window.mainloop()
