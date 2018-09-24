import os


class Packages:
    def __init__(self):
        self.packages = self._get_packages()

    def __str__(self):
        # Run pip list command
        return str(os.popen('pip list').read())

    def __iter__(self):
        return iter([(name, version) for name, version in self.packages.items()])

    @staticmethod
    def _get_packages():
        # Run pip freeze command
        pip_freeze = os.popen('pip freeze').read()

        # Create dictionary of packages
        return {package.split('==')[0]: package.split('==')[1] for package in pip_freeze.strip().split('\n')}


def main():
    print(Packages())


if __name__ == '__main__':
    main()
