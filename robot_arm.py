import serial
import time
import numpy as np
# import master_control

# # # 아두이노와 시리얼 통신 설정
port = 'COM3'
arduino = serial.Serial(port, 9600)  # 'COM포트'는 아두이노가 연결된 포트로 수정
time.sleep(2)  # 시리얼 통신 시작 후 잠시 대기

# 링크 길이 정의
link1_length = 12.0
link3_length = 12.0
link4_length = 10.0

def inverse_kinematics(x_target, y_target, z_target):
    # 목표점까지의 거리 계산
    d = np.sqrt(x_target ** 2 + y_target ** 2 + z_target ** 2)
    d_prime = np.sqrt((y_target - 10) ** 2 + z_target ** 2)

    # 가능한 위치인지 체크
    if d_prime > np.sqrt( link1_length ** 2 + link3_length ** 2 ):
        raise ValueError("Target is unreachable")

    # 어깨 관절 각도 계산 (평면에 대한 회전)
    theta1 = np.arctan2(y_target, x_target)

    # Inverse Kinematics 공식을 사용하여 theta2와 theta3를 계산합니다.
    cos_theta3 = (d_prime ** 2 - link1_length ** 2 - link3_length ** 2) / (2 * link1_length * link3_length)
    # 여기서 cos_theta3의 값이 [-1, 1] 범위 내에 있는지 확인합니다.
    if not -1 <= cos_theta3 <= 1:
        raise ValueError("cos_theta3 out of range, invalid target position")

    # cos_theta3 값에 따라 theta3 계산
    theta3 = np.arccos(cos_theta3)

    # theta2 계산
    sin_theta3 = np.sqrt(1 - (cos_theta3 ** 2))
    k1 = link1_length + (link3_length * cos_theta3)
    k2 = link3_length * sin_theta3

    theta2 = np.arctan2((y_target - 10), z_target) - np.arctan2(k2, k1)


    # 각도를 도(degree)로 변환
    theta1_deg = np.degrees(theta1)
    theta2_deg = np.degrees(theta2)
    theta3_deg = np.degrees(theta3)

    theta4_deg = 90 - theta2_deg - theta3_deg

    return theta1_deg, theta2_deg, theta3_deg, theta4_deg

def set_motor_speed(right_speed, left_speed):
    command = f"M1{left_speed}\nM2{right_speed}\n"
    arduino.write(command.encode())

def set_servo_angle( servo_number, angle):
    command = f"S{servo_number}{angle}\n"
    arduino.write(command.encode())

# 사용자 입력 처리
while True:
    try:
        command_type = input("Enter command type ('servo' or 'motor'): ")
        if command_type == "s":

            # (x,y,z)값으로 나타내기
            x_target = 0.0
            y_target = float(input("Enter y_target: "))
            z_target = float(input("Enter z_target: "))

            theta1, theta2, theta3, theta4 = inverse_kinematics(x_target, y_target, z_target)

            if theta2 <= 90:
                theta2 = 90 - theta2
            if theta4 <= 90:
                theta4 = 90 - theta4

            print(f"Link1 joint angle: {theta2}")
            print(f"Link3 joint angle: {theta3}")
            print(f"Link4 joint angle: {theta4}")
            #
            # set_servo_angle(1, theta2)
            # time.sleep(1)
            # set_servo_angle(2, theta3)
            # time.sleep(1)
            # set_servo_angle(3, theta4)
            # time.sleep(1)
            # set_servo_angle(4, 10)  # 임의의 값
            # time.sleep(1)


        elif command_type == "m":
            motorSpeedRight = int(input("Enter PWM value for right motor (negative for reverse): "))
            motorSpeedLeft = int(input("Enter PWM value for left motor (negative for reverse): "))
            set_motor_speed(motorSpeedRight, motorSpeedLeft)

    except KeyboardInterrupt:
        break
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# arduino.close()