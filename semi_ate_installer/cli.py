from environment.handler import EnvironmentHandler
import questionary
import pyfiglet
from channel.repository import Repository

from semi_ate_installer.state.state_machine import NewEnvSM
from semi_ate_installer.state.base import State


def print_semi_ate_installer_banner():
    ascii_banner = pyfiglet.figlet_format('SemiATE Installer')
    print(ascii_banner)


def main():
    # available_packages = Repository().get_available_versions('^(semi-ate-apps-common|semi-ate-common)$')
    # for a in available_packages:
    #     print(a)
    print_semi_ate_installer_banner()
    # env = select_environment()
    # print(env.name)
    # # env.install_packages(['semi-ate-common=1.0.10', 'semi-ate-apps-common=1.0.10'])
    # env.get_installed_packages()

    # for p in env.semi_ate_packages:
    #     print(p)

    # for p in env.required_packages:
    #     print(p)


    state_machine = NewEnvSM()
    while state_machine.is_done() != State.Done:
        state_machine.next()


if __name__ == '__main__':
    main()