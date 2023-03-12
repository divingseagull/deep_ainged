import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from util import embed

class ExtensionManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.extensions = [
            __file__
        ]

    @nextcord.slash_command("load")
    async def load_ext(self, interaction: Interaction, module: str):
        try:
            self.bot.load_extension(module)
        except commands.errors.ExtensionAlreadyLoaded:
            await interaction.response.send_message(
                embed=embed.Error(description="확장이 이미 로드되어있습니다.")
            )
        except commands.errors.ExtensionNotFound:
            await interaction.response.send_message(
                embed=embed.Error(description="확장을 찾을 수 없습니다.")
            )
        except commands.errors.ExtensionError as err:
            await interaction.response.send_message(
                embed=embed.Error(description=f"오류가 발생했습니다.```{err}```")
            )
        else:
            self.extensions.insert(module)

    @nextcord.slash_command("unload")
    async def unload_ext(self, interaction: Interaction, module: str):
        try:
            if module == __name__:
                raise ValueError()
            self.bot.unload_extension(module)
        except ValueError:
            await interaction.response.send_message(
                embed=embed.Error(description=f"이 확장은 언로드할 수 없습니다.")
            )
        except commands.errors.ExtensionNotLoaded:
            await interaction.response.send_message(
                embed=embed.Error(description="확장이 로드되어있지 않습니다.")
            )
        except commands.errors.ExtensionFailed as err:
            await interaction.response.send_message(
                embed=embed.Error(description=f"오류가 발생했습니다.```{err}```")
            )
        else:
            self.extensions.remove(module)

    @nextcord.slash_command("reload")
    async def reload_ext(self, interaction: Interaction, module: str="ALL"):
        try:
            if module == "ALL":
                for ext in self.extensions:
                    self.bot.reload_extension(ext)
        except commands.errors.ExtensionNotLoaded:
            await interaction.response.send_message(
                embed=embed.Error(description="확장이 로드되어있지 않습니다.")
            )
        except commands.errors.ExtensionError as err:
            await interaction.response.send_message(
                embed=embed.Error(description=f"오류가 발생했습니다. ```{err}```")
            )

def setup(bot: commands.Bot):
    bot.add_cog(ExtensionManager(bot))
