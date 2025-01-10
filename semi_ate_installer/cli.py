import sys
import pyfiglet

from semi_ate_installer.state.state_machine import NewEnvSM
from semi_ate_installer.state.base import State


def print_semi_ate_installer_banner():
    ascii_banner = pyfiglet.figlet_format('SemiATE Installer')
    print(ascii_banner)


def main():
    print_semi_ate_installer_banner()
    if not sys.stdin.isatty():
        return

    state_machine = NewEnvSM()
    while state_machine.is_done() != State.Done:
        state_machine.next()


if __name__ == '__main__':
    main()