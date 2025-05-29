import sys
import sqlite3
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                             QComboBox, QTableWidget, QTableWidgetItem, QCheckBox, QHeaderView)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDateEdit
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtGui import QIcon

conn = sqlite3.connect("financeiro.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS lancamentos (
        id INTEGER PRIMARY KEY,
        categoria TEXT,
        tipo TEXT,
        valor REAL,
        data TEXT,
        descricao TEXT,
        pago INTEGER DEFAULT 0
    )
""")
conn.commit()

class FinanceiroApp(QWidget):
    def __init__(self):
        super().__init__()

        with open("sf.qss", "r") as file:
            self.setStyleSheet(file.read())
            
        self.setWindowTitle("Sistema Financeiro")
        self.setGeometry(300, 150, 900, 600)

        self.title_label = QLabel(" SISTEMA FINANCEIRO ")
        self.title_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #FFFFFF; text-align: center;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)  

        content_layout = QHBoxLayout()

        table_layout = QVBoxLayout()
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(["Categoria", "Tipo", "Valor", "Data", "Descrição", "Pago"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabela.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)

        table_layout.addWidget(
    QLabel(
        '<h3 style="color: #00B0FF;">Planilha de Lançamentos</h3>',
        alignment=Qt.AlignmentFlag.AlignCenter
    )
)
        table_layout.addWidget(self.tabela)

        self.tabela.setStyleSheet("background-color: #1A1A1A; border: 1px solid #000000; gridline-color: #000000;")
        self.tabela.horizontalHeader().setStyleSheet("color: #A0A0A0; background-color: #262626; font-weight: bold;")

        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        input_layout.addWidget(
    QLabel(
        '<h3 style="color: #FFD700;">Adicionar Lançamento</h3>',
        alignment=Qt.AlignmentFlag.AlignCenter
    )
)

        self.categoria_combo = QComboBox()
        self.categoria_combo.addItems(["Alimentação", "Transporte", "Educação", "Lazer", "Saúde", "Economias", "Viagem", "Compras", "Outros"])
        self.categoria_combo.setStyleSheet("background-color: #1A1A1A; color: white; padding: 5px; border-radius: 5px;")
        self.categoria_combo.setMinimumHeight(50)

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Despesa", "Receita"])
        self.tipo_combo.setMinimumHeight(50)
        self.tipo_combo.setStyleSheet("background-color: #1A1A1A; color: white; padding: 5px; border-radius: 5px;")

        self.valor_input = QLineEdit()
        self.valor_input.setPlaceholderText("Valor (R$)")
        self.valor_input.setMinimumHeight(50)
        self.valor_input.setStyleSheet("background-color: #1A1A1A; color: white; padding: 5px; border-radius: 5px;")

        self.data_input = QDateEdit()
        self.data_input.setDisplayFormat("yyyy-MM-dd")  
        self.data_input.setCalendarPopup(True)  
        self.data_input.setDate(QDate.currentDate()) 
        self.data_input.setMinimumHeight(50)
        self.data_input.setStyleSheet("background-color: #1A1A1A; color: white; padding: 5px; border-radius: 5px;")

        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Descrição")
        self.desc_input.setMinimumHeight(50)
        self.desc_input.setStyleSheet("background-color: #1A1A1A; color: white; padding: 5px; border-radius: 5px;")

        self.pago_checkbox = QCheckBox("Pago/Lembrete")
        self.pago_checkbox.setStyleSheet("font-size: 16px; padding: 10px;")
        self.pago_checkbox.setStyleSheet("background-color: #1A1A1A; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")

        input_layout.addWidget(QLabel("Categoria:"))
        input_layout.addWidget(self.categoria_combo)
        input_layout.addWidget(QLabel("Tipo:"))
        input_layout.addWidget(self.tipo_combo)
        input_layout.addWidget(QLabel("Valor:"))
        input_layout.addWidget(self.valor_input)
        input_layout.addWidget(QLabel("Data:"))
        input_layout.addWidget(self.data_input)
        input_layout.addWidget(QLabel("Descrição:"))
        input_layout.addWidget(self.desc_input)
        input_layout.addWidget(self.pago_checkbox)

        btn_layout = QHBoxLayout()

        self.btn_add = QPushButton("Adicionar Lançamento")
        self.btn_add.setStyleSheet("background-color: #28a745; color: white; font-weight: bold;")
        self.btn_add.clicked.connect(self.adicionar_lancamento)
        self.btn_add.setIcon(QIcon("icons/add.png.png"))

        self.btn_limpar = QPushButton("Limpar Registros")
        self.btn_limpar.setStyleSheet("background-color: #dc3545; color: white; font-weight: bold;")
        self.btn_limpar.clicked.connect(self.limpar_registros)
        self.btn_limpar.setIcon(QIcon("icons/trash.png.png"))

        self.btn_excluir_ultimo = QPushButton("Excluir Último Lançamento")
        self.btn_excluir_ultimo.setStyleSheet("background-color: #007bff; color: white; font-weight: bold;")
        self.btn_excluir_ultimo.clicked.connect(self.excluir_ultimo_lancamento)
        self.btn_excluir_ultimo.setIcon(QIcon("icons/remove.png.png"))

        btn_layout.addWidget(self.btn_limpar)
        btn_layout.addWidget(self.btn_excluir_ultimo)

        input_layout.addWidget(self.btn_add)
        input_layout.addLayout(btn_layout)

        self.btn_add.setStyleSheet("""
            QPushButton {
                background-color: #28a745; color: white; font-weight: bold; 
            }
            QPushButton:hover {
                background-color: #218838;
           }
        """)

        self.btn_limpar.setStyleSheet("""
            QPushButton {
                background-color: #dc3545; color: white; font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b22222;
            }
        """)

        self.btn_excluir_ultimo.setStyleSheet("""
            QPushButton {
                background-color: #007bff; color: white; font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        content_layout.addLayout(table_layout, 2)  
        content_layout.addLayout(input_layout, 1)  

        main_layout.addLayout(content_layout)

        self.hist_label = QLabel("")
        self.hist_label.setFont(QFont("Arial", 14))
        self.hist_label.setStyleSheet("color: #FFD700;")
        main_layout.addWidget(self.hist_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.total_label = QLabel("")
        self.total_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.total_label.setStyleSheet("color: #FFFFFF;")
        main_layout.addWidget(self.total_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)
        self.carregar_dados()

    def adicionar_lancamento(self):
        categoria = self.categoria_combo.currentText()
        tipo = self.tipo_combo.currentText()
        valor_text = self.valor_input.text().replace(',', '.')
        data = self.data_input.text()
        descricao = self.desc_input.text()

        self.valor_input.setStyleSheet("background-color: #1A1A1A; color: white; padding: 5px; border-radius: 5px;")
        self.desc_input.setStyleSheet("background-color: #1A1A1A; color: white; padding: 5px; border-radius: 5px;")

        campos_vazios = []
    
        if not valor_text:
            campos_vazios.append("Valor")
            self.valor_input.setStyleSheet("background-color: #1A1A1A; color: red; border: 2px solid red; padding: 5px; border-radius: 5px;")
        
        if not descricao:
            campos_vazios.append("Descrição")
            self.desc_input.setStyleSheet("background-color: #1A1A1A; color: red; border: 2px solid red; padding: 5px; border-radius: 5px;")

        if campos_vazios:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erro ao adicionar")
            msg.setText(f"Por favor, preencha os campos obrigatórios: {', '.join(campos_vazios)}.")
            msg.setStyleSheet("background-color: #262626; color: #FFD700; font-size: 16px;")  
            return
    
        try:
            valor = float(valor_text)
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erro de Valor")
            msg.setText("Digite um valor numérico válido.")
            msg.setStyleSheet("background-color: #262626; color: #FFD700; font-size: 16px;") 
            msg.exec()
            return

        pago = 1 if self.pago_checkbox.isChecked() else 0

        cursor.execute("INSERT INTO lancamentos (categoria, tipo, valor, data, descricao, pago) VALUES (?, ?, ?, ?, ?, ?)",
                       (categoria, tipo, valor, data, descricao, pago))
        conn.commit()
        animacao = QPropertyAnimation(self.btn_add, b"geometry")
        animacao.setDuration(200) 
        animacao.setStartValue(self.btn_add.geometry())
        animacao.setEndValue(self.btn_add.geometry().adjusted(0, -5, 0, -5)) 
        animacao.start()
        self.carregar_dados()

    def carregar_dados(self):
        cursor.execute("SELECT categoria, tipo, valor, data, descricao, pago FROM lancamentos ORDER BY data DESC")
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(["Categoria", "Tipo", "Valor", "Data", "Descrição", "Pago"])
        dados = cursor.fetchall()

        self.tabela.setRowCount(len(dados))
        total_receita = 0
        total_despesa = 0

        for row_idx, row_data in enumerate(dados):
            Categoria, tipo, valor, data, descricao, pago = row_data
            
            for col_idx, item in enumerate(row_data):
                cell = QTableWidgetItem(str(item))
                cell.setForeground(QColor("#FFFFFF"))
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabela.setItem(row_idx, col_idx, cell)

            if tipo == "Despesa":
                tipo_cell = QTableWidgetItem(tipo)
                tipo_cell.setForeground(QColor("#dc3545"))
                tipo_cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabela.setItem(row_idx, 1, tipo_cell)  
                total_despesa += valor

            elif tipo == "Receita":
                tipo_cell = QTableWidgetItem(tipo)
                tipo_cell.setForeground(QColor("#28a745"))
                tipo_cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabela.setItem(row_idx, 1, tipo_cell) 
                total_receita += valor

            pago_cell = QTableWidgetItem("✅" if pago == 1 else "❌")
            pago_cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabela.setItem(row_idx, 5, pago_cell)

        if dados:
            ultimo = dados[0]
            self.hist_label.setText(f"Último lançamento: {float(ultimo[2]):.2f} R$ | {ultimo[0]} | {ultimo[1]}")
        else:
            self.hist_label.setText("Nenhum lançamento registrado.")

        saldo = total_receita - total_despesa
        self.total_label.setText(f" Receita Total: {total_receita:.2f} R$ |  Despesa Total: {total_despesa:.2f} R$ |  Saldo Mensal: {saldo:.2f} R$")

    def limpar_registros(self):
        cursor.execute("DELETE FROM lancamentos")
        conn.commit()
        self.carregar_dados()

    def excluir_ultimo_lancamento(self):
        cursor.execute("SELECT id FROM lancamentos ORDER BY id DESC LIMIT 1")
        ultimo_registro = cursor.fetchone()

        if ultimo_registro:
            cursor.execute("DELETE FROM lancamentos WHERE id = ?", (ultimo_registro[0],))
            conn.commit()
            self.carregar_dados()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Nenhum lançamento encontrado")
            msg.setText("Não há registros para excluir.")
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #262626;
                    color: #FFD700;
                    font-size: 16px;
                    border: 2px solid #444;
                }
                QLabel {
                    color: #FFD700;
                    font-weight: bold;
                }
               QPushButton {
                    background-color: #007bff;
                    color: white;
                    font-weight: bold;
                    border-radius: 5px;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
            """)
            msg.exec()

app = QApplication(sys.argv)
janela = FinanceiroApp()
janela.show()
sys.exit(app.exec())