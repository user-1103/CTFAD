"""
Day by day attaches a chalange to the site in the docs folder from the source
material in the ctfad-cals.
"""
import datetime
from pathlib import Path
import json
import subprocess as sp
from urllib.parse import quote_plus as qp

CATAGORIES = {
        "osint": "OSINT - Using public records to find 'hidden' data.",
        "forensics": "Forensics - Excratcing data and metadata from files.",
        "re": "Reverse Engineering (RE) - Figuring out how a program works.",
        "pwn": ("Exploitation (PWN) - Crafting paylods that make a program "
        "work in unintended ways."),
        "crypto": ("Crypto - Math wizardry that 'locks' information in some"
        "way."),
        "stego": "Stegonography - Non-crypto data obsucation.",
        "misc": "Misc - Fun stuff, trivia, ect..."
        }

CHAL_CARD = """

                    <div class="col-lg-4 col-md-6 portfolio-item filter-%c">
                        <div class="portfolio-wrap">
                            <img src="%l" class="img-fluid" alt="">
                            <div class="portfolio-info">
                                <h4>%d</h4>
                                <p>%n</p>
                                <div class="portfolio-links">
                                    <a href="%j" 
                                       class="portfolio-details-lightbox"
                                        data-glightbox="type: external"
                                        title="%n">
                                        <i class="bx bx-show-alt"></i>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>

"""

def commit_update() -> None:
    now = datetime.datetime.utcnow()
    DAY = now.date().isoformat()
    tmp = ""
    with open(Path('./docs/template.html'), "r") as f_template:
        template = f_template.read()
    with open(Path(f'../ctfad-chals/{DAY}/chal.json'), "r") as f_chal:
        chal = json.load(f_chal)
        ADD_URL = ""
        with open(Path("../add_hook"), "r") as f:
            ADD_URL = f.readlines()
        ADD_URL = ADD_URL[0][:-1]
        template = template.replace("%N", chal["name"])
        ADD_URL = ADD_URL.replace("%n", qp(chal["name"]))
        template = template.replace("%D", DAY)
        ADD_URL = ADD_URL.replace("%d", qp(DAY))
        template = template.replace("%C", CATAGORIES[chal["catagory"]])
        ADD_URL = ADD_URL.replace("%c", qp(chal["catagory"]))
        template = template.replace("%?", f'{chal["difficulty"]}/10')
        ADD_URL = ADD_URL.replace("%?", qp(str(chal["difficulty"])))
        template = template.replace("%R", chal["regex"])
        ADD_URL = ADD_URL.replace("%r", qp(chal["regex"]))
        template = template.replace("%H", chal["hash"])
        ADD_URL = ADD_URL.replace("%h", qp(chal["hash"]))
        template = template.replace("%T", chal["description"])
        ADD_URL = ADD_URL.replace("%t", qp(chal["description"]))
        ADD_URL = ADD_URL.replace("%f", qp(chal["flag"]))
        print(str(len(ADD_URL)))
        sp.run(f"curl '{ADD_URL}'", shell=True, check=True)
        f_out_f = f'CTFAD-{DAY}.zip'
        f_out_f_link = f'{f_out_f}'
        f_out_f_path = Path(f'./docs/days/{f_out_f}')
        f_out_f_path_in = Path(f'../ctfad-chals/{DAY}/{f_out_f}')
        f_out_chal = f'{DAY}.html'
        f_out_chal_link = f'days/{f_out_chal}'
        f_out_chal_path = Path(f'./docs/days/{f_out_chal}')
        f_out_img1 = f'{DAY}-img1.png'
        f_out_img1_link = f'{f_out_img1}'
        f_out_img1_path = Path(f'./docs/days/{f_out_img1}')
        f_out_img1_path_in = Path(f'../ctfad-chals/{DAY}/{f_out_img1}')
        f_out_img2 = f'{DAY}-img2.png'
        f_out_img2_link = f'{f_out_img2}'
        f_out_img2_path = Path(f'./docs/days/{f_out_img2}')
        f_out_img2_path_in = Path(f'../ctfad-chals/{DAY}/{f_out_img2}')
        f_out_img3 = f'{DAY}-img3.png'
        f_out_img3_link = f'{f_out_img3}'
        f_out_img3_path = Path(f'./docs/days/{f_out_img3}')
        f_out_img3_path_in = Path(f'../ctfad-chals/{DAY}/{f_out_img3}')
        template = template.replace("%F", f_out_f)
        template = template.replace("%L", f_out_f_link)
        template = template.replace("%1", f_out_img1_link)
        template = template.replace("%2", f_out_img2_link)
        template = template.replace("%3", f_out_img3_link)
        with open(Path("./docs/base.html"), "r") as f_base:
            f_out = f_base.read()
            f_out = f_out.replace("%t", f_out_chal_link)
            f_out = f_out.replace("%u", now.isoformat(sep=" "))
            global CHAL_CARD
            CHAL_CARD = CHAL_CARD.replace("%l", f'days/{f_out_img1_link}')
            CHAL_CARD = CHAL_CARD.replace("%d", DAY)
            CHAL_CARD = CHAL_CARD.replace("%n", chal["name"])
            CHAL_CARD = CHAL_CARD.replace("%c", chal["catagory"])
            CHAL_CARD = CHAL_CARD.replace("%j", f_out_chal_link)
            f_out = f_out.replace("%a", CHAL_CARD)
            with open(Path("./docs/card_buffer.html"), "r") as f_buffer:
                f_out = f_out.replace("%b", f_buffer.read())
            with open(Path("./docs/card_buffer.html"), "a") as f_buffer:
                f_buffer.write(CHAL_CARD)
            with open(f_out_chal_path, "w+") as f_out_tmp:
                f_out_tmp.write(template)
            with open(Path('./docs/index.html'), "w+") as f_out_tmp:
                f_out_tmp.write(f_out)
        sp.run(["cp", f_out_img1_path_in, f_out_img1_path], check=True)
        sp.run(["cp", f_out_img2_path_in, f_out_img2_path], check=True)
        sp.run(["cp", f_out_img3_path_in, f_out_img3_path], check=True)
        sp.run(["cp", f_out_f_path_in, f_out_f_path], check=True)
        print("Done.")

def push_update() -> None:
        sp.run("git add ./docs/days*", shell=True, check=True)
        sp.run("git add -u", shell=True, check=True)
        sp.run("git commit -m 'Auto Push.'", shell=True, check=True)
        sp.run("git push", shell=True, check=True)


if __name__ == "__main__":
    try:
        commit_update()
        push_update()
        url = ""
        with open(Path("../err_hook"), "r") as f:
            url = f.readlines()
        t = sp.run((f'curl -H "Content-Type: application/json" -d'
            " '{\"username\": \"Build Success!\", \"content\": \"Published.\"}'"
            f' "{url[0][:-1]}"'), shell=True)

    except Exception as e:
        url = ""
        with open(Path("../err_hook"), "r") as f:
            url = f.readlines()
        t = sp.run((f'curl -H "Content-Type: application/json" -d'
            " '{\"username\": \"Build Failed!\", \"content\": \"%.\"}'"
            f' "{url[0][:-1]}"').replace("%", str(e)), shell=True)
