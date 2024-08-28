import tkinter as tk
from pymodbus.client import ModbusTcpClient

# Глобальний клієнт для контролера
modbus_client = None

# Функція для встановлення з'єднання з контролером
def connect_to_controller():
    global modbus_client
    ip_address = ip_entry.get()
    port_number = int(port_entry.get())  # Змінив назву змінної на port_number

    try:
        modbus_client = ModbusTcpClient(ip_address, port=port_number)
        connection = modbus_client.connect()

        if connection:
            status_label.config(text="Підключено", fg="green")
        else:
            status_label.config(text="Не вдалося підключитися", fg="red")
    except Exception as e:
        status_label.config(text=f"Помилка: {str(e)}", fg="red")

# Функція для зчитування даних з контролера
def read_variable():
    if modbus_client is None or not modbus_client.is_socket_open():
        result_label.config(text="Немає з'єднання з контролером")
        return

    variable_address = int(variable_entry.get())

    try:
        response = modbus_client.read_holding_registers(variable_address, 1)
        if response.isError():
            result_label.config(text="Помилка зчитування")
        else:
            result_label.config(text=f"Значення: {response.registers[0]}")
    except Exception as e:
        result_label.config(text=f"Помилка: {str(e)}")

# Створення вікна
root = tk.Tk()
root.title("Зчитувач змінних з Eaton XC-303")

# Поля для вводу IP, порта, адреси змінної
tk.Label(root, text="IP-адреса").grid(row=0, column=0)
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1)

tk.Label(root, text="Порт").grid(row=1, column=0)
port_entry = tk.Entry(root)
port_entry.grid(row=1, column=1)

tk.Label(root, text="Адреса змінної").grid(row=2, column=0)
variable_entry = tk.Entry(root)
variable_entry.grid(row=2, column=1)

# Кнопка для з'єднання з контролером
connect_button = tk.Button(root, text="Підключитися", command=connect_to_controller)
connect_button.grid(row=3, column=0, columnspan=2)

# Індикатор статусу з'єднання
status_label = tk.Label(root, text="Не підключено", fg="red")
status_label.grid(row=4, column=0, columnspan=2)

# Кнопка для зчитування змінної
read_button = tk.Button(root, text="Зчитати", command=read_variable)
read_button.grid(row=5, column=0, columnspan=2)

# Поле для виводу результату
result_label = tk.Label(root, text="")
result_label.grid(row=6, column=0, columnspan=2)

# Запуск інтерфейсу
root.mainloop()