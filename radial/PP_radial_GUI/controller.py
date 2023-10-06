import main

if __name__ == "__main__":
	print("main.py should be started instead")
	exit()

import numpy as np
import threading
import time

import maths
import view

# For mouse precision (also dictates how close the sides of the potential can be)
relative_epsilon = 0.02
in_range = ""
epsilon_x = (maths.x_max - maths.x_min) * relative_epsilon
epsilon_E = (maths.E_max - maths.E_min) * relative_epsilon
starting_x = 0

# For playing
playing = False
time_speed = 0.005


def update_textbox(textbox, value):
	""" Updates the value in a textbox """
	textbox.delete(0, view.tk.END)
	textbox.insert(0, value)


# Value updates

def update_v_barrier(value):
	""" Updates the potential barrier value """
	maths.V_barrier = float(value)
	view.V_barrier_slider.set(maths.V_barrier)
	update_textbox(view.V_barrier_textbox, round(maths.V_barrier, 3))
	update_potential()


def update_barrier_end(value):
	""" Updates the end of the potential barrier """
	if float(value) > maths.barrier_start + 2*epsilon_x:
		maths.barrier_end = float(value)
	else:
		maths.barrier_end = maths.barrier_start + 2*epsilon_x
	view.barrier_end_slider.set(maths.barrier_end)
	update_textbox(view.barrier_end_textbox, round(maths.barrier_end, 3))
	update_potential()


def update_a(value):
	""" Updates the gaussian distribution factor """
	maths.a = float(value)
	view.gaussian_slider.set(maths.a)
	update_textbox(view.gaussian_textbox, round(maths.a, 3))
	update_potential()
	update_wave_function()
	view.plt.draw()
	view.canvas.draw()


def update_e(value):
	""" Updates the energy """
	if float(value) < maths.E_min:
		value = maths.E_min
	maths.E = float(value)
	view.E_slider.set(maths.E)
	update_textbox(view.E_textbox, round(maths.E, 7))
	update_energy()


def update_t(value):
	""" Updates time """
	maths.t = float(value)
	view.t_slider.set(maths.t)
	update_textbox(view.t_textbox, round(maths.t, 3))
	update_energy()


# Update values from a different textboxes
def update_e_from_tb(event):
	update_e(good_value(view.E_textbox.get(), maths.E))


def update_v_barrier_from_tb(event):
	update_v_barrier(good_value(view.V_barrier_textbox.get(), maths.V_barrier))


def update_barrier_end_from_tb(event):
	update_barrier_end(good_value(view.barrier_end_textbox.get(), maths.barrier_end))


def update_a_from_tb(event):
	update_a(good_value(view.gaussian_textbox.get(), maths.a))


def update_t_from_tb(event):
	update_t(good_value(view.t_textbox.get(), maths.t))


def good_value(value, old_value):
	""" Checks if the value is actually a number, if not returns the previous one"""
	try:
		float(value)
		return float(value)
	except ValueError:
		return old_value


def reset_values():
	""" Resets to initial values """

	maths.l = maths.default_l
	view.l_var.set(maths.l)
	
	maths.V_barrier = maths.default_V_barrier
	view.V_barrier_slider.set(maths.V_barrier)
	update_textbox(view.V_barrier_textbox, round(maths.V_barrier, 3))

	maths.barrier_end = maths.default_barrier_end
	view.barrier_end_slider.set(maths.barrier_end)
	update_textbox(view.barrier_end_textbox, round(maths.barrier_end, 3))

	maths.E = maths.default_E
	view.E_slider.set(maths.E)
	update_textbox(view.E_textbox, round(maths.E, 4))

	maths.a = maths.default_a
	view.gaussian_slider.set(maths.a)
	update_textbox(view.gaussian_textbox, round(maths.a, 3))

	maths.calculate_energy()
	maths.calculate_potential()
	maths.calculate_effective_potential()
	view.energy_plt.set_data(maths.energy[0], maths.energy[1])
	update_potential()
	update_wave_function()
	view.plt.draw()
	view.canvas.draw()


def change_l():
	maths.l = view.l_var.get()
	update_potential()
	update_wave_function()
	view.plt.draw()
	view.canvas.draw()


def update_potential():
	""" Updates the value of the potential and refreshes the view """
	maths.calculate_potential()
	view.potential_plt.set_data(maths.potential[0], maths.potential[1])
	maths.calculate_effective_potential()
	view.effective_potential_plt.set_data(maths.effective_potential[0], maths.effective_potential[1])
	update_wave_function()
	view.plt.draw()
	view.canvas.draw()


def update_energy():
	""" Updates the value of the energy and refreshes the view """
	maths.calculate_energy()
	view.energy_plt.set_data(maths.energy[0], maths.energy[1])
	update_wave_function()
	view.plt.draw()
	view.canvas.draw()


def update_wave_function():
	""" Updates the wave function """
	maths.calculate_wave_function()
	view.ax2.set_ylim(maths.psi_min, maths.psi_max)
	if view.show_abs.get():
		view.wave_function_abs.set_data(maths.psi[0], np.absolute(maths.psi[1]))
	if view.show_real.get():
		view.wave_function_real.set_data(maths.psi[0], np.real(maths.psi[1]))
	if view.show_imaginary.get():
		view.wave_function_imaginary.set_data(maths.psi[0], np.imag(maths.psi[1]))
	if view.show_color_mesh.get():
		view.wave_function_color_mesh.remove()
		view.plot_color_mesh(maths.psi)


def change_wave_type():
	maths.wave_packet = view.wave_packet_bool.get()
	if maths.wave_packet:
		view.gaussian_slider.configure(state="normal")
		view.gaussian_textbox.configure(state="normal")
	else:
		view.gaussian_slider.configure(state="disabled")
		view.gaussian_textbox.configure(state="disabled")
	update_wave_function()
	view.plt.draw()
	view.canvas.draw()


# Play/pause
def play():
	while playing:
		view.t_slider.set(maths.t + time_speed)
		if maths.t >= maths.t_max:
			stop()
			return
		time.sleep(0.02)


def play_pause():
	global playing
	if not playing:
		playing = True
		view.t_play_pause.configure(text=view.pause_icon)
		threading.Thread(target=play).start()
	else:
		playing = False
		view.t_play_pause.configure(text=view.play_icon)


def stop():
	global playing
	playing = False
	view.t_play_pause.configure(text=view.play_icon)
	update_t(maths.t_min)


# Plot interaction handling
def button_press_callback(event):
	""" Detects clicks and checks if in range of an editable plot """
	global in_range, starting_x

	if event.inaxes:
		if maths.barrier_start <= event.xdata <= maths.barrier_end and maths.V_barrier - epsilon_E <= event.ydata <= maths.V_barrier + epsilon_E:
			in_range = "V_barrier"
		elif maths.barrier_end - epsilon_x <= event.xdata <= maths.barrier_end + epsilon_x and min([maths.V_barrier, maths.V_1]) <= event.ydata <= max([maths.V_barrier, maths.V_1]):
			in_range = "barrier_end"
		elif maths.E - epsilon_E <= event.ydata <= maths.E + epsilon_E:
			in_range = "E"
		else:
			in_range = ""

	else:
		in_range = ""


def button_release_callback(event):
	""" Detects click release and removes any interaction with the plot """
	global in_range
	in_range = ""


def motion_notify_callback(event):
	""" Detects movement while clicking and updates the corresponding values """
	global in_range, starting_x

	if event.button and event.inaxes:
		if in_range == "V_barrier":
			update_v_barrier(event.ydata)
		elif in_range == "barrier_end":
			update_barrier_end(event.xdata)
		elif in_range == "E":
			update_e(event.ydata)


def initialise():
	view.initialise()
