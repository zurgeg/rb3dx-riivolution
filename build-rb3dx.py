from os.path import isdir, exists, join, basename
from os import chdir, curdir, mkdir
from click import Choice, prompt, confirm, echo
from alive_progress import alive_bar
from subprocess import Popen, DEVNULL, PIPE
from shutil import copy, move
from glob import glob
from threading import Thread

menu_choices = Choice(["Make ISO", "Make Riivolution"])

def call_bar_at_a_very_fast_rate(bar):
    try:
        while True:
            bar()
    except:
        pass

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
                break
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
                echo("Oh! It looks like you have RB3DX downloaded already!")
                old_dir = curdir
                chdir(join(curdir, "temp", "rock-band-3-delue"))
                Popen(["git", "checkout", "wii"], stdout=DEVNULL, stderr=DEVNULL).wait()
                chdir(old_dir)
                where_is_rb3dx = join(curdir, "temp", "rock-band-3-deluxe")
                do_break = True
                break
            if do_break:
                break



    with alive_bar(title="Making Riivolution Patch", total=0, enrich_print=False) as bar:
        t = Thread(target=call_bar_at_a_very_fast_rate, name="fast", args=[bar], daemon=True)
        t.start()
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
        if where_is_rb3.startswith("\""):
            where_is_rb3 = where_is_rb3[1:-1]
        if exists(where_is_rb3) and not isdir(where_is_rb3):
            bar()
            id6_process = Popen([where_is_wit, "id6", where_is_rb3], stdout=PIPE, stderr=PIPE)
            bar()
            id6_stdout, _ = id6_process.communicate()
            bar()
            id6_process.wait()
            bar()
            if id6_stdout.startswith(b"SZB"):
                bar()
                bar.title(f"Extracting Rock Band 3...")
                bar()
                if not isdir(join(curdir, "temp", "extracted_rb3")):
                    Popen([where_is_wit, "extract", where_is_rb3, join(curdir, "temp", "extracted_rb3")], stdout=PIPE, stderr=PIPE).wait()
                bar()
                arks = glob(join(curdir, "temp", "extracted_rb3", "files", "gen") + "/*.ark")
                for ark in arks:
                    bar()
                    bar.title(f"Copying ARK {ark}")
                    bar()
                    dest = join(where_is_rb3dx, "_build", "wii")
                    bar()
                    if not isdir(join(where_is_rb3dx, "_build", "wii")):
                        raise Exception("This **probably** should never happen. But just in case, you forgot to checkout the wii branch")
                    bar()
                    copy(ark, dest)
                bar.title("Executing build script...")
                Popen(join(where_is_rb3dx, "_build_wii.bat")).wait()
                


            else:
                raise Exception("Oh... You thought you could get around ME? AND MY IDIOT PROTECTION? NOT TODAY!")
        else:
            raise Exception("I am tired of having to write idiot protection... that's not a file")
    while True:
        dest = prompt("Alrighty! Where should I put the finished files?", prompt_suffix=" ")
        if not isdir(dest):
            echo("It needs to be a directory...")
        else:
            echo("Alrighty, give me one minute while I copy the files...")
            arks = glob(join(where_is_rb3dx, "_build", "wii", "*.ark"))
            try:
                mkdir(join(dest, "rb3"))
                mkdir(join(dest, "riivolution"))
            except:
                pass
            for ark in arks:
                echo(f"Copying {ark}...")
                copy(ark, join(dest, "rb3"))
            echo("Copying Riivolution XML")
            copy(join(curdir, "rb3dx-riivo.xml"), join(dest, "riivolution"))
            break
    echo("All done! Thank you!")





        
