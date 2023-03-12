from nextcord import Embed, Interaction

class Error:
    def __init__(self, title: str="오류", description: str="오류가 발생했습니다", color: hex=0xFF0000):
        self.embed = Embed(
            title=title,
            description=description,
            color=color
        )
