import cv2
import inputs
import threading

class WebcamApp:

	def __init__(self):

		self.camera = cv2.VideoCapture(0)
		self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
		self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)


		if not self.camera.isOpened():
			raise Exception("Unable to open the camera!")

		self.is_running = True
		self.thread = threading.Thread(target=self.show_camera)
		self.thread.start()

		self.image_counter = 0
		self.controller = None

		# mapping misconfigured controller button names
		self.btn_a = "BTN_THUMB"
		self.btn_b = "BTN_THUMB2"
		self.btn_y = "BTN_TOP"
		self.btn_x = "BTN_TRIGGER"

		self.initialise_controller()

	def show_camera(self):

		cv2.namedWindow("Webcam Feed", cv2.WND_PROP_FULLSCREEN)

		while self.is_running:
			ret, frame = self.camera.read()
			if ret:
				cv2.imshow("Webcam Feed", frame)
				key = cv2.waitKey(1)
				if key == ord(" "):
					self.save_image()

		cv2.destroyAllWindows()

	def initialise_controller(self):

		try:
			self.controller = inputs.devices.gamepads[0]
		except IndexError:
			print("No game controller found!")

		self.check_controller_input() #Start checking for controller input!

	def save_image(self):

		ret, frame = self.camera.read()
		if ret:
			filename = f"./photos/captured_image_{self.image_counter}.jpg"
			cv2.imwrite(filename, frame)
			print(f"./photos/Image saved as {filename}")
			self.image_counter += 1

	def check_controller_input(self):

		if self.controller:
			events = self.controller.read()
			for event in events:
				if event.code == self.btn_a and event.state == 1:
					self.save_image()
				elif event.code == self.btn_b and event.state == 1:
					self.save_image()
				elif event.code == self.btn_x and event.state == 1:
					self.save_image()
				elif event.code == self.btn_y and event.state == 1:
					self.save_image()

		if self.is_running:
			threading.Timer(0.01, self.check_controller_input).start()

	def stop(self):

		self.is_running = False
		self.thread.join()
		self.camera.release()

if __name__ == "__main__":

	app = WebcamApp()
	app.check_controller_input() #Start checking for controller input!
