from core.settings import (
    BASE_HEIGHT,
    BASE_WIDTH,
    GameContext,
    sys,
    MIN_UI_SIZE,
    SIZE_RATIOS,
    Path,
)
from core.enums import PieceColors, ResizeAxis


def clamp(value: float, min_value: float, max_value: float):
    return min(max_value, max(value, min_value))


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

    body = "\n".join(f"│ {line.ljust(width)} │" for line in lines)

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
    scaled_ui_elem = min(max_size, scaled_ui_elem)  # ensures elements stay on screen

    return scaled_ui_elem if get_exact else int(scaled_ui_elem)


def resize(point, axis: ResizeAxis = ResizeAxis.AUTO):
    # get needed info
    x, y = point
    curr_win_w, curr_win_h = GameContext.game.display.get_size()

    # get scale
    scale_x = curr_win_w / BASE_WIDTH
    scale_y = curr_win_h / BASE_HEIGHT
    match axis:
        case ResizeAxis.WIDTH:
            scale_y = scale_x
        case ResizeAxis.HEIGHT:
            scale_x = scale_y
        case ResizeAxis.MIN:
            scale_x = scale_y = min(scale_x, scale_y)
        case ResizeAxis.MAX:
            scale_x = scale_y = max(scale_x, scale_y)
        case ResizeAxis.AUTO:
            pass
        case _:
            raise ValueError(f'axis argument "{axis}" is invalid')

    # compute resized point and return
    x_resized = clamp(x * scale_x, MIN_UI_SIZE, curr_win_w)
    y_resized = clamp(y * scale_y, MIN_UI_SIZE, curr_win_h)

    return (x_resized, y_resized)


def scale(scalar, get_exact=False, axis: ResizeAxis = ResizeAxis.AUTO):
    window_width, window_height = GameContext.game.display.get_size()

    match axis:
        case ResizeAxis.MIN:
            scale = min(window_width / BASE_WIDTH, window_height / BASE_HEIGHT)
        case ResizeAxis.MAX:
            scale = max(window_width / BASE_WIDTH, window_height / BASE_HEIGHT)
        case ResizeAxis.WIDTH:
            scale = window_width / BASE_WIDTH
        case ResizeAxis.HEIGHT:
            scale = window_height / BASE_HEIGHT
        case ResizeAxis.AUTO:
            scale = window_height / BASE_HEIGHT
        case _:
            raise ValueError(f'axis argument "{axis}" is invalid')

    scaled_num = scale * scalar
    # prevent elements from going off screen
    scaled_num = min(window_width, window_height, scaled_num)
    scaled_num = max(MIN_UI_SIZE, scaled_num)

    return scaled_num if get_exact else int(scaled_num)


def get_all_pieces_of_color(color, board):
    pieces = []
    for row in board.board:
        for square in row:
            if square.empty():
                continue
            if square.piece.color == color:
                pieces.append(square.piece)

    return pieces


def opposite_color(color):
    return PieceColors.BLACK if color == PieceColors.WHITE else PieceColors.WHITE
