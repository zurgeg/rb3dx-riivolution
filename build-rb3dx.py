from os.path import isdir, exists, join
from os import chdir, curdir
from click import Choice, prompt, confirm, echo
from alive_progress import alive_bar
from subprocess import Popen, DEVNULL, PIPE
from shutil import move

menu_choices = Choice(["Make ISO", "Make Riivolution"])


print("---Welcome to zurgeg's RB3DX build tools!---")
what_to_do = prompt("What do you want to do?", prompt_suffix=": ", show_choices=True, type=menu_choices)

if what_to_do == "Make ISO":
    raise NotImplementedError("Make ISO not implemented")
else:
    where_is_wit = prompt("WIT Location")
    where_is_rb3 = prompt("RB3 Location")
    while True:
        if not isdir(join(curdir, "temp", "rock-band-3-deluxe")):
            has_rb3dx = confirm("Do you have RB3DX downloaded?")
            if has_rb3dx:
                where_is_rb3dx = prompt("RB3DX Location")
            else:
                where_is_rb3dx = join(curdir, "temp", "rock-band-3-deluxe")
                echo("Okay. I'll download RB3DX now...")
                keep_rb3dx = confirm("By the way... should I keep RB3DX afterwards? If you run this utility afterwards, I'll update and use the previously downloaded RB3DX.")
                echo("Alright. I'll check for Git now...")
                try:
                    Popen(["git"], stdout=DEVNULL, stderr=DEVNULL).wait()
                except:
                    echo("Sorry! I couldn't find Git! Please install it and try again.")
                    exit(1)
                echo("Okay. We are ready to clone the repository. Please wait...")
                statuscode = Popen(["git", "clone", "https://github.com/hmxmilohax/rock-band-3-deluxe", "./temp/rock-band-3-deluxe"], stdout=DEVNULL, stderr=DEVNULL).wait()
                if statuscode:
                    echo("Uh oh! We had a problem running Git. Try again later.")
                    echo(f"(In case you wanted to know, the status code was {statuscode})")
                    exit()
                else:
                    echo("Alright! I've downloaded RB3DX!")
        else:
            while True:
                echo("Oh! It looks like you have RB3DX downloaded already! Awesome! I'll update that real quick...")
                old_dir = curdir
                chdir(join(curdir, "temp", "rock-band-3-delue"))
                statuscode = Popen(["git", "pull"], stdout=DEVNULL, stderr=DEVNULL).wait()
                if statuscode:
                    use_other_rb3dx = prompt("Sorry! I couldn't update RB3DX! Do you want to use a different copy of RB3DX?")
                    if use_other_rb3dx:
                        # We'll move the cloned RB3DX temporarily
                        chdir(old_dir)
                        # We'll move this back during cleanup.
                        move(join(curdir, "temp", "rock-band-3-delue"), join(curdir, "temp", "rb3dx-update-fail"))
                        do_break = False
                        break
                else:
                    where_is_rb3dx = join(curdir, "temp", "rock-band-3-deluxe")
                    do_break = True
                    break
            if do_break:
                break



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
        bar()
        # We won't even try with the idiot protection here.
        if exists(where_is_rb3) and not isdir(where_is_rb3):
            bar()
            id6_process = Popen([where_is_wit, "id6", where_is_rb3], stdout=PIPE, stderr=PIPE)
            bar()
            id6_stdout, _ = id6_process.communicate()
            bar()
            id6_process.wait()
            bar()
            if id6_stdout.startswith("SZE"):
                bar()
                bar.title(f"Extracting Rock Band 3...")
                bar()
                Popen([where_is_wit, "extract", where_is_rb3, join(curdir, "temp", "extracted_rb3")]).wait()
                bar()
                

            

        
