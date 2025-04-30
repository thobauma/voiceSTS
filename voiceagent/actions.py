from smolagents import tool
from typing import Optional


allowed_strings = [
    "rest",
    "smith",
    "lift",
    "dig",
    "toke",
    "purify",
    "heal",
    "leave",
    "accept",
    "refuse",
    "sleep",
    "relic",
    "strike",
    "pain",
    "shop",
    "apotheosis"
]
allowed_potion_actions = ["discard", "use"]

@tool
def action_choose_number(
    number: int
) -> str:
    """A tool that chooses a specified numbered action
    Args:
        number: An integer representing the action to be choosen (e.g. 1)
    """
    return "choose " + str(number)

@tool
def action_play(card: int, target: Optional[int] = None) -> str:
    """A tool that plays a card onto a specified target
    Args:
        card: An integer representing the card to be played (e.g. 1)
        target: An optional integer representing the target (e.g. 2)
    """
    if target is not None:
        return " ".join(["play", str(card), str(target)])
    return "play " + str(card) 

@tool
def action_choose_string(string: str) -> str:
    """A tool that chooses a specific action
    Args:
        string: A string representing an action (e.g. 'dig')
    """
    return "choose " + string

@tool
def action_potion(action: str, potion: int, target: Optional[int] = None
) -> str:
    """A tool that performs a potion action onto a target
    Args:
        action: A string representing the choosen action (e.g. '')
        potion: An integer representing the choosen potion (e.g. 1)
        target: An optional integer representing the target (e.g. 2)
    """
    if target is not None:
        return " ".join(["potion", action, str(potion), str(target)])
    return "potion " + action + " " + str(potion)

@tool
def action_cancel() -> str:
    """A tool that performs the cancel action
    """
    return "cancel"

@tool
def action_proceed() -> str:
    """A tool that performs the proceed action
    """
    return "proceed"

@tool
def action_return() -> str:
    """A tool that performs the return action
    """
    return "return"

@tool
def action_skip() -> str:
    """A tool that performs the skip action
    """
    return "skip"

@tool
def action_confirm() -> str:
    """A tool that performs the confirm action
    """
    return "confirm"

@tool
def action_end() -> str:
    """A tool that performs the end action
    """
    return "end"

action_tools=[action_choose_number,
    #    action_choose_multiple_numbers,
        action_play,
        action_choose_string,
        action_potion,
        action_cancel,
        action_proceed,
        action_return,
        action_skip,
        action_confirm, 
        action_end]
