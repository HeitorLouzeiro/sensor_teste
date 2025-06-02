# Integração MPU6050 + Servo Motor
# Giroscópio controla movimento do servo

import machine
from machine import Pin, I2C, PWM
from imu import MPU6050
from time import sleep
import math


# LED para indicar funcionamento
LED = machine.Pin("LED", machine.Pin.OUT)
LED.on()

# Configuração do I2C para MPU6050
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)  # Pico
imu = MPU6050(i2c)

# Configuração do Servo Motor no pino GP16
servo = PWM(Pin(16))
servo.freq(50)  # Frequência padrão para servos: 50Hz

def mapear_valor(valor):
    valor = max(min(valor, 90), -90)  # Limita entre -90 e 90
    return int(5000 + (valor / 90) * 4000)  # Mapeia para 5000-15000us


def mover_servo(angulo):
    """
    Move o servo para o ângulo especificado (0-180 graus)
    """
    # Limita o ângulo entre 0 e 180
    angulo = max(0, min(180, angulo))
    
    # Conversão: ângulo 0-180 para ciclo duty entre 1638 (0.5ms) e 8191 (2.5ms)
    min_duty = 1638
    max_duty = 8191
    duty = int(min_duty + (angulo / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)
    return angulo

def mapear_gyro_para_servo(valor_gyro, sensibilidade=1.0):
    """
    Converte valor do giroscópio para ângulo do servo
    valor_gyro: valor do eixo Y do giroscópio (-32768 a 32767)
    sensibilidade: ajusta a resposta (1.0 = normal, 0.5 = menos sensível)
    """
    # Normaliza o valor do giroscópio para 0-180 graus
    # Considera que valores típicos do gyro estão entre -200 e +200
    max_gyro = 200 * sensibilidade
    
    # Mapeia de -max_gyro/+max_gyro para 0-180 graus
    angulo = 90 + (valor_gyro / max_gyro) * 90
    
    # Garante que está no range válido
    return max(0, min(180, angulo))

print("=== Sistema MPU6050 + Servo Iniciado ===")
print("Incline o sensor para controlar o servo motor")
print("Pressione Ctrl+C para parar")

# Variáveis para controle
posicao_servo = 90  # Posição inicial central
sensibilidade = 0.8  # Ajuste a sensibilidade conforme necessário


ultimo_valor = 0  # Para controle de movimento suave
try:
    while True:
        # Lê os dados do sensor
        ax = round(imu.accel.x, 2)
        ay = round(imu.accel.y, 2)
        az = round(imu.accel.z, 2)
        gx = round(imu.gyro.x)
        gy = round(imu.gyro.y)  # Usaremos este eixo para controlar o servo
        gz = round(imu.gyro.z)
        
        giro = gy   
        
        if abs(giro) > 1:
            ultimo_valor += giro * 0.02  # Acumula o valor do giroscópio para suavizar o movimento
            ultimo_valor = max(min(ultimo_valor, 90), -90)
        
        duty = mapear_valor(ultimo_valor)
        servo.duty_u16(duty)
        sleep(0.02)  # Aguarda um pouco para evitar sobrecarga
        

except KeyboardInterrupt:
    print("\nParando sistema...")
    servo.deinit()  # Desliga o PWM do servo
    LED.off()
    print("Sistema parado.")