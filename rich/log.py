from datetime import datetime
from typing import Any, List, Optional

from .console import Console, ConsoleRenderable, RenderableType
from .containers import Renderables
from .table import Table
from .text import Text


class Logger:
    def __init__(
        self,
        console: Console,
        show_time: bool = True,
        show_path: bool = True,
        time_format: str = "[%x %X] ",
    ) -> None:
        self.console = console
        self.show_time = show_time
        self.show_path = show_path
        self.time_format = time_format
        self._last_time: Optional[datetime] = None

    def __call__(
        self,
        *objects: Any,
        log_time: datetime = None,
        path: str = None,
        line_no: int = None,
    ) -> None:
        output = Table(show_header=False, expand=True, box=None, padding=0)
        if self.show_time:
            output.add_column(style="log.time")
        output.add_column(ratio=1, style="log.message")
        if self.show_path and path:
            output.add_column(style="log.path")
        row: List[RenderableType] = []
        if self.show_time:
            if log_time is None:
                log_time = datetime.now()
            row.append(Text(log_time.strftime(self.time_format)))
        row.append(Renderables(objects))
        if self.show_path and path:
            if line_no is None:
                row.append(Text(path))
            else:
                row.append(Text(f"{path}:{line_no}"))
        output.add_row(*row)

        self.console.print(output)


if __name__ == "__main__":
    console = Console()
    print(console)
    logger = Logger(console)

    logger("Hello", path="foo.py", line_no=20)