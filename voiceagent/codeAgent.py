from typing import List, Callable, TypedDict
from smolagents import CodeAgent, Model


class codeAgent:
    def __init__(self,
                 tools: List[Callable],
                 model: Model,
                 prompt_template
                 ):
        self.model = model
        self.tools = {tool.name: tool for tool in tools}
        self.prompt_template = prompt_template
        
