import subprocess
import os
import ctypes
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())


class VPNManager:
    def __init__(self):
        self.CLI_PATH = os.getenv("CLI_PATH")
        self.CONFIG_PATH = os.getenv("CONFIG_PATH")
        self.TUNNEL_NAME = os.path.splitext(os.path.basename(self.CONFIG_PATH))[0]

        if not self.is_admin():
            print("ВНИМАНИЕ: Скрипт запущен без прав Администратора!")

        self.connect_vpn()

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    def connect_vpn(self):
        """Включить VPN"""
        print("Подключение к VPN (AmneziaWG)...")
        try:
            result = subprocess.run(
                [self.CLI_PATH, "/installtunnelservice", self.CONFIG_PATH],
                capture_output=True, text=True, check=True
            )
            print("Статус: VPN успешно запущен и работает.")
        except subprocess.CalledProcessError as e:
            if "already exists" in e.stderr or "already exists" in e.stdout or e.returncode == 1:
                print("Статус: VPN уже был включен ранее.")
            else:
                print(f"Ошибка при подключении: {e.stderr or e.stdout}")

    def disconnect_vpn(self):
        print("Отключение от VPN...")
        try:
            subprocess.run(
                [self.CLI_PATH, "/uninstalltunnelservice", self.TUNNEL_NAME],
                capture_output=True, text=True, check=True
            )
            print("Штатная команда на отключение отправлена.")
        except subprocess.CalledProcessError:
            pass  # Игнорируем, если утилита считает, что туннеля уже нет

        # 2. Жёсткое завершение процессов службы (Taskkill)
        # AmneziaWG создает службу с именем 'amneziawg-tunnel' или по имени конфига
        try:
            # Убиваем системные процессы, которые могут удерживать соединение
            subprocess.run(["taskkill", "/F", "/IM", "amneziawg.exe"], capture_output=True, text=True)
            subprocess.run(["taskkill", "/F", "/IM", "awg.exe"], capture_output=True, text=True)
        except Exception:
            pass

        # 3. Очистка сетевого кэша Windows (чтобы вернуть родной IP)
        try:
            subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True)
            print("Статус: VPN полностью отключен, сетевой кэш сброшен.")
        except Exception as e:
            print(f"Не удалось очистить кэш DNS: {e}")

    def wait(self):
        pass

    def __del__(self):
        self.disconnect_vpn()
