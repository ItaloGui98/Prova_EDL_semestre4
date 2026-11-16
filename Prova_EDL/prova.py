# PROVA - ESTRUTURA DE DADOS

# ============================================================
# QUESTÃO 1 - HISTÓRICO DE NAVEGAÇÃO
# ============================================================

class HistoricoNavegacao:
    def __init__(self, pagina_inicial):
        self.atual = pagina_inicial
        self.voltar_pilha = []
        self.proximo_pilha = []

    def visitar(self, pagina):
        self.voltar_pilha.append(self.atual)
        self.atual = pagina

        # Substituir a pilha evita percorrer os elementos antigos.
        self.proximo_pilha = []

    def voltar(self):
        if self.voltar_pilha:
            self.proximo_pilha.append(self.atual)
            self.atual = self.voltar_pilha.pop()

        return self.atual

    def proximo(self):
        if self.proximo_pilha:
            self.voltar_pilha.append(self.atual)
            self.atual = self.proximo_pilha.pop()

        return self.atual

#Explicação: Tendo em vista o contexto da questão, a provável causa do problema era não limpar o histórico de avanço ao visitar uma nova página, o qual permitia acessar páginas antigas.

def executar_questao_1():
    navegador = HistoricoNavegacao("Spotify")

    navegador.visitar("YouTube")
    navegador.visitar("GitHub")

    print("Pagina atual:", navegador.atual)
    print("Voltar:", navegador.voltar())
    print("Voltar:", navegador.voltar())
    print("proximo:", navegador.proximo())

    navegador.visitar("Netflix")
    print("Depois de visitar uma nova pagina:", navegador.atual)
    print("proximo sem pagina disponivel:", navegador.proximo())


# ============================================================
# QUESTÃO 2 - FILA DE PACIENTES
# ============================================================

class NoPaciente:
    def __init__(self, nome):
        self.nome = nome
        self.proximo = None

class Fila:
    def __init__(self):
        self.inicio = None
        self.fim = None

    def chegar(self, nome):
        novo = NoPaciente(nome)

        if self.fim is None:
            self.inicio = novo
            self.fim = novo
        else:
            self.fim.proximo = novo
            self.fim = novo

    def chamar_proximo(self):
        if self.inicio is None:
            return None

        nome = self.inicio.nome
        self.inicio = self.inicio.proximo

        if self.inicio is None:
            self.fim = None

        return nome

    def desistir(self, nome):
        atual = self.inicio
        anterior = None

        while atual is not None:
            if atual.nome == nome:
                if anterior is None:
                    self.inicio = atual.proximo
                else:
                    anterior.proximo = atual.proximo

                if atual == self.fim:
                    self.fim = anterior

                return True

            anterior = atual
            atual = atual.proximo

        return False

#Explicação: A complexidade da desistência é O(n), pois independente do caso, é necessário percorrer toda a fila para identificar quem desistiu. Com isso, seria inviável ser O(1) porque não sabemos em qual posição o paciente está.

def executar_questao_2():
    fila = Fila()

    fila.chegar("Ana")
    fila.chegar("Carlos")
    fila.chegar("Maria")

    print("Paciente chamado:", fila.chamar_proximo())
    print("Carlos desistiu?", fila.desistir("Carlos"))
    print("Proximo paciente:", fila.chamar_proximo())
    print("Fila vazia - chamada:", fila.chamar_proximo())


# ============================================================
# QUESTÃO 3 - VERIFICAÇÃO DE SIMBOLOS NO EDITOR
# ============================================================

def verificar_simbolos(texto):
    pilha = []

    aberturas = {
        "(": ")",
        "[": "]",
        "{": "}"
    }

    fechamentos = [")", "]", "}"]

    for i in range(len(texto)):
        simbolo = texto[i]

        if simbolo in aberturas:
            pilha.append((simbolo, i))

        elif simbolo in fechamentos:
            if not pilha:
                return i

            abertura, posicao = pilha.pop()

            if aberturas[abertura] != simbolo:
                return i

    if pilha:
        return pilha[0][1]

    return -1

#Explicação: A complexidade de tempo é do tipo O(n), pois percorre o texto uma única vez. De memória também se encontra em O(n), pois a pilha pode armazer todos os símbolos de abertura.

def executar_questao_3():
    texto = "(a + b]"

    resultado = verificar_simbolos(texto)

    print("Texto verificado:", texto)

    if resultado == -1:
        print("Todos os simbolos estao corretos!")
    else:
        print("Simbolo incorreto na posicao:", resultado)
        print("Simbolo:", texto[resultado])


# ============================================================
# QUESTÃO 4 - PLAYLIST
# ============================================================

class NoMusica:
    def __init__(self, musica):
        self.musica = musica
        self.proximo = None


def remover_repetidas(inicio):
    atual = inicio

    while atual is not None and atual.proximo is not None:
        if atual.musica == atual.proximo.musica:
            atual.proximo = atual.proximo.proximo
        else:
            atual = atual.proximo

    return inicio


def inverter_playlist(inicio):
    anterior = None
    atual = inicio

    while atual is not None:
        proximo = atual.proximo
        atual.proximo = anterior
        anterior = atual
        atual = proximo

    return anterior

#Explicação: Caso a música apareça novamente em outra posição da playlist, será mantida, pois não é uma repetição consecutiva.

def executar_questao_4():
    inicio = NoMusica("Musica A")
    inicio.proximo = NoMusica("Musica A")
    inicio.proximo.proximo = NoMusica("Musica B")
    inicio.proximo.proximo.proximo = NoMusica("Musica C")
    inicio.proximo.proximo.proximo.proximo = NoMusica("Musica C")

    inicio = remover_repetidas(inicio)

    print("Playlist sem repeticoes consecutivas:")
    atual = inicio
    while atual is not None:
        print(atual.musica)
        atual = atual.proximo

    inicio = inverter_playlist(inicio)

    print("Playlist invertida:")
    atual = inicio
    while atual is not None:
        print(atual.musica)
        atual = atual.proximo


# ============================================================
# QUESTÃO 5 - BALANCEAMENTO
# ============================================================

class NoServidor:
    def __init__(self, nome):
        self.nome = nome
        self.proximo = None


class Balanceador:
    def __init__(self):
        self.ultimo = None

    def adicionar(self, nome):
        novo = NoServidor(nome)

        if self.ultimo is None:
            novo.proximo = novo
            self.ultimo = novo
        else:
            novo.proximo = self.ultimo.proximo
            self.ultimo.proximo = novo
            self.ultimo = novo

    def proxima_requisicao(self):
        if self.ultimo is None:
            return None

        self.ultimo = self.ultimo.proximo
        return self.ultimo.nome

    def remover(self, nome):
        if self.ultimo is None:
            return False

        primeiro = self.ultimo.proximo
        atual = primeiro
        anterior = self.ultimo

        while True:
            if atual.nome == nome:
                if atual.proximo == atual:
                    self.ultimo = None

                else:
                    anterior.proximo = atual.proximo

                    if atual == self.ultimo:
                        self.ultimo = anterior

                return True

            anterior = atual
            atual = atual.proximo

            if atual == primeiro:
                break

        return False

def executar_questao_5():
    balanceador = Balanceador()

    balanceador.adicionar("Servidor 1")
    balanceador.adicionar("Servidor 2")
    balanceador.adicionar("Servidor 3")

    print("Proxima requisicao:", balanceador.proxima_requisicao())
    print("Proxima requisicao:", balanceador.proxima_requisicao())
    print("Remover Servidor 2:", balanceador.remover("Servidor 2"))
    print("Remover Servidor 5:", balanceador.remover("Servidor 5"))
    print("Proxima requisicao:", balanceador.proxima_requisicao())

    vazio = Balanceador()
    print("Requisicao sem servidores:", vazio.proxima_requisicao())


# ============================================================
# MENU DA PROVA
# ============================================================

def menu():
    while True:
        print("\n========== MENU DA PROVA ==========")
        print("1 - Questao 1: Histórico de navegação")
        print("2 - Questao 2: Fila de pacientes")
        print("3 - Questao 3: Verificação de símbolos no editor")
        print("4 - Questao 4: Playlist de músicas")
        print("5 - Questao 5: Balanceamento de servidores")
        print("6 - Questao 6: Desfazer e refazer - memória")
        print("0 - Sair")
        print("========================================")

        opcao = input("Escolha uma questao: ")

        if opcao == "1":
            executar_questao_1()
        elif opcao == "2":
            executar_questao_2()
        elif opcao == "3":
            executar_questao_3()
        elif opcao == "4":
            executar_questao_4()
        elif opcao == "5":
            executar_questao_5()
        elif opcao == "0":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inexistente! Tente novamente")

if __name__ == "__main__":
    menu()
