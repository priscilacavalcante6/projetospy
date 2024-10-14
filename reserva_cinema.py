import threading
import time

class Cinema:
    def __init__(self, filas, colunas):
        self.assentos = [[0 for _ in range(colunas)] for _ in range(filas)]  # 0 = disponível, 1 = reservado
        self.lock = threading.Lock()

    # Função para exibir o estado atual dos assentos
    def exibir_assentos(self):
        for linha in self.assentos:
            print(" ".join(map(str, linha)))
        print()

    # Função para reservar um assento
    def reservar_assento(self, fila, coluna):
        with self.lock:
            if self.assentos[fila][coluna] == 0:  # Assento disponível
                print(f"Assento [{fila + 1}, {coluna + 1}] reservado com sucesso!")
                self.assentos[fila][coluna] = 1
                return True
            else:
                print(f"Assento [{fila + 1}, {coluna + 1}] já está reservado.")
                return False

# Simulação de clientes tentando reservar assentos simultaneamente
def cliente_reservando(cinema, fila, coluna):
    cinema.reservar_assento(fila, coluna)

# Exemplo de uso
cinema = Cinema(5, 5)  # Cinema com 5 filas e 5 colunas de assentos

# Exibir assentos disponíveis inicialmente
cinema.exibir_assentos()

# Clientes tentando reservar assentos
clientes = []
for i in range(3):  # Simulando 3 clientes tentando reservar o mesmo assento
    t = threading.Thread(target=cliente_reservando, args=(cinema, 2, 3))  # Tentando reservar o assento [3, 4]
    clientes.append(t)
    t.start()

# Esperar que todas as threads terminem
for cliente in clientes:
    cliente.join()

# Exibir o estado dos assentos após as reservas
cinema.exibir_assentos()
