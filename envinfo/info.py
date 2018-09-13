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
import multiprocess as mp
from os import getlogin
from psutil import virtual_memory
from platform import python_version, python_compiler, system, release, machine, processor, architecture, node


class Formatter:
    """Inherited class with methods called by numerous classes."""
    def __init__(self, info_type, info):
        self.type = info_type
        self.info = info

    def __str__(self):
        return self.create_string()

    def create_string(self):
        lst = [self.type, '------------------']
        for k, v in self.info().items():
            lst.append(self.format_string(k, v))
        lst.append('\n')
        return '\n'.join(lst)

    @staticmethod
    def format_string(key, value):
        return f'{key:20} ==> {value}'

    @staticmethod
    def format_size(num_bytes, binary=False, strip=True):
        """
        Format a number of bytes as a human readable size.

        Parameters
        ----------
        num_bytes : int
            The size to format.
        binary : bool, optional
            The base to group the number of bytes.
        strip : bool, optional
            If trailing zeros should be keeped or stripped.

        Returns
        -------
        str
            The human readable file size.
        """
        size_units = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

        if binary:
            base = 2 ** 10
        else:
            base = 10 ** 3

        for i, unit in reversed(list(enumerate(size_units))):
            divider = base ** i
            if num_bytes >= divider:
                formatted = '{:0.2f}'.format(num_bytes / divider, unit)
                if strip:
                    formatted = formatted.rstrip('0').rstrip('.')
                formatted = '{} {}'.format(formatted, unit)

                return formatted

        # Failed to match a unit
        return '0 {}'.format(size_units[0])


class Python(Formatter):
    """Python related information such as Python version and Python compiler"""
    def __init__(self):
        super(Python, self).__init__('Python', self.info)

    def info(self):
        return {'version': self.version, 'compiler': self.compiler}

    @property
    def version(self): return python_version()

    @property
    def compiler(self): return python_compiler()


class System(Formatter):
    """Software related information such as operating system, machine type, username, etc."""
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
    def username(self): return getlogin()


class Memory(Formatter):
    """Memory information class."""
    def __init__(self):
        super(Memory, self).__init__('Memory', self.info)

    def info(self):
        return {'installed': self.installed, 'available': self.available}

    def __str__(self): return self.installed

    @property
    def installed(self): return self.format_size(virtual_memory()[0], binary=True)

    @property
    def available(self): return self.format_size(virtual_memory()[1], binary=True)


class Processor:
    """Processor information class"""
    def __str__(self): return self.type

    @property
    def type(self): return processor()

    @property
    def cores(self): return mp.cpu_count()


class Hardware(Formatter):
    """Hardware related information such as memory and processor information"""
    def __init__(self):
        self.type = 'Hardware'
        super(Hardware, self).__init__('Hardware', self.info)

    def info(self):
        return {'memory_installed': self.memory.installed, 'memory_available': self.memory.available,
                'processor_type': self.processor.type, 'processor_cores': self.processor.cores}

    @property
    def memory(self): return Memory()

    @property
    def processor(self): return Processor()


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
