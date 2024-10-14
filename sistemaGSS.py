import heapq
import itertools

# Classe para gerenciar solicitações no centro de atendimento
class GerenciadorSolicitacoes:
    def __init__(self):
        self.contador = itertools.count()  # Para garantir a ordem FIFO das solicitações padrão
        self.fila_prioridade = []  # A lista que será usada como heap (fila de prioridade)

    # Método para adicionar uma solicitação
    def adicionar_solicitacao(self, demanda, tipo="padrão"):
        # Prioridade 1 para urgente e 2 para padrão
        prioridade = 1 if tipo == "urgente" else 2
        # A tupla armazenada no heap é (prioridade, tempo_chegada, demanda)
        # O contador gera um número único para garantir que a ordem seja mantida para solicitações de mesma prioridade
        heapq.heappush(self.fila_prioridade, (prioridade, next(self.contador), demanda))
        print(f"Solicitação '{demanda}' de tipo '{tipo}' adicionada à fila.")

    # Método para processar a próxima solicitação (remover da fila)
    def processar_solicitacao(self):
        if not self.fila_prioridade:
            print("Nenhuma solicitação para processar.")
            return
        # heapq.heappop remove e retorna o item com a menor prioridade (urgente primeiro)
        prioridade, _, demanda = heapq.heappop(self.fila_prioridade)
        tipo = "urgente" if prioridade == 1 else "padrão"
        print(f"Processando solicitação '{demanda}' de tipo '{tipo}'.")

    # Exibir o estado atual da fila
    def exibir_fila(self):
        if not self.fila_prioridade:
            print("Fila de solicitações está vazia.")
            return
        print("Fila atual de solicitações (por prioridade):")
        for prioridade, _, demanda in sorted(self.fila_prioridade):
            tipo = "urgente" if prioridade == 1 else "padrão"
            print(f"  - Solicitação '{demanda}', Tipo: '{tipo}'")

# Exemplo de uso do GerenciadorSolicitacoes
gerenciador = GerenciadorSolicitacoes()

# Adicionando algumas solicitações à fila
gerenciador.adicionar_solicitacao("Resolver problema de login", "padrão")
gerenciador.adicionar_solicitacao("Falha no sistema", "urgente")
gerenciador.adicionar_solicitacao("Recuperação de senha", "padrão")
gerenciador.adicionar_solicitacao("Servidor fora do ar", "urgente")

# Exibindo o estado da fila
gerenciador.exibir_fila()

# Processando as solicitações na ordem de prioridade
gerenciador.processar_solicitacao()  # Deve processar uma solicitação urgente
gerenciador.processar_solicitacao()  # Deve processar outra urgente
gerenciador.processar_solicitacao()  # Agora deve processar a solicitação padrão
gerenciador.processar_solicitacao()  # Processa a última solicitação

# Exibindo o estado da fila após o processamento
gerenciador.exibir_fila()
