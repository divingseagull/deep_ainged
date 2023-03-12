from nextcord.ext import commands

import os
import json

cwd = os.getcwd()
with open(f"{cwd}/settings.json", 'r', encoding="UTF-8") as settingsf:
    settings: dict = json.load(settingsf)

token_path: str = settings["token"]["token_path"]
owner_ids: list[int] = settings["owner_ids"]

bot = commands.Bot(owner_ids=owner_ids)

if __name__ == "__main__":
    load_state = {"success": 0, "tried": 0}
    for d in os.listdir("src"):
        if os.path.isdir(d):
            for ext in os.listdir(d):
                if not ext.endswith(".py"):
                    continue
                if ext == "core.py":
                    continue
                if ext in settings["extensions"]["initial_load_exceptions"]:
                    continue
                try:
                    bot.load_extension(f"{d}.{ext}")
                except commands.errors.ExtensionFailed as err:
                    print(err)
                except commands.errors.ExtensionError as err:
                    print(err)
                except Exception as err:
                    print(err)
                else:
                    load_state["success"] += 1
                finally:
                    load_state["tried"] += 1

    failure = load_state["tried"] - load_state["success"]
    success = load_state['success']
    print(f"{success} extensions loaded, {failure} failures.")

    with open(token_path, 'r', encoding="UTF-8") as tokenf:
        bot.run(tokenf.read())