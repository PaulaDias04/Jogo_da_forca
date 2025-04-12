import random

class JogoDaForcaLogica:
    def __init__(self, palavras):
        self.palavras = palavras
        self.palavra_secreta = random.choice(self.palavras).upper()
        self.letras_corretas = set()
        self.letras_erradas = set()
        self.tentativas_restantes = 6

    def exibir_palavra(self):
        display = ""
        for letra in self.palavra_secreta:
            if letra in self.letras_corretas:
                display += letra + " "
            else:
                display += "_ "
        return display.strip()

    def tentar_letra(self, letra): 
        letra = letra.upper()
        if not letra.isalpha() or len(letra) != 1:
            return False, "Por favor, digite uma letra válida."
        if letra in self.letras_corretas or letra in self.letras_erradas:
            return False, "Você já tentou essa letra."
        if letra in self.palavra_secreta:
            self.letras_corretas.add(letra)
            if "_" not in self.exibir_palavra():
                return True, "Parabéns! Você adivinhou a palavra."
            return True, "Letra correta!"
        else:
            self.letras_erradas.add(letra)
            self.tentativas_restantes -= 1
            if self.tentativas_restantes == 0:
                return False, f"Você perdeu! A palavra era: {self.palavra_secreta}"
            return False, "Letra incorreta."

    def get_estado_jogo(self):
        return {
            "palavra_exibida": self.exibir_palavra(),
            "letras_erradas": sorted(list(self.letras_erradas)),
            "tentativas_restantes": self.tentativas_restantes
        }