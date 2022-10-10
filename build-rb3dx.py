from os.path import isdir, exists, join
from os import access
from click import Choice, prompt, echo
from alive_progress import alive_bar
from subprocess import Popen, DEVNULL

menu_choices = Choice(["Make ISO", "Make Riivolution"])


print("---Welcome to zurgeg's RB3DX build tools!---")
what_to_do = prompt("What do you want to do?", prompt_suffix=": ", show_choices=True, type=menu_choices)

if what_to_do == "Make ISO":
    raise NotImplementedError("Make ISO not implemented")
else:
    where_is_wit = prompt("WIT Location")
    where_is_rb3 = prompt("RB3 Location")
    with alive_bar(title="Making Riivolution Patch", total=0, enrich_print=False) as bar:
        bar.title(f"Checking if WIT (at {where_is_wit}) works...")
        # 21 lines of janky idiot protection.
        while True:
            bar()
            try:
                Popen([where_is_wit, "version"], stdout=DEVNULL, stderr=DEVNULL).wait()
                bar()
                break
            except FileNotFoundError:
                # Is it quoted?
                if where_is_wit.startswith("\""):
                    where_is_wit = where_is_wit[1:-1]
                else:
                    raise Exception("...That file isn't there, idiot")
            except OSError:
                # Is it a directory?
                if isdir(where_is_wit):
                    if exists(join(where_is_wit, "wit")):
                        where_is_wit = join(where_is_wit, "wit")
                    elif exists(join(where_is_wit, "wit.exe")):
                        where_is_wit = join(where_is_wit, "wit.exe")
                else:
                    raise Exception("An unknown OS error occured.\nSOMEHOW, you were stupid enough to get around my dummy protection.")
        bar.title(f"Checking if game (at {where_is_rb3}) is a valid RB3 Wii game...")
        
        
