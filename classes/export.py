from fpdf import FPDF


class StoryPDF(FPDF):
    HEADER_IMAGE = 'assets/images/BookSmartLogo.jpeg'

    def __init__(self, story_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_text = "BookSmartAI" + " - " + story_name

    def header(self):
        # Logo
        self.image(self.HEADER_IMAGE, 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, self.header_text, 0, 0, 'C')
        # Line break
        self.ln(50)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
