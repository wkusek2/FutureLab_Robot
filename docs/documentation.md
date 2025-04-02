# Dokumentacja funkcji i metod programu

## Spis treści

1. [App](#app)
	- [App module](#app-module)
	- [UI](#ui)
	- [Plot](#plot)
2. [Robot](#robot)
3. [Communicator](#com)
4. [Driver](#driver)
	- [Driver module](#driver-module)
	- [Servo module](#servo-module)
5. [Camera](#camera)
	- [Camera module](#camera-module)
	- [Utils](#utils)

---

## 1. App
<a name="app"></a>

Główna część programu, zawiera GUI oraz obiekty służące do przeliczania pozycji robota oraz wizualizacji jego ustawienia. 

Docelowo interfejs użytkownika (widok z kamer, panel sterowania) wyświetlany będzie po stronie usera, natomiast wszystkie obliczenia wykonywane będą po stronie Jetsona.


### 1.1 App module
<a name="app-module"></a>

Importuje biblioteki tk oraz ctk w celu utworzenia interfejsu - docelowo znajdzie się w osobnym module do uruchomienia po stronie usera.

- `gui`

- `run`

- `update_robot`

- `refresh_connection`

	- `refresh_connection_esp32`

	- `refresh_connection_arduino`

- `update_table`

	- `update_display`

- `on_combobox_select`

- `refresh_com_ports`

- `on_combobox_select_arduino`

- `refresh_arduino_ports`

- `thetas_to_0`

- `event_handler`


### 1.2 UI
<a name="ui"></a>


### 1.3 Plot
<a name="plot"></a>



## 2. Robot
<a name="robot"></a>



## 3. Communicator
<a name="com"></a>



## 4. Driver
<a name="driver"></a>


### 4.1 Driver module
<a name="driver-module"></a>


### 4.2 Servo module
<a name="servo-module"></a>



## 5. Camera
<a name="camera"></a>


### 5.1 Camera module
<a name="camera-module"></a>

### 5.2 Utils
<a name="utils"></a>

