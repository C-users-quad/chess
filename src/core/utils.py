from core.settings import *

def get_tui_text_box(text: object):
    """
    Bundles up lines of text in a neat box. Mainly used for printing and debugging.
    Args:
        lines (```list[str]```) : the list of strings to be bundled up.
            for example, it should look something like this for a button class'
            __str__ method:
            ```
            text = (
                f"Button {hex(id(self))}\n"
                f"Size: {self.rect.size}\n"
                f"Topleft: {self.rect.topleft}\n"
                f"Center: {self.rect.center}\n"
                f"Bottomright: {self.rect.bottomright}\n"
            )
            return get_tui_text_box(lines)
            ```
    Returns:
        str : the completed and bundled-up string, ready for printing.
    """
    lines = str(text).split("\n")
    width = max(len(line) for line in lines)
    top = "┌" + "─" * (width + 2) + "┐"
    bottom = "└" + "─" * (width + 2) + "┘"

    body = "\n".join(
        f"│ {line.ljust(width)} │" for line in lines
    )

    return f"{top}\n{body}\n{bottom}"

def asset_path(relative):
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent.parent.parent  # go up one directory
    return base / relative

def get_ui_elem(element):
    """used to get ui elements that are scaled to the window size"""
    window_width, window_height = GameContext.game.display.get_size()
    return int(window_height * SIZE_RATIOS[element])
