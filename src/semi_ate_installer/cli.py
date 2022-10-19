import click
import pyfiglet

from semi_ate_installer.state.state_machine import NewEnvSM
from semi_ate_installer.state.base import State


def print_semi_ate_installer_banner():
    ascii_banner = pyfiglet.figlet_format("SemiATE Installer")
    print(ascii_banner)


# feedstock build will try to execute the semi-ate-installer to verify a working executable
# but as the installer doesn't behave as a CLI it starts and waits for user input
# which will block for ever and the build terminates with an error
# this shall extend the installer to behave as a CLI
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
