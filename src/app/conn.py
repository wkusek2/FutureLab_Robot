import time

from src.servo.driver import Driver

class Communicator():
    def __init__(self) -> None:
        self.toggle = False
        self.driver = Driver()

    def get_servo_pos(self):
        return self.driver.get_servo_pos()

    def get_com_ports(self):
        return self.driver.get_com_ports()

    def get_positions(self):
        return self.driver.get_positions()

    def get_data(self):
        return self.driver.get_data()

    def set_selected_port(self, port, device):
        return self.driver.set_selected_port(port, device)

    def set_selected_port_arduino(self):
        pass



    def start_receive_data_thread(self, callback):
        self.driver.start_receive_data_thread(callback)

    def connect_esp32(self):
        return self.driver.connect_esp32()

    def connect_arduino(self):
        return self.driver.connect_arduino()



    def move(self, id, pos):
        self.driver.move(id, pos)

    def move_to_position(self, pos1, pos2, pos3, pos4, off_1, off_2, off_3, off_4):
        self.driver.move_to_position(pos1, pos2, pos3, pos4, off_1, off_2, off_3, off_4)



    def test(self, id_move_s, position_move_s):
        print("czesc")
        if(id_move_s.get() is None and position_move_s.get() is None):
            print("uzupełnij luke")
        else:
            self.move(int(id_move_s.get()),int(position_move_s.get()))

    def toggle_and_send_command(self, status_torque):
        self.toggle = not self.toggle
        if self.toggle:
            self.driver.send_command("T,1")
            status_torque.configure("Status: " + str(self.toggle))
        else:
            self.driver.send_command("T,0")
            status_torque.configure("Status: " + str(self.toggle))

    # def showcase_camera(self):
    #     self.driver.move_camera(1, 80)
    #     self.driver.move_camera(2, 0)
    #     self.driver.move_camera(3, 80)
    #     self.driver.move_camera(4, 0)
    #     time.sleep(2)
    #     self.driver.move_camera(1, 0)
    #     self.driver.move_camera(2, 150)
    #     self.driver.move_camera(3, 0)
    #     self.driver.move_camera(4, 150)
    #     time.sleep(2)

    # def transport_mode(self):
    #     self.driver.move(2, 2048)
    #     self.driver.move(3, 300)
    #     self.driver.move(4, 2048)
    #     self.driver.move(5, 2048)
    #     time.sleep(5)
    #     self.driver.move(1, 2160)
    #     time.sleep(5)
    #     self.driver.move(2, 3620)
    #     self.driver.move(3, 350)
    #     self.driver.move(4, 2048)
    #     self.driver.move(5, 2048)
