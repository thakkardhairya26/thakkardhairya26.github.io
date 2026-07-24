from pathlib import Path
import argparse
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
DPI_SCALE = 300 / 72


# ============================
# Helpers
# ============================

def clean_directory(path: Path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def convert_pdf_to_images(pdf_path: Path, output_dir: Path):
    """
    Convert PDF pages into lossless WebP images.
    """

    print(f"Converting {pdf_path.name}...")

    pdf = pymupdf.open(pdf_path)
    output_page_number = 1

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

        page_images = [img]
        if pix.width > pix.height * 1.2:
            midpoint = img.width // 2
            page_images = [
                img.crop((0, 0, midpoint, img.height)),
                img.crop((midpoint, 0, img.width, img.height))
            ]

        for page_image in page_images:
            image_path = output_dir / f"{output_page_number:03}.webp"
            page_image.save(
                image_path,
                "WEBP",
                lossless=True,
                method=6
            )
            output_page_number += 1

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
    position:fixed;
    top:10px;
    left:50%;
    transform:translateX(-50%);
    z-index:20;
    color:white;
    padding:4px;
    border-radius:8px;
    background:rgba(17,17,17,.9);
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


#pdf-viewer {{
    display:none;
    position:fixed;
    inset:0;
    width:100vw;
    height:100vh;
    border:0;
    background:white;
    z-index:10;
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


<button onclick="showFlipbook()">
Flipbook
</button>

<button onclick="showPdfViewer()">
PDF viewer
</button>

<a href="../assets/Dhairya_Thakkar_Portfolio.pdf"
target="_blank"
download>

<button>
Download PDF
</button>

</a>

</div>



<div id="flipbook"></div>


<iframe
id="pdf-viewer"
src="../assets/Dhairya_Thakkar_Portfolio.pdf"
title="Dhairya Thakkar portfolio PDF">
</iframe>



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

function showFlipbook() {{
     document.getElementById("flipbook").style.display = "block";
     document.getElementById("pdf-viewer").style.display = "none";
}}


function showPdfViewer() {{
     document.getElementById("flipbook").style.display = "none";
     document.getElementById("pdf-viewer").style.display = "block";
}}




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

    parser = argparse.ArgumentParser(
        description="Generate the portfolio site."
    )
    parser.add_argument(
        "--update-webp",
        action="store_true",
        help="Regenerate the portfolio page images from the source PDF."
    )
    args = parser.parse_args()

    if not CV_FILE.exists():
        raise FileNotFoundError(
            f"Missing {CV_FILE}"
        )

    if not PORTFOLIO_FILE.exists():
        raise FileNotFoundError(
            f"Missing {PORTFOLIO_FILE}"
        )


    OUTPUT.mkdir(exist_ok=True)

    if args.update_webp:
        clean_directory(PAGES)
        convert_pdf_to_images(
            PORTFOLIO_FILE,
            PAGES
        )
    elif not any(PAGES.glob("*.webp")):
        raise FileNotFoundError(
            "No portfolio WebP pages found. Run with --update-webp first."
        )


    generate_portfolio_html()

    generate_landing_page()


    print("\nDone!")
    print(
        "Open index.html in your browser."
    )


if __name__ == "__main__":
    main()