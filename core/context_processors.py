from pathlib import Path

STATIC_DIR = Path(__file__).resolve().parent / "static"


def asset_version(request):
    """Version string for CSS/JS links so browsers reload them after edits."""
    mtimes = [
        int(p.stat().st_mtime)
        for p in (STATIC_DIR / "css", STATIC_DIR / "js")
        for p in p.glob("*")
        if p.is_file()
    ]
    return {"asset_version": max(mtimes, default=0)}
