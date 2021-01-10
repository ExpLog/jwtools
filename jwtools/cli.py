import sys

import jwt
from rich.columns import Columns
from rich.console import Console
from rich.table import Table
from rich.traceback import install
from typer import Typer, Option

cli = Typer()
install()
console = Console()

STDOUT_TTY = sys.stdout.isatty()
STDIN_TTY = sys.stdin.isatty()


@cli.command()
def print_jwt(encoded_jwt: str,
              use_table: bool = Option(False, '--table', '-t'),
              verbose: int = Option(0, '--verbose', '-v', count=True)):
    if verbose >= 1:
        console.print(f'[bold red]STDOUT[/] [blink yellow]is {"not" if not STDOUT_TTY else ""}[/]a tty')
        console.print(f'[bold red]STDIN[/] [blink yellow]is {"not" if not STDIN_TTY else ""}[/]a tty')

    headers = jwt.get_unverified_header(encoded_jwt)
    claims = jwt.decode(encoded_jwt, options={"verify_signature": False})

    if use_table:
        claims_table = Table(title='Claims', show_header=True, header_style='bold magenta')
        claims_table.add_column('Claim')
        claims_table.add_column('Value')

        for claim, value in claims.items():
            claims_table.add_row(claim, str(value))

        headers_table = Table(title="Header", show_header=True, header_style='bold magenta')
        headers_table.add_column('Header')
        headers_table.add_column('Value')
        for header, value in headers.items():
            headers_table.add_row(header, value)

        columns = Columns([headers_table, claims_table], title='JWT')
        console.print(columns)
    else:
        decoded_jwt = {'headers': headers, 'claims': claims}
        console.print(decoded_jwt)


if __name__ == '__main__':
    cli()
