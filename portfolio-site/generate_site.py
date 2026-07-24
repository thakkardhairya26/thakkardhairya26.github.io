from pathlib import Path
import pymupdf  # PyMuPDF
from PIL import Image
import shutil
import html


# ============================
# Configuration
# ============================

SITE_NAME = "Dhairya Thakkar"

ROOT = Path(__file__).parent

ASSETS = ROOT / "assets"

CV_FILE = ASSETS / "Dhairya_Thakkar_CV.pdf"
PORTFOLIO_FILE = ASSETS / "Dhairya_Thakkar_Portfolio.pdf"

OUTPUT = ROOT / "portfolio"
PAGES = OUTPUT / "pages"

LANDING_PAGE = ROOT / "index.html"


# Render quality
DPI_SCALE = 2.2


# ============================
# Helpers
# ============================

def clean_directory(path: Path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def convert_pdf_to_images(pdf_path: Path, output_dir: Path):
    """
    Convert PDF pages into optimized WebP images.
    """

    print(f"Converting {pdf_path.name}...")

    pdf = pymupdf.open(pdf_path)

    for i, page in enumerate(pdf):

        pix = page.get_pixmap(
            matrix=pymupdf.Matrix(
                DPI_SCALE,
                DPI_SCALE
            ),
            alpha=False
        )

        image_path = output_dir / f"{i+1:03}.webp"

        img = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        img.save(
            image_path,
            "WEBP",
            quality=85,
            method=6
        )

        print(
            f"  page {i+1}/{len(pdf)}"
        )


def generate_page_list():
    """
    Generate JS array containing page images.
    """

    pages = sorted(PAGES.glob("*.webp"))

    return ",\n".join(
        f'"pages/{p.name}"'
        for p in pages
    )


# ============================
# Generate flipbook page
# ============================

def generate_portfolio_html():

    images = generate_page_list()

    html_content = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>{SITE_NAME} Portfolio</title>


<style>

body {{
    margin:0;
    background:#111;
    height:100vh;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    font-family:Arial, sans-serif;
}}


#toolbar {{
    color:white;
    margin-bottom:20px;
}}


button {{
    padding:10px 18px;
    border-radius:8px;
    border:none;
    cursor:pointer;
    margin:5px;
}}


#flipbook {{
    background:white;
}}


</style>


<script src="https://unpkg.com/page-flip/dist/js/page-flip.browser.js">
</script>


</head>


<body>


<div id="toolbar">

<button onclick="location.href='../index.html'">
← Back
</button>


<a href="../assets/Portfolio_Dhairya_Thakkar.pdf"
target="_blank">

<button>
Download PDF
</button>

</a>

</div>



<div id="flipbook"></div>



<script>


const images = [

{images}

];


const pageFlip = new St.PageFlip(

document.getElementById("flipbook"),

{{

width:600,
height:850,

size:"stretch",

minWidth:315,
maxWidth:1000,

minHeight:420,
maxHeight:1350,


showCover:true,

mobileScrollSupport:false

}}

);



pageFlip.loadFromImages(images);



document.addEventListener(
"keydown",
(e)=>{{

if(e.key==="ArrowRight")
    pageFlip.flipNext();


if(e.key==="ArrowLeft")
    pageFlip.flipPrev();

}}
);


</script>


</body>

</html>
"""

    OUTPUT.mkdir(exist_ok=True)

    (OUTPUT / "index.html").write_text(
        html_content,
        encoding="utf-8"
    )


# ============================
# Generate landing page
# ============================

def generate_landing_page():

    content = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">


<title>{SITE_NAME}</title>


<style>

body {{

font-family:
-apple-system,
BlinkMacSystemFont,
"Segoe UI",
Arial;

background:#fafafa;

display:flex;

justify-content:center;

align-items:center;

height:100vh;

margin:0;

}}



.container {{

text-align:center;

}}



h1 {{

font-size:48px;

margin-bottom:10px;

}}



.subtitle {{

color:#555;

font-size:20px;

margin-bottom:40px;

}}



.card {{

display:inline-block;

padding:30px;

margin:15px;

background:white;

border-radius:18px;

box-shadow:
0 10px 30px rgba(0,0,0,.08);

width:240px;

}}



a {{

text-decoration:none;

color:#111;

}}



button {{

padding:12px 25px;

border:none;

border-radius:8px;

background:#111;

color:white;

cursor:pointer;

font-size:16px;

}}

</style>


</head>


<body>


<div class="container">


<h1>
{SITE_NAME}
</h1>


<div class="subtitle">
Portfolio & Curriculum Vitae
</div>



<div class="card">

<h2>
CV
</h2>

<p>
View my professional experience
</p>

<a href="assets/Dhairya_Thakkar_CV.pdf"
target="_blank">

<button>
Open CV
</button>

</a>

</div>




<div class="card">

<h2>
Portfolio
</h2>

<p>
Interactive project portfolio
</p>


<a href="portfolio/index.html">

<button>
Open Portfolio
</button>

</a>


</div>



</div>


</body>

</html>
"""

    LANDING_PAGE.write_text(
        content,
        encoding="utf-8"
    )


# ============================
# Main
# ============================

def main():

    if not CV_FILE.exists():
        raise FileNotFoundError(
            f"Missing {CV_FILE}"
        )

    if not PORTFOLIO_FILE.exists():
        raise FileNotFoundError(
            f"Missing {PORTFOLIO_FILE}"
        )


    clean_directory(OUTPUT)

    PAGES.mkdir()


    convert_pdf_to_images(
        PORTFOLIO_FILE,
        PAGES
    )


    generate_portfolio_html()

    generate_landing_page()


    print("\nDone!")
    print(
        "Open index.html in your browser."
    )


if __name__ == "__main__":
    main()