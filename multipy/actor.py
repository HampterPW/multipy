"""Actor-based concurrency utilities."""
from __future__ import annotations

from queue import Queue
from threading import Thread
from typing import Any, Callable
import time


def actor(func: Callable[[Any], None]) -> Callable[[], Queue]:
    """Decorator to create an actor."""
    def start(*args: Any, **kwargs: Any) -> Queue:
        inbox: Queue = Queue()

        def loop() -> None:
            while True:
                msg = inbox.get()
                if msg is None:
                    break
                func(msg, *args, **kwargs)

        Thread(target=loop, daemon=True).start()
        return inbox

    return start


def send(actor_inbox: Queue, message: Any) -> None:
    actor_inbox.put(message)


if __name__ == "__main__":
    @actor
    def printer(msg: str) -> None:
        print('actor received:', msg)

    inbox = printer()
    send(inbox, 'hello')
    send(inbox, None)  # stop
    time.sleep(0.1)
