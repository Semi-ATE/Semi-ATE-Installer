import click
import pyfiglet

from semi_ate_installer.state.state_machine import NewEnvSM
from semi_ate_installer.state.base import State


def print_semi_ate_installer_banner():
    ascii_banner = pyfiglet.figlet_format("SemiATE Installer")
    print(ascii_banner)


@click.command()
def run():
    print_semi_ate_installer_banner()

    state_machine = NewEnvSM()
    while state_machine.is_done() != State.Done:
        state_machine.next()


def main():
    run()


if __name__ == "__main__":
    main()
