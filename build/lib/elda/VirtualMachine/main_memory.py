from .virtual_memory import VirtualMemory
from collections import OrderedDict


class MainMemory:
    """
    Memory that handles global program memory, local memory for the main function and constants.
    """

    def __init__(self):
        """
        Initializes the execution counter on 0 and all memories empty. Sets the active_record as None.
        """
        self.counter_execution = 0

        self.memory_global = {}
        self.memory_constants = {}

        self.memory_local = {}

        self.memory_execution = OrderedDict()

        self.base_execution = 50000

        self.active_record = None

    def add_scope(self, parent, size):
        """
        Adds a new scope (function) into the memory_execution. Raises TypeError if the execution stack is filled.
        :param parent: The function in which the called function is called
        :param size: The size of the function
        """
        new_scope = VirtualMemory(parent, size)

        if self.counter_execution + size > 50000:
            raise TypeError(f"Stack Overflow: The execution stack was filled.")

        address = self.base_execution + self.counter_execution

        self.counter_execution = self.counter_execution + size
        self.memory_execution[address] = new_scope

    def remove_scope(self):
        """
        Removes a scope from the memory_execution and sets is parent as active.
        """
        if self.active_record is not None:
            self.active_record = self.active_record.parent if self.active_record.parent is not self else None
            record = list(self.memory_execution.keys())[-1]
            self.counter_execution -= self.memory_execution[record].size
            del self.memory_execution[record]
