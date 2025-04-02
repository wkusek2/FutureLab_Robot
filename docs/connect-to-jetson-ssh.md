## Przygotowanie do połączeń SSH

>*__UWAGA__* </br>
> Niesprecyzowanie klucza skutkuje koniecznością wpisania hasła do Orina przy każdorazowej próbie wykonania komendy `ssh` albo `scp`

W celu łączenia się z Jetsonem poprzez SSH dobrym sposobem jest logowanie przy użyciu zainstalowanego już na urządzeniu klucza prywatnego.
W tym celu należy plik [`utils/ssh/jetson-key`](../utils/ssh/jetson-key) przenieść do odpowiedniego katalogu w zależności od dystrubucji:

- ### Linux

  ```bash
  cp utils/ssh/jetson-key ~/.ssh/
  ```

- ### Windows

  ```cmd
  copy utils/ssh/jetson-key C:\Users\<NAZWA UŻYTKOWNIKA>\.ssh # ścieżka będzie potrzebna w innych skryptach
  ```

## Połączenie poprzez terminal

Po skopiowaniu pliku, w celu połączenia się poprzez SSH do Jetsona należy wpisać w terminalu:
```bash
ssh -i <ŚCIEŻKA/DO/KLUCZA> orin@192.168.55.1
# LINUX: ssh -i ~/.ssh/jetson-key orin@192.168.55.1
# WINDOWS: ssh -i C:\Users\<UŻYTKOWNIK>\.ssh\jetson-key orin@192.168.55.1
```

Można również wykorzystać przygotowany skrypt znajdujący się w repozytorium, który weryfikuje poprawne połączenie.
```bash
utils/connect-jetson.sh <ŚCIEŻKA/DO/KLUCZA>
```
