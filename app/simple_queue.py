import json
import os
import logging
import threading
import time
from collections import deque
from tenacity import retry, stop_after_attempt, wait_fixed

logger = logging.getLogger(__name__)

class SimpleQueue:
    def __init__(self, queue_name, persistence=True):
        self.queue_name = queue_name
        self.queue = deque()
        self.persistence = persistence
        self.queue_file = f"{queue_name}.json" if persistence else None
        self.lock = threading.Lock()
        self._load_from_file()
        logger.info(f"Initialized Simple Queue: {queue_name}")

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def _load_from_file(self):
        """Load queue from file if persistence is enabled."""
        if self.persistence and os.path.exists(self.queue_file):
            with open(self.queue_file, "r") as f:
                try:
                    data = json.load(f)
                    self.queue = deque(data)
                    logger.info(f"Queue '{self.queue_name}' loaded from file.")
                except json.JSONDecodeError:
                    logger.warning(
                        f"Invalid JSON in queue file: {self.queue_file}, creating new queue"
                    )
                    self.queue = deque()
        else:
            logger.info(
                f"Queue '{self.queue_name}' doesn't exist or persistence disabled, creating new queue"
            )
            self.queue = deque()

    def _save_to_file(self):
         """Save queue to file if persistence is enabled."""
         if self.persistence:
             try:
                 with self.lock:
                     with open(self.queue_file, "w") as f:
                       json.dump(list(self.queue), f)
                 logger.debug(f"Queue '{self.queue_name}' saved to file.")
             except IOError as e:
                 logger.error(f"Error writing to queue file: {e}")

    def enqueue(self, message):
        """Adds message to the end of the queue."""
        with self.lock:
             self.queue.append(message)
        self._save_to_file()
        logger.debug(f"Enqueued message to '{self.queue_name}': {message}")

    def dequeue(self):
        """Removes and returns the first message from the queue. Returns None if queue is empty."""
        with self.lock:
             if self.queue:
                message = self.queue.popleft()
                self._save_to_file()
                logger.debug(f"Dequeued message from '{self.queue_name}': {message}")
                return message
             else:
                logger.debug(f"Queue '{self.queue_name}' is empty.")
                return None

    def peek(self):
        """Returns the first message from the queue without removing it. Returns None if the queue is empty."""
        with self.lock:
             if self.queue:
                return self.queue[0]
             else:
                logger.debug(f"Queue '{self.queue_name}' is empty.")
                return None
    
    def size(self):
        """Returns the size of the queue"""
        with self.lock:
            return len(self.queue)

    def clear(self):
        """Clears the queue"""
        with self.lock:
            self.queue.clear()
        self._save_to_file()
        logger.debug(f"Queue '{self.queue_name}' cleared.")