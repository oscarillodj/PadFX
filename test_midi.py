import mido

print("Dispositivos MIDI encontrados:")

for puerto in mido.get_input_names():
    print("-", puerto)


print("\nEsperando señal MIDI...")

puerto = mido.open_input(
    mido.get_input_names()[0]
)

for mensaje in puerto:
    print(mensaje)