# bananaPiM4Zero
Tutorial de como instalar o Armbian no BananaPi M4 zero e configurar o que for necessário para usar na placa de robótica.

Como a versão utilizada é a de 8Gb de eMMC, devemos baixar a versão do armbian baseada em debian 12, versão Minimal(IoT). A atual no momento da criação do manual é a Armbian 25.2.2 Bookworm Minimal.

Agora devemos instalar no cartão SD, dar boot, configurar inicialmente a instação e depois instalar no eMMC usando o armbian-config.

Após isso, ligue a placa no pelo eMMC e altere o arquivo /boot/armbianEnv.txt
Insira a linha *overlays=bananapi-m4-sdio-wifi-bt* para o wifi funcionar.
Reinicie a placa novamente, agora no armbian-config conecte no wifi para poder instalar e atualizar os demais itens.

Para as duas portas usbC funcionarem como HOST, precisamos alterar a configuração do conector CN2 (USB0) para isso precisamos editar o arquivo DTB dele. E alterar as linhas para desativar o USB OTG e ATIVAR os dois modos HOSTs ta porta USB0.

* Atualize o APT (sudo apt update)
* Instale o net-tools (sudo apt install net-tools)
* Instale o ambiente gráfico XFCE pelo armbian-config
* Instale o python3-full (sudo apt install python3-full)
* Instale o python3-pip e o pipx (sudo apt install python3-pip pipx)
* Instale o ultralytics usando um ambiente virtual personalizado:
    * python -m venv meu_venv
    * source meu_venv/bin/activate  
    * pip install ultralytics
    * python meu_script.py (como rodar o script)
* Para utilizar as seriais no python é necessário instalar a biblioteca serial (pip install serial pyserial), ATENÇÂO, sempre que for usar o PIP, você deve usar o comando "source meu_venv/bin/activate" antes (caso ainda nao esteja com o ambiente personalizado já aberto)
* Para acessar os pinos GPIO do BananaPI é necessário instalar a biblioteca (python3-libgpiod)
     * Instale python3-libgpiod (sudo apt install python3-libgpiod)
     * Crie o grupo (sudo groupadd gpio)
     * Adicione o usuario ao grupo de GPIO (sudo usermod -aG gpio $USER)
     * Crie o arquivo gipo-rules "sudo nano /etc/udev/rules.d/99-gpio.rules"
          * Dentro do arquivo adicione KERNEL=="gpio*", GROUP="gpio", MODE="0660"
      * Recarregue as regras do udev
         * sudo udevadm control --reload-rules
         * sudo udevadm trigger
      * Reinicie a placa
* Para acessar os sensores i2c é necessário instalar o modulo adafruit-blinka (pip install adafruit-blinka)
* Para utilizar o sensor de cor TCS34725 via porta i2c é necessário instalar o módulo adafruit-circuitpython-tcs34725 (pip install adafruit-circuitpython-tcs34725)
* Para usar o PWM é necessario fazer um overlay, para isso, baixe o arquivo pwm-pi12.dts, coloque na pasta do usuario e rode o comando
     *
