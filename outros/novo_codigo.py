import sys, socket
import plotly.graph_objects as go
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from cryptography.fernet import Fernet


# Funções
def encrypt(message, key):
    cipher_suite = Fernet(key)
    ciphertext = cipher_suite.encrypt(message.encode())
    return ciphertext.decode()


def text_to_binary(message):
    binary_message = ' '.join(format(ord(char), '08b') for char in message)
    return binary_message


def nrz_encoding(binary_message):
    signal = []
    for bit in binary_message:
        if bit == '0':
            signal.extend([-1, -1])  # Codifica '0' como sinal negativo
        elif bit == '1':
            signal.extend([1, 1])  # Codifica '1' como sinal positivo
    return signal


def rz_encoding(binary_message):
    signal = []
    for bit in binary_message:
        if bit == '0':
            signal.extend([0] * 2)  # Codifica '0' como sinal zero
        elif bit == '1':
            signal.extend([1, -1])  # Codifica '1' como sinal positivo seguido de sinal negativo
    return signal


def about(message):
    # Gerar uma nova chave válida para uso com o algoritmo Fernet
    key = Fernet.generate_key()
    # Criptografa a mensagem
    mensagem_criptografada = encrypt(message, key)
    mensagem_binaria = text_to_binary(mensagem_criptografada)
    # Codifica em NRZ
    mensagem_codificada_nrz = nrz_encoding(mensagem_binaria)
    # Codifica em RZ
    mensagem_codificada_rz = rz_encoding(mensagem_binaria)

    return message, mensagem_criptografada, key, mensagem_binaria, mensagem_codificada_nrz, mensagem_codificada_rz


def plot_graphs(mensagem_codificada_nrz, mensagem_codificada_rz):
    # Criação do gráfico NRZ utilizando Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(mensagem_codificada_nrz))), y=mensagem_codificada_nrz, mode='lines'))

    fig.update_layout(
        title="Codificação NRZ",
        xaxis_title="Tempo",
        yaxis_title="Nível de Sinal"
    )
    fig.show()

    # Criação do gráfico RZ utilizando Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(mensagem_codificada_rz))), y=mensagem_codificada_rz, mode='lines'))

    fig.update_layout(
        title="Codificação RZ",
        xaxis_title="Tempo",
        yaxis_title="Nível de Sinal"
    )
    fig.show()

def ip_config_emissor(mensagem_codificada):
    # Obtém o nome do host
    hostname = socket.gethostname()

    # Obtém o endereço IP associado ao nome do host
    ip_address = socket.gethostbyname(hostname)
    # Coloca o ip do emissor na variável ip_address
    ip_address = socket.gethostbyname(socket.gethostname())

    HOST = ip_address # Endereço IP do receptor
    PORT = 12345  # Porta de comunicação
    # Cria o socket TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta ao receptor
    s.connect((HOST, PORT))

    # Envia a mensagem codificada
    s.sendall(mensagem_codificada.encode())

    # Fecha o socket
    s.close()


class OutputWindow(QtWidgets.QMainWindow):
    def __init__(self, message,mensagem_criptografada, key, binary_message, nrz_signal, rz_signal):
        super(OutputWindow, self).__init__()
        self.setWindowTitle("Output Window")
        self.setGeometry(100, 100, 600, 400)

        self.text_edit = QtWidgets.QTextEdit(self)
        self.text_edit.setGeometry(QtCore.QRect(10, 10, 580, 380))
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QtGui.QFont("Courier", 10))
        self.text_edit.append("Mensagem original: {}".format(message))
        self.text_edit.append("\n")
        self.text_edit.append("Mensagem criptografada: {}".format(mensagem_criptografada))
        self.text_edit.append("\n")
        self.text_edit.append("Chave utilizada: {}".format(key))
        self.text_edit.append("\n")
        self.text_edit.append("Mensagem em binário: {}".format(binary_message))
        self.text_edit.append("\n")
        self.text_edit.append("Sinal codificado NRZ: {}".format(nrz_signal))
        self.text_edit.append("\n")
        self.text_edit.append("Sinal codificado RZ: {}".format(rz_signal))


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(721, 501)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 390, 721, 111))
        self.frame.setStyleSheet("background-color: rgb(216, 216, 216);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.message_line = QtWidgets.QLineEdit(self.frame)
        self.message_line.setGeometry(QtCore.QRect(10, 20, 221, 20))
        self.message_line.setObjectName("message_line")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 0, 141, 16))
        self.label_2.setObjectName("label_2")
        self.plot_button = QtWidgets.QPushButton(self.frame)
        self.plot_button.setGeometry(QtCore.QRect(380, 20, 75, 23))
        self.plot_button.setObjectName("plot_button")
        self.plot_button.clicked.connect(self.plot_button_clicked)
        self.load_button = QtWidgets.QPushButton(self.frame)
        self.load_button.setGeometry(QtCore.QRect(250, 20, 95, 23))
        self.load_button.setObjectName("load_button")
        self.load_button.clicked.connect(self.load_button_clicked)
        self.send_button = QtWidgets.QPushButton(self.frame)
        self.send_button.setGeometry(QtCore.QRect(510, 20, 75, 23))
        self.send_button.setObjectName("send_button")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 721, 391))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)

        self.output_window = None  # Variável de instância para a janela de saída

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Digite o texto aqui:"))
        self.plot_button.setText(_translate("MainWindow", "Plotar"))
        self.load_button.setText(_translate("MainWindow", "Carregar Dados"))
        self.send_button.setText(_translate("MainWindow", "Enviar"))

    def plot_button_clicked(self):
        message = self.message_line.text()
        if not message:
            QMessageBox.warning(MainWindow, "Atenção", "Digite uma mensagem antes de plotar.")
            return

        message,mensagem_criptografada, key, mensagem_binaria, mensagem_codificada_nrz,mensagem_codificada_rz = about(message)
        plot_graphs(mensagem_codificada_nrz,mensagem_codificada_rz)

    def load_button_clicked(self):
        message = self.message_line.text()
        if not message:
            QMessageBox.warning(MainWindow, "Atenção", "Digite uma mensagem antes de carregar.")
            return

        message, mensagem_criptografada, key, binary_message, mensagem_codificada_nrz, mensagem_codificada_rz = about(message)

        self.output_window =  OutputWindow(message, mensagem_criptografada, key, binary_message, mensagem_codificada_nrz, mensagem_codificada_rz)

        self.output_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
