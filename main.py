import tkinter as tk
from tkinter import filedialog

class SistemaApostas:
    def __init__(self):
        self.apostas = {}

    def carregar_apostas(self, arquivo):
        with open(arquivo, 'r') as f:
            for linha in f:
                dados = linha.strip().split()
                nome = dados[0]
                valor = float(dados[1])
                staff_apostado = dados[2]
                if nome in self.apostas:
                    self.apostas[nome]["valor"] += valor
                else:
                    self.apostas[nome] = {"valor": valor, "staff_apostado": staff_apostado}

    def calcular_vencedores(self, staff_vencedor):
        vencedores = {nome: aposta["valor"] for nome, aposta in self.apostas.items() if aposta["staff_apostado"] == staff_vencedor}
        total_apostado_no_staff = sum(aposta["valor"] for aposta in self.apostas.values() if aposta["staff_apostado"] == staff_vencedor)

        return vencedores, total_apostado_no_staff

    def calcular_total_apostado(self):
        return sum(aposta["valor"] for aposta in self.apostas.values())

    def distribuir_premios(self, total_premio, vencedores):
        total_apostado_vencedores = sum(valor for valor in vencedores.values())
        proporcoes = {nome: vencedor / total_apostado_vencedores for nome, vencedor in vencedores.items()}
        premios = {nome: proporcao * total_premio for nome, proporcao in proporcoes.items()}
        return premios


class ApostasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Apostas")

        self.sistema = SistemaApostas()

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.btn_load = tk.Button(self.frame, text="Carregar Apostas", command=self.carregar_apostas)
        self.btn_load.pack()

        self.label_apostas = tk.Label(self.frame, text="Apostas carregadas:")
        self.label_apostas.pack()

        self.staff_entry = tk.Entry(self.frame)
        self.staff_entry.pack()

        self.btn_calcular = tk.Button(self.frame, text="Calcular Vencedores", command=self.calcular_vencedores)
        self.btn_calcular.pack()

        self.label_resultado = tk.Label(self.frame, text="")
        self.label_resultado.pack()

    def carregar_apostas(self):
        arquivo_apostas = filedialog.askopenfilename(title="Selecione o arquivo de apostas", filetypes=[("Text files", "*.txt")])
        self.sistema.carregar_apostas(arquivo_apostas)

        text = "Apostas carregadas:\n"
        for nome, aposta in self.sistema.apostas.items():
            text += f"{nome}: {aposta['valor']} em {aposta['staff_apostado']}\n"

        self.label_apostas.config(text=text)

    def calcular_vencedores(self):
        staff_vencedor = self.staff_entry.get()
        vencedores, total_apostado_no_staff = self.sistema.calcular_vencedores(staff_vencedor)

        text = f"Vencedores no staff {staff_vencedor}:\n"
        for nome, valor in vencedores.items():
            porcentagem_ganho = (valor / total_apostado_no_staff) * 100
            valor_ganho_total = porcentagem_ganho * self.sistema.calcular_total_apostado() / 100
            text += f"{nome}: Valor ganho: {valor_ganho_total}, Porcentagem ganha: {porcentagem_ganho:.2f}%\n"

        self.label_resultado.config(text=text)



def main():
    root = tk.Tk()
    app = ApostasGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
