# flake8: noqa: E501

from datetime import datetime


def mask_hours(seg: float):
    seconds = int(seg)
    hours = int(seconds / 3600)
    seconds = int(seconds) % 3600
    minutes = int(seconds / 60)
    seconds = int(seconds) % 60
    milisseconds = int((seg - int(seg)) * 1000)
    return f"{hours:02}h {minutes:02}m {seconds:02}s {milisseconds:03}ms"


def log_info(id: str, msg: str, total: int | None = None, just: int = 60):
    id_str = f"{id}".ljust(4)[0:4]
    d = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"
    msg = f"{msg.strip().replace('\n', '')}".ljust(just)[0:just]
    total_str = f" | Total: {mask_hours(total)}" if total is not None else ""
    print(f"* {id_str} | [INFO] {d} | {msg}{total_str}")
