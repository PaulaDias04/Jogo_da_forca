import tkinter as tk
from tkinter import messagebox
import winsound
from forca_logica import JogoDaForcaLogica

class JogoDaForcaGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Jogo da Forca")

        # Configurações de estilo
        self.palavras = ["BRASIL", "ARGENTINA", "PARAGUAI", "URUGUAI", "PERU", "CHILE"]
        self.fonte_principal = ("Arial", 16)
        self.fonte_titulo = ("Arial", 24, "bold")
        self.cor_principal = "#f0f0f0"  # Cor de fundo
        self.cor_texto = "#333333"      # Cor do texto
        self.cor_forca = "#333333"      # Cor das linhas da forca
        self.cor_acerto = "green"       # Feedback positivo
        self.cor_erro = "red"           # Feedback negativo

        # Inicializa o jogo
        self.jogo_logica = JogoDaForcaLogica(self.palavras)
        self.master.config(bg=self.cor_principal)
        self.elementos_forca = {
            'cabeca': None, 'corpo': None, 
            'braco_esquerdo': None, 'braco_direito': None,
            'perna_esquerda': None, 'perna_direita': None
        }

        # Configuração do layout
        self.criar_interface()

    def criar_interface(self):
        """Cria todos os elementos da interface"""
        # Frame principal
        self.frame_principal = tk.Frame(self.master, bg=self.cor_principal)
        self.frame_principal.pack(pady=20)

        # Área da forca (lado esquerdo)
        self.frame_forca = tk.Frame(self.frame_principal, bg=self.cor_principal)
        self.frame_forca.pack(side=tk.LEFT, padx=40)

        self.canvas_forca = tk.Canvas(
            self.frame_forca, 
            width=220, 
            height=300, 
            bg=self.cor_principal, 
            highlightthickness=0
        )
        self.canvas_forca.pack()
        self.desenhar_forca_base()

        # Área de controle (lado direito)
        self.frame_controles = tk.Frame(self.frame_principal, bg=self.cor_principal)
        self.frame_controles.pack(side=tk.RIGHT, padx=40)

        # Elementos da interface
        tk.Label(
            self.frame_controles, 
            text="Jogo da Forca", 
            font=self.fonte_titulo, 
            bg=self.cor_principal, 
            fg=self.cor_texto
        ).pack(pady=10)

        self.label_palavra = tk.Label(
            self.frame_controles, 
            text=self.jogo_logica.exibir_palavra(), 
            font=("Arial", 24), 
            bg=self.cor_principal, 
            fg=self.cor_texto
        )
        self.label_palavra.pack(pady=20)

        self.label_tentativas = tk.Label(
            self.frame_controles, 
            text=f"Tentativas restantes: {self.jogo_logica.tentativas_restantes}", 
            font=self.fonte_principal, 
            bg=self.cor_principal, 
            fg=self.cor_texto
        )
        self.label_tentativas.pack(pady=5)

        self.label_letras_erradas = tk.Label(
            self.frame_controles, 
            text="Letras erradas: ", 
            font=self.fonte_principal, 
            bg=self.cor_principal, 
            fg=self.cor_erro
        )
        self.label_letras_erradas.pack(pady=5)

        # Entrada de letra
        self.frame_entrada = tk.Frame(self.frame_controles, bg=self.cor_principal)
        self.frame_entrada.pack(pady=20)
        
        tk.Label(
            self.frame_entrada, 
            text="Digite uma letra:", 
            font=self.fonte_principal, 
            bg=self.cor_principal, 
            fg=self.cor_texto
        ).pack(side=tk.LEFT)

        self.entry_letra = tk.Entry(
            self.frame_entrada, 
            font=self.fonte_principal, 
            width=3, 
            justify='center'
        )
        self.entry_letra.pack(side=tk.LEFT, padx=10)
        self.entry_letra.focus_set()

        self.botao_tentar = tk.Button(
            self.frame_controles, 
            text="Tentar", 
            font=self.fonte_principal, 
            command=self.tentar_letra, 
            bg="#dddddd", 
            fg=self.cor_texto, 
            padx=20, 
            pady=5
        )
        self.botao_tentar.pack(pady=10)

        # Feedback
        self.label_feedback = tk.Label(
            self.frame_controles, 
            text="", 
            font=self.fonte_principal, 
            bg=self.cor_principal
        )
        self.label_feedback.pack(pady=10)

    def desenhar_forca_base(self):
        """Desenha a estrutura básica da forca"""
        self.canvas_forca.create_line(30, 280, 190, 280, width=5, fill=self.cor_forca)  # Base
        self.canvas_forca.create_line(60, 280, 60, 30, width=5, fill=self.cor_forca)    # Poste
        self.canvas_forca.create_line(60, 30, 160, 30, width=5, fill=self.cor_forca)     # Topo
        self.canvas_forca.create_line(160, 30, 160, 60, width=3, fill=self.cor_forca)    # Corda

    def tentar_letra(self):
        """Processa a tentativa de letra do jogador"""
        letra = self.entry_letra.get().upper()
        self.entry_letra.delete(0, tk.END)
        
        # Feedback sonoro imediato
        winsound.PlaySound("SystemQuestion", winsound.SND_ASYNC)

        if not letra or len(letra) != 1 or not letra.isalpha():
            self.mostrar_feedback("Por favor, digite uma letra válida", self.cor_erro)
            return

        resultado, mensagem = self.jogo_logica.tentar_letra(letra)
        self.mostrar_feedback(mensagem, self.cor_acerto if resultado else self.cor_erro)
        self.atualizar_interface()

        if not resultado:
            if "perdeu" in mensagem.lower():
                self.botao_tentar.config(state=tk.DISABLED)
                self.tocar_som_perda()
                self.desenhar_boneco_completo()
            else:
                self.tocar_som_erro()
                self.atualizar_forca()
        else:
            if "parabéns" in mensagem.lower():
                self.botao_tentar.config(state=tk.DISABLED)
                self.tocar_som_acerto()
            else:
                self.tocar_som_acerto()

    def atualizar_interface(self):
        """Atualiza todos os elementos visuais da interface"""
        estado = self.jogo_logica.get_estado_jogo()
        self.label_palavra.config(text=estado["palavra_exibida"])
        self.label_tentativas.config(text=f"Tentativas restantes: {estado['tentativas_restantes']}")
        self.label_letras_erradas.config(text=f"Letras erradas: {', '.join(estado['letras_erradas'])}")

    def atualizar_forca(self):
        """Desenha partes do boneco conforme os erros"""
        erros = 6 - self.jogo_logica.tentativas_restantes
        
        if erros == 1 and not self.elementos_forca['cabeca']:
            self.elementos_forca['cabeca'] = self.canvas_forca.create_oval(140, 60, 180, 100, width=2, outline=self.cor_forca)
        elif erros == 2 and not self.elementos_forca['corpo']:
            self.elementos_forca['corpo'] = self.canvas_forca.create_line(160, 100, 160, 180, width=2, fill=self.cor_forca)
        elif erros == 3 and not self.elementos_forca['braco_esquerdo']:
            self.elementos_forca['braco_esquerdo'] = self.canvas_forca.create_line(160, 120, 130, 150, width=2, fill=self.cor_forca)
        elif erros == 4 and not self.elementos_forca['braco_direito']:
            self.elementos_forca['braco_direito'] = self.canvas_forca.create_line(160, 120, 190, 150, width=2, fill=self.cor_forca)
        elif erros == 5 and not self.elementos_forca['perna_esquerda']:
            self.elementos_forca['perna_esquerda'] = self.canvas_forca.create_line(160, 180, 130, 210, width=2, fill=self.cor_forca)
        elif erros == 6 and not self.elementos_forca['perna_direita']:
            self.elementos_forca['perna_direita'] = self.canvas_forca.create_line(160, 180, 190, 210, width=2, fill=self.cor_forca)

    def desenhar_boneco_completo(self):
        """Desenha todas as partes do boneco (quando perde)"""
        partes = {
            'cabeca': (140, 60, 180, 100),
            'corpo': (160, 100, 160, 180),
            'braco_esquerdo': (160, 120, 130, 150),
            'braco_direito': (160, 120, 190, 150),
            'perna_esquerda': (160, 180, 130, 210),
            'perna_direita': (160, 180, 190, 210)
        }
        
        for parte, coords in partes.items():
            if not self.elementos_forca[parte]:
                if parte == 'cabeca':
                    self.elementos_forca[parte] = self.canvas_forca.create_oval(*coords, width=2, outline=self.cor_forca)
                else:
                    self.elementos_forca[parte] = self.canvas_forca.create_line(*coords, width=2, fill=self.cor_forca)

    def mostrar_feedback(self, mensagem, cor):
        """Exibe mensagem de feedback temporária"""
        self.label_feedback.config(text=mensagem, fg=cor)
        self.master.after(3000, lambda: self.label_feedback.config(text=""))

    # Sons do jogo
    def tocar_som_acerto(self):
        winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC)

    def tocar_som_erro(self):
        winsound.PlaySound("SystemHand", winsound.SND_ASYNC)

    def tocar_som_perda(self):
        winsound.PlaySound("SystemExclamation", winsound.SND_ASYNC)

def main():
    root = tk.Tk()
    app = JogoDaForcaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()