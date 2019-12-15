#!/usr/bin/env python3
from dataclasses import field, dataclass
from functools import partial
from typing import Tuple, List, Dict
import asyncio
import inspect

Val = Tuple[int, int]


@dataclass
class Pipe:
    """
    This class facilitates communication between multiple IntPuter processes or an IntPuter and peripheral devices.

    Internally, it uses a list to store queued data and a semaphore to block if there is no available data to read.
    """
    semaphore: asyncio.Semaphore = field(default_factory=partial(asyncio.Semaphore, 0))
    data: List[int] = field(default_factory=list)

    async def dequeue(self) -> int:
        """
        Get the first stored item, waiting for data if there isn't any
        """
        await self.semaphore.acquire()
        return self.data.pop(0)

    def peek(self) -> int:
        """
        Gets the first item in the queue without removing it.
        """
        if self.data:
            return self.data[0]

    def enqueue(self, val: int) -> None:
        """
        Add a new item to the back of the queue
        """
        self.data.append(val)
        self.semaphore.release()

    def clear(self) -> None:
        """
        Clear the data list and re-create the semaphore to use in a second run.
        """
        self.data.clear()
        self.semaphore = asyncio.Semaphore(0)


class IntPuter:
    """
    This class is the IntPuter interpreter. It supports a number of different opcodes of various sizes and can be run in
    asynchronous mode with other instances or external peripherals using Pipes for communication.
    """
    # Initial loaded code, for resets
    __code: List[int] = []
    # Current copy of the code
    code: List[int] = []
    # Instruction pointer
    ptr: int = 0
    # Relative memory base
    rel_base: int = 0
    # Whether or not the program has ended
    ended: bool = False
    # I/O pipes
    input_pipe: Pipe = None
    output_pipe: Pipe = None

    def __init__(self, code: str, input_pipe: Pipe = None, output_pipe: Pipe = None):
        self.__code = [int(x) for x in code.split(',')]
        self.input_pipe = input_pipe
        self.output_pipe = output_pipe
        self.reset()

    def op_add(self, o1: Val, o2: Val, r: Val) -> None:
        self.set_value(r, self.load_val(o1) + self.load_val(o2))

    def op_mul(self, o1: Val, o2: Val, r: Val) -> None:
        self.set_value(r, self.load_val(o1) * self.load_val(o2))

    async def op_input(self, r: Val) -> None:
        if self.input_pipe:
            val = await self.input_pipe.dequeue()
        else:
            val = int(input("Input Required:"))
        self.set_value(r, val)

    async def op_output(self, i: Val) -> None:
        val = self.load_val(i)
        if self.output_pipe is not None:
            self.output_pipe.enqueue(val)
            # Relinquish control to the event loop allowing other processes to run.
            await asyncio.sleep(0)
        else:
            print(val)

    def op_jump_true(self, i: Val, o: Val) -> bool:
        if self.load_val(i):
            self.ptr = self.load_val(o)
            return True
        return False

    def op_jump_false(self, i: Val, o: Val) -> bool:
        if not self.load_val(i):
            self.ptr = self.load_val(o)
            return True
        return False

    def op_less_than(self, o1: Val, o2: Val, r: Val) -> None:
        if self.load_val(o1) < self.load_val(o2):
            self.set_value(r, 1)
        else:
            self.set_value(r, 0)

    def op_equals(self, o1: Val, o2: Val, r: Val) -> None:
        if self.load_val(o1) == self.load_val(o2):
            self.set_value(r, 1)
        else:
            self.set_value(r, 0)

    def op_update_rel_base(self, o1: Val) -> None:
        self.rel_base += self.load_val(o1)

    def op_stop(self) -> None:
        self.ended = True

    # END Instruction Definitions

    # BEGIN Instruction Lookup Table

    INSTRUCTIONS = {
        1: {
            'name': 'Add',
            'size': 4,
            'function': op_add
        },
        2: {
            'name': 'Multiply',
            'size': 4,
            'function': op_mul
        },
        3: {
            'name': 'Input',
            'size': 2,
            'function': op_input
        },
        4: {
            'name': 'Output',
            'size': 2,
            'function': op_output
        },
        5: {
            'name': 'Jump If True',
            'size': 3,
            'function': op_jump_true
        },
        6: {
            'name': 'Jump If False',
            'size': 3,
            'function': op_jump_false
        },
        7: {
            'name': 'Less Than',
            'size': 4,
            'function': op_less_than
        },
        8: {
            'name': 'Equals',
            'size': 4,
            'function': op_equals
        },
        9: {
            'name': 'Update Relative Base',
            'size': 2,
            'function': op_update_rel_base
        },
        99: {
            'name': 'Stop',
            'size': 1,
            'function': op_stop,
        }
    }

    # END Instruction Lookup Table

    def decode_instruction(self) -> Tuple[partial, int]:
        """
        Decodes instructions and parameters into a function. Returns a callable partial with all parameters already
        bound.
        """
        # Get the current instruction from the memory location at the instruction pointer
        instruction: int = self.code[self.ptr]
        # The OpCode is the last 2 digits of the instruction
        op_code: int = instruction % 100
        # Lookup the OpCode in the instruction table
        instr: Dict = self.INSTRUCTIONS[op_code]
        # Map the parameter modes. There is probably a more efficient way of doing this but this works so I'll leave it
        modes: List[int] = [
            (instruction // (10 ** (x + 2))) % 10
            for x in range(instr['size'] - 1)
        ]
        # Map the parameters. This zips the parameter modes with the OpCode arguments.
        params: List[Val] = list(zip(modes, self.code[self.ptr + 1:self.ptr + instr['size']]))
        # Return a partial with the parameters bound.
        return partial(instr['function'], self, *params), instr['size']

    def load_val(self, val_spec: Val) -> int:
        """
        Load a value from memory
        """
        mode, loc = val_spec
        if mode == 1:
            return loc
        else:
            addr = self.decode_address(val_spec)
            return self.code[addr]

    def set_value(self, val_spec: Val, value: int) -> None:
        """
        Save a value to memory
        """
        mode, loc = val_spec
        if mode == 1:
            raise Exception("Can't store in immediate mode")
        else:
            addr = self.decode_address(val_spec)
            self.code[addr] = value

    def decode_address(self, val_spec: Val) -> int:
        """
        Decode a non-immediate address. This basically abstracts absoulte and relative addresses.
        """
        mode, offset = val_spec
        if mode == 0:
            addr = offset
        elif mode == 2:
            addr = self.rel_base + offset
        else:
            raise Exception("Can't decode immediate values")
        self.check_bounds(addr)
        return addr

    def check_bounds(self, addr: int) -> None:
        """
        Check if the code is trying to access memory outside of the bounds of the array, increase the size as requried.
        """
        if addr >= len(self.code):
            extra = addr - len(self.code) + 1
            self.code.extend([0] * extra)

    def reset(self) -> None:
        """
        Resets the IntPuter to it's initial state.
        """
        self.code = self.__code[::]
        self.ptr = 0
        self.ended = False
        self.rel_base = 0

    def set_loc(self, loc: int, val: int) -> None:
        """
        Sets the value of a specific memory location.
        """
        self.code[loc] = val

    async def run_async(self):
        """
        Run the IntPuter code asynchronously
        """
        while not self.ended:
            # lookup and call instruction
            try:
                instruction, size = self.decode_instruction()
            except IndexError:
                print("Instruction Pointer:", self.ptr, len(self.code))
            else:
                # Run the instruction
                result = instruction()
                # Some operations are async, but not all. If it is, await the result.
                if inspect.isawaitable(result):
                    result = await result

                # Jumps return True if the jump occurred, False otherwise. Everything else returns None.
                # The below executes on any instruction which didn't jump, updating the instruction pointer.
                if not result:
                    self.ptr += size

        return self.code

    def run(self):
        """
        Sets up and runs synchronously by creating an internal event loop and calling run_async.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.run_async())
