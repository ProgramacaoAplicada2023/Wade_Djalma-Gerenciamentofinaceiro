import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class GerenciamentoFinanceiroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento Financeiro")
        self.root.geometry("600x300")
        self.saldo_atual = 0.0
        self.gasto_no_mes = 0.0
        self.economias = 0.0
        self.transacoes = {"Despesa": {"Aluguel": [], "Combustível": [], "Alimentação": [], "Financiamento": [], "Manutenção": [], "Vestuário": [], "Gás e Energia": [], "Outros": []},
                           "Receita": [],
                           "Compra no Cartão": []}

        # Configuração da barra de menu
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Sair", command=root.destroy)
        file_menu.add_command(label="Deslogar", command=self.deslogar)

        # Criação de um estilo para alterar as configurações visuais
        style = ttk.Style()

        # Cores formais
        bg_color = "#F0F0F0"  # Cor de fundo
        fg_color = "#000000"  # Cor do texto (preto)
        button_color = "#4CAF50"  # Cor do botão

        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TButton', background=button_color, foreground=fg_color)
        style.map('TButton', background=[('active', '#45A049')])

        # Frame para exibir saldo, economias e gasto no mês
        self.frame_saldo = ttk.Frame(root, style='TFrame')
        self.frame_saldo.pack(pady=10)

        ttk.Label(self.frame_saldo, text="Saldo Atual:", style='TLabel').grid(row=0, column=0, padx=10, pady=5)
        self.label_saldo = ttk.Label(self.frame_saldo, text=f"R${self.saldo_atual:.2f}", style='TLabel')
        self.label_saldo.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.frame_saldo, text="Gasto no Mês:", style='TLabel').grid(row=1, column=0, padx=10, pady=5)
        self.label_gasto_mes = ttk.Label(self.frame_saldo, text=f"R${self.gasto_no_mes:.2f}", style='TLabel')
        self.label_gasto_mes.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.frame_saldo, text="Economias:", style='TLabel').grid(row=2, column=0, padx=10, pady=5)
        self.label_economias = ttk.Label(self.frame_saldo, text=f"R${self.economias:.2f}", style='TLabel')
        self.label_economias.grid(row=2, column=1, padx=10, pady=5)

        # Frame para ações financeiras
        self.frame_acoes = ttk.Frame(root, style='TFrame')
        self.frame_acoes.pack(pady=20)

        # Botões de ação
        btn_adicionar_despesa = ttk.Button(self.frame_acoes, text="Adicionar Despesa", command=self.adicionar_despesa, style='TButton')
        btn_adicionar_despesa.grid(row=0, column=0, padx=10, pady=5)

        btn_adicionar_receita = ttk.Button(self.frame_acoes, text="Adicionar Receita", command=self.adicionar_receita, style='TButton')
        btn_adicionar_receita.grid(row=0, column=1, padx=10, pady=5)

        btn_adicionar_compra_cartao = ttk.Button(self.frame_acoes, text="Adicionar Compra no Cartão", command=self.adicionar_compra_cartao, style='TButton')
        btn_adicionar_compra_cartao.grid(row=0, column=2, padx=10, pady=5)

        btn_guardar_dinheiro = ttk.Button(self.frame_acoes, text="Guardar Dinheiro", command=self.guardar_dinheiro, style='TButton')
        btn_guardar_dinheiro.grid(row=1, column=0, padx=10, pady=5)

        btn_visualizar_extrato = ttk.Button(self.frame_acoes, text="Visualizar Extrato", command=self.visualizar_extrato, style='TButton')
        btn_visualizar_extrato.grid(row=1, column=1, padx=10, pady=5)

        btn_deslogar = ttk.Button(self.frame_acoes, text="Deslogar", command=self.deslogar, style='TButton')
        btn_deslogar.grid(row=1, column=2, padx=10, pady=5)

        self.tipos_despesa = ["Aluguel", "Combustível", "Alimentação", "Financiamento", "Manutenção", "Vestuário", "Outros"]

    def visualizar_grafico_despesas(self):
        # Criar dados de exemplo para o gráfico (substitua isso pelos seus próprios dados)
        categorias = list(self.transacoes["Despesa"].keys())
        valores = [sum(map(lambda x: float(x.split()[0][3:]), transacoes)) for transacoes in
                   self.transacoes["Despesa"].values()]

        # Criar um gráfico de barras
        fig, ax = plt.subplots()
        ax.bar(categorias, valores)

        # Adicionar rótulos e título
        ax.set_ylabel('Valor (R$)')
        ax.set_xlabel('Categorias de Despesas')
        ax.set_title('Despesas por Categoria')

        # Adicionar o gráfico à interface gráfica usando o Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Adicionar um botão para fechar o gráfico
        btn_fechar_grafico = tk.Button(self.root, text="Fechar Gráfico", command=lambda: self.fechar_grafico(canvas))
        btn_fechar_grafico.pack()

    def fechar_grafico(self, canvas):
        # Destruir o widget do gráfico e o botão
        canvas.get_tk_widget().destroy()
        canvas.get_tk_widget().get_tk_widget().destroy()
        self.atualizar_labels()  # Atualizar os rótulos após fechar o gráfico

    def adicionar_despesa(self):
        janela_despesa = tk.Toplevel(self.root)
        janela_despesa.title("Adicionar Despesa")

        frame_despesa = tk.Frame(janela_despesa)
        frame_despesa.pack(pady=20)

        tk.Label(frame_despesa, text="Valor da Despesa:").grid(row=0, column=0, padx=10, pady=5)
        entry_valor_despesa = tk.Entry(frame_despesa)
        entry_valor_despesa.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_despesa, text="Tipo de Gasto:").grid(row=1, column=0, padx=10, pady=5)
        combo_tipo_gasto = ttk.Combobox(frame_despesa, values=self.tipos_despesa)
        combo_tipo_gasto.grid(row=1, column=1, padx=10, pady=5)

        btn_confirmar_despesa = tk.Button(frame_despesa, text="Confirmar", command=lambda: self.confirmar_transacao(janela_despesa, float(entry_valor_despesa.get()), "Despesa", combo_tipo_gasto.get()))
        btn_confirmar_despesa.grid(row=2, column=0, columnspan=2, pady=10)

    def adicionar_receita(self):
        janela_receita = tk.Toplevel(self.root)
        janela_receita.title("Adicionar Receita")

        frame_receita = tk.Frame(janela_receita)
        frame_receita.pack(pady=20)

        tk.Label(frame_receita, text="Valor da Receita:").grid(row=0, column=0, padx=10, pady=5)
        entry_valor_receita = tk.Entry(frame_receita)
        entry_valor_receita.grid(row=0, column=1, padx=10, pady=5)

        btn_confirmar_receita = tk.Button(frame_receita, text="Confirmar", command=lambda: self.confirmar_transacao(janela_receita, float(entry_valor_receita.get()), "Receita", None))
        btn_confirmar_receita.grid(row=1, column=0, columnspan=2, pady=10)

    def adicionar_compra_cartao(self):
        janela_compra_cartao = tk.Toplevel(self.root)
        janela_compra_cartao.title("Adicionar Compra no Cartão")

        frame_compra_cartao = tk.Frame(janela_compra_cartao)
        frame_compra_cartao.pack(pady=20)

        tk.Label(frame_compra_cartao, text="Valor da Compra:").grid(row=0, column=0, padx=10, pady=5)
        entry_valor_compra = tk.Entry(frame_compra_cartao)
        entry_valor_compra.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_compra_cartao, text="Parcelas:").grid(row=1, column=0, padx=10, pady=5)
        entry_parcelas = tk.Entry(frame_compra_cartao)
        entry_parcelas.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame_compra_cartao, text="Descrição da Compra:").grid(row=2, column=0, padx=10, pady=5)
        entry_descricao_compra = tk.Entry(frame_compra_cartao)
        entry_descricao_compra.grid(row=2, column=1, padx=10, pady=5)

        btn_confirmar_compra_cartao = tk.Button(frame_compra_cartao, text="Confirmar", command=lambda: self.confirmar_compra_cartao(janela_compra_cartao, float(entry_valor_compra.get()), int(entry_parcelas.get()), entry_descricao_compra.get()))
        btn_confirmar_compra_cartao.grid(row=3, column=0, columnspan=2, pady=10)

    def confirmar_compra_cartao(self, janela, valor, parcelas, descricao):
        if parcelas <= 0:
            messagebox.showerror("Erro", "O número de parcelas deve ser maior que zero.")
            return

        valor_parcela = valor / parcelas
        datas_parcelas = self.calcular_datas_parcelas(parcelas)

        for i in range(parcelas):
            transacao_descricao = f"Descrição: {descricao}\n" if descricao else ""
            transacao = f"{transacao_descricao}Parcela {i + 1}/{parcelas}: R${valor_parcela:.2f} em {datas_parcelas[i]}"
            self.transacoes["Compra no Cartão"].append(transacao)
            self.gasto_no_mes += valor_parcela  # Adiciona apenas o valor da parcela ao gasto no mês

            # Exibe um extrato separado para cada transação
            messagebox.showinfo("Confirmação", f"Compra parcelada de R${valor:.2f} em {parcelas} vezes confirmada!\n{transacao}")

        self.saldo_atual -= valor
        self.atualizar_labels()
        janela.destroy()

    def guardar_dinheiro(self):
        janela_guardar_dinheiro = tk.Toplevel(self.root)
        janela_guardar_dinheiro.title("Guardar/Retirar Dinheiro")

        frame_guardar_dinheiro = tk.Frame(janela_guardar_dinheiro)
        frame_guardar_dinheiro.pack(pady=20)

        tk.Label(frame_guardar_dinheiro, text="Valor:").grid(row=0, column=0, padx=10, pady=5)
        entry_valor = tk.Entry(frame_guardar_dinheiro)
        entry_valor.grid(row=0, column=1, padx=10, pady=5)

        # Adicionando botão de opção (radiobutton) para escolher entre "Guardar" e "Retirar"
        var_tipo_operacao = tk.StringVar()
        var_tipo_operacao.set("guardar")  # Valor padrão, operação de guardar dinheiro

        radio_guardar = tk.Radiobutton(frame_guardar_dinheiro, text="Guardar", variable=var_tipo_operacao,
                                       value="guardar")
        radio_guardar.grid(row=1, column=0, padx=5, pady=5)

        radio_retirar = tk.Radiobutton(frame_guardar_dinheiro, text="Retirar", variable=var_tipo_operacao,
                                       value="retirar")
        radio_retirar.grid(row=1, column=1, padx=5, pady=5)

        btn_confirmar = tk.Button(frame_guardar_dinheiro, text="Confirmar",
                                  command=lambda: self.confirmar_guardar_dinheiro(janela_guardar_dinheiro,
                                                                                  float(entry_valor.get()),
                                                                                  var_tipo_operacao.get()))
        btn_confirmar.grid(row=2, column=0, columnspan=2, pady=10)

    def confirmar_guardar_dinheiro(self, janela, valor, tipo_operacao):
        if tipo_operacao == "guardar":
            self.economias += valor
            self.saldo_atual -= valor
        elif tipo_operacao == "retirar":
            if valor > self.economias:
                messagebox.showerror("Erro", "Saldo insuficiente para retirar a quantia desejada.")
                return
            self.economias -= valor
            self.saldo_atual += valor

        self.atualizar_labels()
        messagebox.showinfo("Confirmação", f"R${valor:.2f} {tipo_operacao}do com sucesso!")

        janela.destroy()

    def calcular_datas_parcelas(self, parcelas):
        datas = []
        data_atual = datetime.now()

        for i in range(parcelas):
            nova_data = data_atual + timedelta(days=(i + 1) * 30)  # Adiciona 30 dias para cada parcela
            datas.append(nova_data.strftime('%d/%m/%Y'))

        return datas

    def confirmar_transacao(self, janela, valor, tipo, tipo_gasto):
        if tipo == "Despesa":
            self.saldo_atual -= valor
            self.gasto_no_mes += valor
            self.transacoes[tipo][tipo_gasto].append(f"R${valor:.2f} em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        elif tipo == "Receita":
            self.saldo_atual += valor
            self.transacoes[tipo].append(f"R${valor:.2f} em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        self.atualizar_labels()
        messagebox.showinfo("Confirmação", f"{tipo} ({tipo_gasto}): R${valor:.2f} confirmada!")
        janela.destroy()

    def atualizar_labels(self):
        self.label_saldo.config(text=f"R${self.saldo_atual:.2f}")
        self.label_gasto_mes.config(text=f"R${self.gasto_no_mes:.2f}")
        self.label_economias.config(text=f"R${self.economias:.2f}")

    def visualizar_extrato(self):
        extrato = ""
        for tipo, transacoes_tipo in self.transacoes.items():
            extrato += f"\n--- {tipo} ---\n"
            if isinstance(transacoes_tipo, list):
                extrato += "\n".join(transacoes_tipo)
            elif isinstance(transacoes_tipo, dict):
                for tipo_gasto, transacoes_tipo_gasto in transacoes_tipo.items():
                    extrato += f"\n--- {tipo_gasto} ---\n"
                    extrato += "\n".join(transacoes_tipo_gasto)

        messagebox.showinfo("Extrato", extrato)

    def deslogar(self):

        messagebox.showinfo("Deslogar", "Usuário deslogado com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = GerenciamentoFinanceiroApp(root)
    root.mainloop()