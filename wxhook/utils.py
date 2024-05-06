import os
import json
import typing
import pathlib
import subprocess

import psutil
import xmltodict

BASE_DIR = pathlib.Path(__file__).resolve().parent
TOOLS = BASE_DIR / "tools"
DLL = TOOLS / "wxhook.dll"
START_WECHAT = TOOLS / "start-wechat.exe"
FAKER = TOOLS / "faker.exe"


def start_wechat_with_inject(port: int) -> typing.Tuple[int, str]:
    result = subprocess.run(f"{START_WECHAT} {DLL} {port}", capture_output=True, text=True)
    code, output = result.stdout.split(",")
    return int(code), output


def fake_wechat_version(pid: int, old_version: str, new_version: str) -> int:
    result = subprocess.run(f"{FAKER} {pid} {old_version} {new_version}", capture_output=True, text=True)
    return int(result.stdout)


def get_processes(process_name: str) -> typing.List[psutil.Process]:
    processes = []
    for process in psutil.process_iter():
        if process.name().lower() == process_name.lower():
            processes.append(process)
    return processes


def get_pid(port: int) -> typing.Tuple[int, int]:
    output = subprocess.run(f"netstat -ano | findStr \"{port}\"", capture_output=True, text=True, shell=True).stdout
    return 0, int(output.split("\n")[0].split("LISTENING")[-1])


def parse_xml(xml: str) -> dict:
    return xmltodict.parse(xml)


def parse_event(event: dict, fields=None) -> dict:
    for field in fields or ["content", "signature"]:
        try:
            if field in event:
                event[field] = parse_xml(event[field])
        except Exception:
            pass
    return event


class WeChatManager:

    def __init__(self):
        # remote port: 19001 ~ 37999
        # socket port: 18999 ~ 1
        # http port:   38999 ~ 57997
        self.filename = BASE_DIR / "tools" / "wxhook.json"
        if not os.path.exists(self.filename):
            self.init_file()
        else:
            self.clean()

    def init_file(self) -> None:
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump({
                "increase_remote_port": 19000,
                "wechat": []
            }, file)

    def read(self) -> dict:
        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def write(self, data: dict) -> None:
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file)

    def refresh(self, pid_list: typing.List[int]) -> None:
        data = self.read()
        cleaned_data = []
        remote_port_list = [19000]
        for item in data["wechat"]:
            if item["pid"] in pid_list:
                remote_port_list.append(item["remote_port"])
                cleaned_data.append(item)

        data["increase_remote_port"] = max(remote_port_list)
        data["wechat"] = cleaned_data
        self.write(data)

    def clean(self) -> None:
        pid_list = [process.pid for process in get_processes("WeChat.exe")]
        self.refresh(pid_list)

    def get_remote_port(self) -> int:
        data = self.read()
        return data["increase_remote_port"] + 1

    def get_listen_port(self, remote_port: int) -> int:
        return 19000 - (remote_port - 19000)

    def get_port(self) -> typing.Tuple[int, int]:
        remote_port = self.get_remote_port()
        return remote_port, self.get_listen_port(remote_port)

    def add(self, pid: int, remote_port: int, server_port: int) -> None:
        data = self.read()
        data["increase_remote_port"] = remote_port
        data["wechat"].append({
            "pid": pid,
            "remote_port": remote_port,
            "server_port": server_port
        })
        self.write(data)
