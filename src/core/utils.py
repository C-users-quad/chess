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
                f"Button {hex(id(self))}\\n"
                f"Size: {self.rect.size}\\n"
                f"Topleft: {self.rect.topleft}\\n"
                f"Center: {self.rect.center}\\n"
                f"Bottomright: {self.rect.bottomright}"
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
        base = Path(__file__).resolve().parent.parent.parent
    return base / relative

def get_ui_elem(element, get_exact=False):
    """used to get base size ui elements"""
    ratio = SIZE_RATIOS[element]
    max_size = min(BASE_WIDTH, BASE_HEIGHT)
    scaled_ui_elem = ratio * max_size
    scaled_ui_elem = min(max_size, scaled_ui_elem) # ensures elements stay on screen
    return scaled_ui_elem if get_exact else int(scaled_ui_elem)

def resize(pos):
    x, y = pos
    curr_win_w, curr_win_h = GameContext.game.display.get_size()
    scale_x = curr_win_w / BASE_WIDTH
    scale_y = curr_win_h / BASE_HEIGHT
    return (x * scale_x, y * scale_y)

def scale(scalar, get_exact=False,
          axis: Literal['width', 'height', 'min', 'max']='min'):
    window_width, window_height = GameContext.game.display.get_size()

    if axis == 'min':
        scale = min(
            window_width / BASE_WIDTH,
            window_height / BASE_HEIGHT
        )
    elif axis == 'max':
        scale = max(
            window_width / BASE_WIDTH,
            window_height / BASE_HEIGHT
        )
    elif axis == 'width':
        scale = window_width / BASE_WIDTH
    elif axis == 'height':
        scale = window_height / BASE_HEIGHT
    else:
        raise ValueError(f"axis argument \"{axis}\" is invalid")

    return scale * scalar if get_exact else int(scale * scalar)
