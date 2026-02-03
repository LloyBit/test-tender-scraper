import typer

from app.commands.delete_file import exterminator_app
from app.commands.parse_to_file import extractor_app
from app.commands.run_api_server import hoster_app
from app.commands.show_data import representer_app

app = typer.Typer()
app.add_typer(extractor_app)
app.add_typer(representer_app)
app.add_typer(exterminator_app)
app.add_typer(hoster_app)


def main() -> None:
    app()


if __name__ == "__main__":
    main()