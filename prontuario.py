class Prontuario:
    def __init__(self, paciente, diagnostico, tratamento, proximo=None):
        self.paciente = paciente
        self.diagnostico = diagnostico
        self.tratamento = tratamento
        self.proximo = proximo  # Aponta para o próximo prontuário

    def __repr__(self):
        return f"Paciente: {self.paciente}, Diagnóstico: {self.diagnostico}, Tratamento: {self.tratamento}"


class ListaEncadeadaProntuarios:
    def __init__(self):
        self.cabeca = None  # A cabeça da lista encadeada (o primeiro prontuário)

    def adicionar_prontuario(self, paciente, diagnostico, tratamento):
        # Cria um novo prontuário e o adiciona no início da lista
        novo_prontuario = Prontuario(paciente, diagnostico, tratamento, self.cabeca)
        self.cabeca = novo_prontuario

    def buscar_prontuario(self, nome_paciente):
        atual = self.cabeca
        # Percorre a lista encadeada até encontrar o paciente
        while atual:
            if atual.paciente == nome_paciente:
                return atual  # Retorna o prontuário se encontrado
            atual = atual.proximo  # Avança para o próximo prontuário
        return None  # Retorna None se o prontuário não for encontrado

    def __repr__(self):
        prontuarios = []
        atual = self.cabeca
        # Percorre a lista encadeada para exibir todos os prontuários
        while atual:
            prontuarios.append(repr(atual))
            atual = atual.proximo
        return "\n".join(prontuarios) if prontuarios else "Nenhum prontuário disponível."


# Uso da lista encadeada para gerenciar prontuários
sistema_prontuarios = ListaEncadeadaProntuarios()

# Adicionando prontuários
sistema_prontuarios.adicionar_prontuario("Alice Santos", "Diabetes Tipo 2", "Metformina")
sistema_prontuarios.adicionar_prontuario("João Silva", "Hipertensão", "Losartana")

# Adicionar mais prontuários conforme necessário
print("Prontuários adicionados:")
print(sistema_prontuarios)

# Buscando um prontuário
prontuario_alice = sistema_prontuarios.buscar_prontuario("Alice Santos")
if prontuario_alice:
    print("\nProntuário de Alice encontrado:")
    print(prontuario_alice)
else:
    print("\nProntuário de Alice não encontrado.")
