from machine import Pin, PWM
import time

# Configura o pino GP15 como PWM
servo = PWM(Pin(16))
servo.freq(50)  # Frequência padrão para servos: 50Hz

def mover_servo(angulo):
    # Conversão: ângulo 0-180 para ciclo duty entre 1638 (0.5ms) e 8191 (2.5ms)
    min_duty = 1638
    max_duty = 8191
    duty = int(min_duty + (angulo / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)
    print(f"Servo movido para {angulo} graus")

while True:
    # Vai de 0 até 180 graus
    for angulo in range(0, 181, 1):
        mover_servo(angulo)
        time.sleep(0.02)
    
    # Volta de 180 até 0 graus
    for angulo in range(180, -1, -1):
        mover_servo(angulo)
        time.sleep(0.02)
