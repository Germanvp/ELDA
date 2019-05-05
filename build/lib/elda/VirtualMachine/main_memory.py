from .virtual_memory import VirtualMemory
from collections import OrderedDict


class MainMemory:

    def __init__(self):
        self.counter_execution = 0

        self.memory_global = {}
        self.memory_constants = {}

        self.memory_local = {}

        self.memory_execution = OrderedDict()

        self.base_execution = 50000

        self.active_record = None

    def add_scope(self, parent, size):
        new_scope = VirtualMemory(parent, size)

        if self.counter_execution + size > 50000:

            raise TypeError(f"Stack Overflow: The execution stack was filled.")

        address = self.base_execution + self.counter_execution

        self.counter_execution = self.counter_execution + size
        # print(self.counter_execution)

        # self.active_record = new_scope
        self.memory_execution[address] = new_scope

    def remove_scope(self):
        if self.active_record is not None:
            self.active_record = self.active_record.parent if self.active_record.parent is not self else None
            record = list(self.memory_execution.keys())[-1]
            self.counter_execution -= self.memory_execution[record].size
            del self.memory_execution[record]

    # def insert_into_memory(self, address_variable, address_value):
    #     """
    #     Inserta variable en memoria y regresa su direccion para que la puedas
    #     poner en la tabla de variables.
    #     """
    #     ## TODO: Cala esto esta cnmadre, se pone una palomita y todo.
    #     ### Hay que ver si esto esta bien, estoy 90% seguro que no.
    #
    #     if self.active_record is None:
    #         self.memory_global[address_variable] = address_value
    #     else:
    #         self.active_record.memory_local[address_variable] = address_value
