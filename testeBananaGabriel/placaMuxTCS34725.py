import struct
import threading
import time
from cronometro import Cronometro
from portas import Portas
class PlacaMuxTCS34725:

    RGB_4X = 0
    RGB_16X = 1
    RGB_4X_LED_OFF = 2
    RGB_16X_LED_OFF = 3
    modo = 0
    quantidadeBytesModo = 32;

    
    def __init__(self, portaSerial):
        self.lista = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        portas = Portas()
        self.ser = portas.abrePortaSerial(portaSerial, 115200)
        if self.ser == None:
            raise Exception("Erro ao abrir a porta serial da placa mux TCS34725")
        self.setModo(self.RGB_4X)
        self._thread_ativa = False
        self._thread = None
        self._iniciarThread()
        
    def __del__(self):
        """Destrutor da classe. Para a thread e fecha a porta serial."""
        self._pararThread()
        if self.ser is not None:
            self.ser.close()

    def _atualizaPeriodicamente(self):
        """Função que chama `atualiza` a cada 25ms."""
        while self._thread_ativa:
            self.atualiza()
            time.sleep(0.025)  # 25ms

    def _iniciarThread(self):
        """Inicia a thread para chamar `atualiza` periodicamente."""
        if not self._thread_ativa:
            self._thread_ativa = True
            self._thread = threading.Thread(target=self._atualizaPeriodicamente)
            self._thread.daemon = True  # Permite que o programa principal encerre mesmo com a thread ativa
            self._thread.start()

    def _pararThread(self):
        """Para a thread que chama `atualiza`."""
        self._thread_ativa = False
        if self._thread is not None:
            self._thread.join()

    def setModo(self, modo):
        if modo < 0 or modo >= 4:
            raise ValueError("Modo inválido. Deve ser 0, 1, 2 ou 3")
        self.modo = modo

    def atualiza(self):
        #limpo o buffer de entrada
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        # Envia o comando para solicitar o bytes necessarios
        self.ser.write(bytes([self.modo]))
        
        # Aguarda receber os self.quantidadeBytesModo bytes via serial
        dados = self.ser.read(self.quantidadeBytesModo)
        
        # Verifica se recebeu exatamente self.quantidadeBytesModo bytes
        if len(dados) == self.quantidadeBytesModo:
            # Atualiza a lista com os valores recebidos
            self.lista = list(dados)
            return True
        else:
            return False

    def leSensor(self, porta):
        # Atualiza os dados antes de ler
        if porta < 0 or porta > 3:
            raise ValueError("Porta inválida. Deve ser 0, 1, 2 ou 3.")
        # tenho que usar struct pra pegar dois bytes da lista e transformar em inteiro com sinal
        indice = porta * 4
        r = struct.unpack('>h', bytes(self.lista[indice:indice+2]))[0]
        g = struct.unpack('>h', bytes(self.lista[indice+2:indice+4]))[0]
        b = struct.unpack('>h', bytes(self.lista[indice+4:indice+6]))[0]
        c = struct.unpack('>h', bytes(self.lista[indice+6:indice+8]))[0]
        return (r, g, b, c)
