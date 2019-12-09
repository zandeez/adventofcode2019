#!/usr/bin/env python3
from functools import partial
from typing import Tuple, List, Dict
import asyncio
import inspect

Val = Tuple[int, int]


class Pipe:
    semaphore: asyncio.Semaphore = None
    data: List[int] = None

    def __init__(self):
        self.data = []
        self.semaphore = asyncio.Semaphore(0)

    async def dequeue(self) -> int:
        await self.semaphore.acquire()
        return self.data.pop(0)

    def peek(self):
        return self.data[0]

    def enqueue(self, val: int):
        self.data.append(val)
        self.semaphore.release()

    def clear(self):
        self.data.clear()
        self.semaphore = asyncio.Semaphore(0)


class IntPuter:
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

    # Instruction Definitions
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

    def op_output(self, i: Val) -> None:
        val = self.load_val(i)
        if self.output_pipe is not None:
            self.output_pipe.enqueue(val)
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

    # Instruction Lookup Table
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

    def decode_instruction(self, instruction: int) -> Tuple[partial, int]:
        op_code: int = instruction % 100
        instr: Dict = self.INSTRUCTIONS[op_code]
        modes: List[int] = [
            (instruction // (10 ** (x + 2))) % 10
            for x in range(instr['size'] - 1)
        ]
        params: List[Val] = list(zip(modes, self.code[self.ptr + 1:self.ptr + instr['size']]))
        return partial(instr['function'], self, *params), instr['size']

    def load_val(self, val_spec: Val) -> int:
        mode, loc = val_spec
        if mode == 1:
            return loc
        else:
            addr = self.decode_address(val_spec)
            return self.code[addr]

    def set_value(self, val_spec: Val, value: int) -> None:
        mode, loc = val_spec
        if mode == 1:
            raise Exception("Can't store in immediate mode")
        else:
            addr = self.decode_address(val_spec)
            self.code[addr] = value

    def decode_address(self, val_spec: Val) -> int:
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
        if addr >= len(self.code):
            extra = addr - len(self.code) + 1
            self.code.extend([0] * extra)

    def reset(self) -> None:
        self.code = self.__code[::]
        self.ptr = 0
        self.ended = False
        self.rel_base = 0

    def set_loc(self, loc: int, val: int) -> None:
        self.code[loc] = val

    @asyncio.coroutine
    async def run_async(self):
        while not self.ended:
            # lookup and call instruction
            try:
                instruction, size = self.decode_instruction(self.code[self.ptr])
            except IndexError:
                print("Instruction Pointer:", self.ptr, len(self.code))
            else:
                result = instruction()
                # Some operations are async, but not all
                if inspect.isawaitable(result):
                    result = await result

                # If result is True, a jump occurred so don't update the function pointer
                if not result:
                    self.ptr += size

        return self.code

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.run_async())
