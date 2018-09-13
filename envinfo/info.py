"""
A lightweight utility for retrieving system information and specifications.

System Information
------------------
Hardware
    Processor
Python
    Version
    Compiler
System
    OS
    Release
    Machine
    Architecture
    Hostname
    Username
"""
import os
import multiprocess as mp
from psutil import virtual_memory
from platform import python_version, python_compiler, system, release, machine, processor, architecture, node
from envinfo.format import format_size, format_string


class Formatter:
    def __init__(self, info_type, info):
        self.type = info_type
        self.info = info

    def __str__(self):
        return self.create_string()

    def create_string(self):
        lst = [self.type, '------------------']
        for k, v in self.info().items():
            lst.append(format_string(k, v))
        lst.append('\n')
        return '\n'.join(lst)


class Python(Formatter):
    def __init__(self):
        super(Python, self).__init__('Python', self.info)

    def info(self):
        return {'version': self.version, 'compiler': self.compiler}

    @property
    def version(self): return python_version()

    @property
    def compiler(self): return python_compiler()


class System(Formatter):
    def __init__(self):
        super(System, self).__init__('System', self.info)

    def info(self):
        return {'os': self.os, 'release': self.release, 'machine': self.machine, 'architecture': self.architecture,
                'hostname': self.hostname, 'username': self.username}

    @property
    def os(self): return system()

    @property
    def release(self): return release()

    @property
    def machine(self): return machine()

    @property
    def architecture(self): return architecture()[0]

    @property
    def hostname(self): return node()

    @property
    def username(self): return os.getlogin()


class Hardware(Formatter):
    def __init__(self):
        self.type = 'Hardware'
        super(Hardware, self).__init__('Hardware', self.info)

    def info(self):
        return {'memory_installed': self.memory.installed, 'memory_available': self.memory.available,
                'processor_type': self.processor.type, 'processor_cores': self.processor.cores}

    @property
    def memory(self):
        class Memory:
            def __init__(self):
                self.installed = format_size(virtual_memory()[0], binary=True)
                self.available = format_size(virtual_memory()[1], binary=True)
        return Memory()

    @property
    def processor(self):
        class Processor:
            def __init__(self):
                self.type = processor()
                self.cores = mp.cpu_count()
        return Processor()


class EnvInfo:
    def __init__(self):
        self.python = Python()
        self.system = System()
        self.hardware = Hardware()

    def __iter__(self):
        return iter([self.python, self.system, self.hardware])

    def __str__(self):
        return ''.join([str(i) for i in self.__iter__()])

    def info(self):
        return {n.type.lower(): n.info() for n in self.__iter__()}


def main():
    env = EnvInfo()
    print(env)
    return env.info()


if __name__ == '__main__':
    main()
