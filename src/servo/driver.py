import serial
import serial.tools.list_ports
import threading
import time

# Inicjalizacja zmiennych globalnych
speed = 150
acc = 150
arduino_baudrate = 9600
esp32_baudrate = 115200


class Driver:
    def __init__(self) -> None:
        self.running = True

        self.id = [1, 2, 3, 4, 5, 6]
        self.voltage = [1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
        self.current = [2.3, 2.4, 2.5, 2.6, 2.7, 3]
        self.temperature = [36.0, 37.0, 38.0, 39.0, 40.0, 40]
        self.positions = [120, 130, 140, 150, 160, 200]
        self.load = [1.5, 1.6, 1.7, 1.8, 1.9, 2]

        self.connection_status = None
        self.selected_port = ""
        self.arduino_port = "/dev/ttyCH341USB0"
        self.esp32_port = "/dev/ttyUSB0"
        self.ser_arduino = None
        self.ser_esp32 = None

        self.camera_left_pos = 45
        self.camera_right_pos = 35
        self.camera_left_max = False
        self.camera_right_max = False

        self.camera_step_delay = 0.02
        self.camera_step_size = 1

    def increase_camera(self, side_of_camera, dir):
        '''
        Used to move camera left or right
        '''
        if side_of_camera == "left":
            next_pos = self.camera_left_pos + dir
            if 0 < next_pos < 80:
                self.camera_left_pos = next_pos
            else:
                self.camera_left_max = True

        elif side_of_camera == "right":
            next_pos = self.camera_right_pos + dir
            if 0 < next_pos < 80:
                self.camera_right_pos = next_pos   
            else:
                self.camera_right_max = True        

        camera = {
            "left": 
            {
                "id": 2,
                "angle": self.camera_left_pos
            },

            "right": 
            {
                "id": 5,
                "angle": self.camera_right_pos
            }
        }

        self.move_camera(
            id_camera =         camera[side_of_camera]["id"], 
            target_position =   camera[side_of_camera]["angle"], 
            step_delay =        self.camera_step_delay,
            step_size =         self.camera_step_size
        )
        time.sleep(0.5)

    def reset_camera(self):
        '''
        Function will set camera to point downwards, freeze the program for about 12 seconds
        '''

        # ID:       ZAKRES:       PARA:
        #   2 UP/DOWN   0-80        LEWA
        #   3 ROTATION  0-140       LEWA
        #   4 ROTATION  0-180       PRAWA
        #   5 UP/DOWN   0-80        PRAWA
        camera_reset = {
            "left-up": {
                "id": 2,
                "angle": 10
            },

            "left-rotation": {
                "id": 9,
                "pos": 620,
                "speed": 150,
                "acc": 50
            },

            "right-rotation": {
                "id": 10,
                "pos": 320,
                "speed": 150,
                "acc": 50
            },

            "right-up": {
                "id": 5,
                "angle": 170
            }
        }

        self.move_camera_pitch(
            id_camera =         camera_reset["left-up"]["id"], 
            target_position =   camera_reset["left-up"]["angle"], 
            step_delay =        self.camera_step_delay,
            step_size =         self.camera_step_size
        )
        time.sleep(4)
        self.move_camera_pitch(
            id_camera =         camera_reset["right-up"]["id"], 
            target_position =   camera_reset["right-up"]["angle"], 
            step_delay =        self.camera_step_delay,
            step_size =         self.camera_step_size
        )
        time.sleep(4)
        self.move_camera_rotation(
            id_servo =         camera_reset["left-rotation"]["id"], 
            target_position =   camera_reset["left-rotation"]["pos"], 
            speed =        camera_reset["left-rotation"]["speed"],
            acc =         camera_reset["left-rotation"]["acc"],
        )
        time.sleep(1)
        self.move_camera_rotation(
            id_servo =         camera_reset["right-rotation"]["id"], 
            target_position =   camera_reset["right-rotation"]["pos"], 
            speed =        camera_reset["right-rotation"]["speed"],
            acc =         camera_reset["right-rotation"]["acc"],
        )     
        time.sleep(1)
        
        self.camera_left_pos = camera_reset["left-up"]["angle"]
        self.camera_right_pos = camera_reset["right-up"]["angle"]
        self.camera_left_max = False
        self.camera_right_max = False
    

    def move_camera_pitch(self, id_camera, target_position, step_delay, step_size):
        id_camera = int(id_camera)
        target_position = int(target_position)
        step_delay = float(step_delay)
        step_size = int(step_size)
        self.send_command_camera(f"{id_camera},{target_position},{step_delay},{step_size}")

    def move_camera_rotation(self, id_servo, target_position, speed, acc):
        id_servo = int(id_servo)
        target_position = int(target_position)
        speed = int(speed)
        acc = int(acc)
        self.send_command(f"{id_servo},{target_position},{speed},{acc}")

    def send_command_camera(self, ard_command):
        if self.ser_arduino is not None and self.ser_arduino.is_open:
            try:  
                full_command = f"*{ard_command}*"
                self.ser_arduino.write(full_command.encode('utf-8') + b'\n')
                print(f"Wysłano komendę: {full_command}")
            except serial.SerialException as e:
                print(f"Błąd wysyłania komendy: {e}")

    def send_command(self, command):
        if command and self.ser_esp32 is not None and self.ser_esp32.is_open:
            try:
                full_command = f"({command})"
                self.ser_esp32.write(full_command.encode('utf-8') + b'\n')
                print(f"Wysłano komendę: {full_command}")
            except serial.SerialException as e:
                print(f"Błąd wysyłania komendy: {e}")

    def connect_arduino(self):
        try:
            if self.ser_arduino is not None and self.ser_arduino.is_open:
                self.ser_arduino.close()
                print("Zresetowano połączenie z Arduino.")
            self.ser_arduino = serial.Serial(self.arduino_port, arduino_baudrate, timeout=1)
            print(f"Połączono z Arduino na porcie {self.arduino_port}")
            connection_status_arduino = 1
            self.running = True
            return connection_status_arduino
        except serial.SerialException as e:
            self.running = False
            print(f"Błąd połączenia: {e}")
            connection_status_arduino = 0
            return connection_status_arduino

    def connect_esp32(self):
        try:
            if self.ser_esp32 is not None and self.ser_esp32.is_open:
                self.ser_esp32.close()
                print("Zresetowano połączenie z ESP32.")
            self.ser_esp32 = serial.Serial(self.esp32_port, esp32_baudrate, timeout=1)
            print(f"Połączono z ESP32 na porcie {self.esp32_port}")
            connection_status_esp32 = 1
            self.running = True
            return connection_status_esp32
        except serial.SerialException as e:
            self.running = False
            print(f"Błąd połączenia: {e}")
            connection_status_esp32 = 0
            return connection_status_esp32

    def move(self, id, position):
        id = int(id)
        position = int(position)
        self.send_command(f"{id},{position},{speed},{acc}")
        self.positions[id - 1] = position

    def move_to_position(self, pos1, pos2, pos3, pos4, off_1, off_2, off_3, off_4):
        try:
            if(pos3 < 150 or pos3 > 2000):
                raise ValueError("Ruch poza zakresem")
            if(pos4 < 1024):
                raise ValueError("Ruch poza zakresem")
                self.move(1, (pos1 + off_1))
                self.move(2, (pos2 + off_2))
                self.move(3, (pos3 - off_3))
                self.move(4, (pos4 - off_4))
                self.move(5, (4096 - pos4 + off_4))

        except ValueError as e:
            print(f"Błąd konwersji współrzędnych lub punkt poza zasięgiem: {e}")

    def set_selected_port(self, port, device):
        self.selected_port = port
        if device == "arduino":
            self.arduino_port = port
        elif device == "esp32":
            self.esp32_port = port


    def receive_data(self, serial_connection, callback):
        buffer = ""
        while self.running:
            if serial_connection is not None and serial_connection.is_open and serial_connection.in_waiting > 0:
                try:
                    data = serial_connection.read(serial_connection.in_waiting).decode('utf-8')
                    buffer += data
                    while '<' in buffer and '>' in buffer:
                        start = buffer.index('<')
                        end = buffer.index('>')
                        message = buffer[start + 1:end]
                        buffer = buffer[end + 1:]

                        values = message.split(',')
                        if len(values) == 6:
                            try:
                                servo_id = int(values[0])
                                voltage = float(values[1])
                                current = float(values[2])
                                temperature = float(values[3])
                                pos = int(values[4])
                                load = float(values[5])
                                callback(servo_id, voltage, current, temperature, pos, load)
                            except ValueError as e:
                                print(f"Błąd konwersji danych: {e}")
                except serial.SerialException as e:
                    print(f"Błąd odczytu danych: {e}")

            time.sleep(0.1)


    def start_receive_data_thread(self, callback):
        self.running = True
        # arduino_thread = threading.Thread(target=lambda: self.receive_data(self.ser_arduino, callback), daemon=True)
        # esp32_thread = threading.Thread(target=lambda: self.receive_data(self.ser_esp32, callback), daemon=True)
        # arduino_thread.start()
        # esp32_thread.start()

    def stop_receiving(self):
        self.running = False

    def get_com_ports(self):
        ports = list(serial.tools.list_ports.comports())
        return [port.device for port in ports]

    def get_positions(self):
        return self.positions

    def get_selected_port(self):
        return self.selected_port

    def get_data(self):
        return self.id, self.voltage, self.current, self.temperature, self.positions, self.load

    def get_servo_pos(self):
        return [self.camera_left_pos, self.camera_right_pos]

#######################################
# def refresh_com_ports(com_ports_var, combobox):
#     com_ports = get_com_ports()
#     com_ports_var.set(com_ports)
#     combobox['values'] = com_ports
