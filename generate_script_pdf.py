"""
HostelOps - Demo Video Script PDF Generator
Generates a professional, production-ready PDF of the 5-minute demo video script.
"""

from fpdf import FPDF
import os


class ScriptPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 6, "HostelOps - Demo Video Script | AWS Agents for Humans Hackathon", align="L")
            self.cell(0, 6, f"Page {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
            self.line(10, 14, 200, 14)
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, "Confidential - HostelOps Hackathon Project", align="C")

    def section_title(self, title, r=30, g=100, b=200):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(r, g, b)
        self.cell(0, 9, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(r, g, b)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        # Replace problematic unicode characters
        text = text.replace("\u2014", "-").replace("\u2013", "-").replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"').replace("\u2022", "-").replace("\u2713", "V").replace("\u2714", "V").replace("\u2026", "...")
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bullet(self, text, indent=15):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.set_x(10)
        self.cell(indent, 5.5, "-  ")
        self.multi_cell(190 - indent, 5.5, text)

    def table_header(self, cols, widths):
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(30, 100, 200)
        self.set_text_color(255, 255, 255)
        for i, col in enumerate(cols):
            self.cell(widths[i], 7, col, border=1, fill=True, align="C")
        self.ln()

    def table_row(self, cols, widths, fill=False):
        self.set_font("Helvetica", "", 8)
        self.set_text_color(30, 30, 30)
        # Replace problematic unicode characters in all columns
        cols = [c.replace("\u2014", "-").replace("\u2013", "-").replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"').replace("\u2022", "-").replace("\u2713", "V").replace("\u2714", "V").replace("\u2026", "...") for c in cols]
        if fill:
            self.set_fill_color(240, 245, 255)
        else:
            self.set_fill_color(255, 255, 255)
        max_h = 6
        x_start = self.get_x()
        y_start = self.get_y()

        # Calculate row height
        for i, col in enumerate(cols):
            lines = self.multi_cell(widths[i], 5, col, dry_run=True, output="LINES")
            h = len(lines) * 5
            if h > max_h:
                max_h = h

        # Check page break
        if self.get_y() + max_h > 270:
            self.add_page()
            y_start = self.get_y()

        # Draw cells
        for i, col in enumerate(cols):
            x = x_start + sum(widths[:i])
            self.set_xy(x, y_start)
            self.cell(widths[i], max_h, "", border=1, fill=fill)
            self.set_xy(x + 1, y_start + 1)
            self.multi_cell(widths[i] - 2, 5, col)

        self.set_xy(x_start, y_start + max_h)


def sanitize(text):
    """Replace unicode characters that aren't supported by latin-1 encoding."""
    return (
        text.replace("\u2014", "-")
        .replace("\u2013", "-")
        .replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2022", "-")
        .replace("\u2713", "V")
        .replace("\u2714", "V")
        .replace("\u2026", "...")
        .replace("\u279c", "->")
        .replace("\u2192", "->")
    )


def build_pdf():
    pdf = ScriptPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)

    # ============================================================
    # COVER PAGE
    # ============================================================
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(20, 60, 140)
    pdf.cell(0, 15, "HostelOps", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, "AI-Powered Operations Manager for PG and Hostel Owners", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(8)
    pdf.set_draw_color(20, 60, 140)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 12, "5-Minute Product Demo Video Script", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "AWS 'Agents for Humans' Hackathon", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(20)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(60, 60, 60)

    info_lines = [
        ("Project:", "HostelOps"),
        ("Tagline:", "An AI-powered operations manager for PG and hostel owners"),
        ("Duration:", "5 minutes (300 seconds)"),
        ("Format:", "Product demo with screen recording + narration"),
        ("Target:", "AWS Agents for Humans Hackathon Judges"),
        ("Tech Stack:", "React + TypeScript, Python, FastAPI, Strands Agents SDK, Amazon Bedrock, MySQL, AWS"),
    ]

    for label, value in info_lines:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(40, 7, label)
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 7, value, new_x="LMARGIN", new_y="NEXT")

    pdf.ln(15)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 7, "Production-Ready Script with Timestamps, Visual Direction, and Voiceover", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Total Duration: 5:00 | Narration: ~2:30 | Visuals: ~5:00", align="C", new_x="LMARGIN", new_y="NEXT")

    # ============================================================
    # TABLE OF CONTENTS
    # ============================================================
    pdf.add_page()
    pdf.section_title("Table of Contents")
    pdf.ln(3)

    toc_items = [
        "1. Video Overview & Structure",
        "2. Master Script Table (Timestamps)",
        "3. Section-by-Section Breakdown",
        "4. Full Voiceover Script",
        "5. Screen-Recording Checklist",
        "6. Assets Required",
        "7. Editing Checklist",
        "8. YouTube Title & Description",
    ]
    for item in toc_items:
        pdf.set_font("Helvetica", "", 12)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 8, item, new_x="LMARGIN", new_y="NEXT")

    # ============================================================
    # 1. VIDEO OVERVIEW
    # ============================================================
    pdf.add_page()
    pdf.section_title("1. Video Overview & Structure")

    pdf.sub_title("Objective")
    pdf.body_text(
        "Create a 5-minute product demo video for the AWS 'Agents for Humans' Hackathon that clearly "
        "demonstrates HostelOps as a REAL AI AGENT performing actual work -- not just a chatbot. "
        "The video must showcase agentic behavior, real-world actions, human-in-the-loop approval, "
        "AWS/Bedrock integration, and the Strands Agents SDK."
    )

    pdf.sub_title("Target Users")
    pdf.body_text("PG owners, Hostel owners, Small accommodation operators, Property/Hostel managers")

    pdf.sub_title("Video Structure")
    sections = [
        ("00:00 - 00:20", "20s", "Hook", "Show the problem: too many manual tasks"),
        ("00:20 - 00:40", "20s", "Introduce HostelOps", "Present the AI operations manager"),
        ("00:40 - 01:00", "20s", "Why It Is An Agent", "Explain agent architecture"),
        ("01:00 - 01:15", "15s", "Start Real Demo", "Type the actual request"),
        ("01:15 - 01:40", "25s", "Understand + Identify", "Agent parses request, finds tenant/room"),
        ("01:40 - 02:05", "25s", "Create + Classify", "Complaint created and categorized"),
        ("02:05 - 02:35", "30s", "Vendor Discovery", "Search, compare, recommend vendors"),
        ("02:35 - 03:00", "25s", "AI Recommendation", "Show recommendation with reasoning"),
        ("03:00 - 03:25", "25s", "Human Approval", "Owner clicks APPROVE (key moment)"),
        ("03:25 - 03:55", "30s", "Execute Actions", "Job created, vendor assigned, tenant notified"),
        ("03:55 - 04:15", "20s", "Activity Log", "Show audit trail of all actions"),
        ("04:15 - 04:35", "20s", "Architecture", "Technical stack overview"),
        ("04:35 - 04:50", "15s", "What Makes It Different", "Key differentiators montage"),
        ("04:50 - 05:00", "10s", "Closing", "Final impact and branding"),
    ]

    widths = [28, 14, 35, 113]
    headers = ["TIMESTAMP", "DUR", "SECTION", "DESCRIPTION"]
    pdf.table_header(headers, widths)

    for i, (ts, dur, sec, desc) in enumerate(sections):
        pdf.table_row([ts, dur, sec, desc], widths, fill=(i % 2 == 0))

    pdf.ln(5)
    pdf.sub_title("Total Duration Breakdown")
    pdf.body_text("Total Video: 5 minutes 00 seconds (300 seconds)")
    pdf.body_text("Total Narration: ~2 minutes 30 seconds (moderate pace, ~310 words)")
    pdf.body_text("Visual Breathing Room: ~2 minutes 30 seconds (pauses, transitions, screen recording)")

    # ============================================================
    # 2. MASTER SCRIPT TABLE
    # ============================================================
    pdf.add_page()
    pdf.section_title("2. Master Script Table")

    # We'll build this as a series of detailed section cards
    master_sections = [
        {
            "timestamp": "00:00 - 00:05",
            "duration": "5s",
            "visual": "HostelOps dashboard fades in from black. Clean, polished UI with sidebar nav, room grid, and stats.",
            "action": "No action. Let the dashboard breathe.",
            "voiceover": "(Silence -- let visuals speak)",
            "overlay": "HostelOps (subtle, bottom-right corner)",
            "transition": "Soft fade-in from black. Light ambient hum.",
        },
        {
            "timestamp": "00:05 - 00:20",
            "duration": "15s",
            "visual": "Dashboard static. Cursor slowly pans across Rooms, Tenants, Complaints, Vendors sections.",
            "action": "Cursor moves naturally across dashboard sections, pausing briefly on each.",
            "voiceover": "Managing a PG or hostel means dealing with dozens of small operational tasks every day. A tenant reports a problem. A vendor needs to be found. Approval is required. Work needs to be assigned. And the tenant needs an update.",
            "overlay": "Too many manual operational tasks. (appears at 00:12)",
            "transition": "Subtle zoom-in on dashboard. Calm background music fades in softly.",
        },
        {
            "timestamp": "00:20 - 00:30",
            "duration": "10s",
            "visual": "HostelOps logo centered on screen, then dissolve to full dashboard view. Show sidebar with all modules visible.",
            "action": "Presenter highlights sidebar modules: Rooms, Tenants, Complaints, Vendors, Maintenance, Approvals, AI Activity.",
            "voiceover": "HostelOps is an AI-powered operations manager built for PG and hostel owners.",
            "overlay": "HostelOps -- AI Operations Manager",
            "transition": "Smooth dissolve from logo to dashboard.",
        },
        {
            "timestamp": "00:30 - 00:40",
            "duration": "10s",
            "visual": "Dashboard in background. Subtle zoom into the AI chat interaction area.",
            "action": "Cursor hovers over the AI interaction section.",
            "voiceover": "Instead of simply answering questions, it can understand an operational request and coordinate the work required to complete it.",
            "overlay": "(None)",
            "transition": "Gentle zoom into AI section. Music remains soft.",
        },
        {
            "timestamp": "00:40 - 00:52",
            "duration": "12s",
            "visual": "Split view: Left -- AI chat area. Right -- Architecture diagram showing React > FastAPI > Strands Agent > Bedrock > Tools > MySQL. Each layer highlights sequentially.",
            "action": "Cursor traces the architecture path as each layer is mentioned.",
            "voiceover": "HostelOps is powered by the Strands Agents SDK and Amazon Bedrock. The agent can reason about a request, select the tools it needs, interact with operational data, take actions, and involve the owner when human approval is required.",
            "overlay": "Understand > Plan > Use Tools > Act > Verify",
            "transition": "Architecture layers illuminate one by one. Subtle tech sound effect per layer.",
        },
        {
            "timestamp": "00:52 - 01:00",
            "duration": "8s",
            "visual": "Back to full dashboard. Cursor navigates to the AI agent chat interface.",
            "action": "Presenter clicks into the AI agent input field.",
            "voiceover": "Let's see this in action.",
            "overlay": "Real Demo Starts Now (brief flash)",
            "transition": "Clean cut to AI interface. Music dips slightly.",
        },
        {
            "timestamp": "01:00 - 01:15",
            "duration": "15s",
            "visual": "AI chat input field. Presenter types the exact request. Text appears character by character: 'Room 12 ka tap leak ho raha hai. Rahul tenant hai.' Submit button is clicked. Brief pause.",
            "action": "Presenter types the full message, clicks Send/Submit. 2-second pause after submission to let judge see the request.",
            "voiceover": "A tenant reports a leaking tap in Room 12. Let's send this to the agent.",
            "overlay": "Room 12 ka tap leak ho raha hai. Rahul tenant hai. (mirrored on screen as typed)",
            "transition": "Typing SFX (subtle). Pause creates anticipation.",
        },
        {
            "timestamp": "01:15 - 01:25",
            "duration": "10s",
            "visual": "Agent processing indicator (spinner or thinking state). Then results appear: Rahul identified with tenant details. Room 12 identified with room details.",
            "action": "Cursor highlights 'Rahul' and 'Room 12' as they appear in the agent response.",
            "voiceover": "The agent first understands the request and retrieves the relevant tenant and room information.",
            "overlay": "1. Understand request (checkmark)",
            "transition": "Smooth animation as results populate.",
        },
        {
            "timestamp": "01:25 - 01:40",
            "duration": "15s",
            "visual": "Agent response continues. Shows: Rahul -- Tenant ID, Room Number, Contact, Status. Room 12 -- Type, Floor, Status. Agent confirms understanding.",
            "action": "Presenter scrolls through the retrieved data. Highlights key fields.",
            "voiceover": "It identifies Rahul and connects the request to Room 12. The agent now has the context it needs to proceed.",
            "overlay": "2. Identify tenant (checkmark) | 3. Identify room (checkmark)",
            "transition": "Subtle scroll animation. Data cards appear sequentially.",
        },
        {
            "timestamp": "01:40 - 01:52",
            "duration": "12s",
            "visual": "Agent creates a maintenance complaint. Complaint card appears with: Complaint ID, Room 12, Rahul, Category: Plumbing/Maintenance, Priority, Status: Open.",
            "action": "Presenter highlights the complaint card, showing all fields.",
            "voiceover": "It then creates a structured maintenance complaint and classifies the issue so the correct operational workflow can begin.",
            "overlay": "Complaint created (checkmark) | Issue classified (checkmark)",
            "transition": "Complaint card animates into view. Soft confirmation sound.",
        },
        {
            "timestamp": "01:52 - 02:05",
            "duration": "13s",
            "visual": "Agent searches for vendors. Vendor list appears. Show actual vendor names, specialties, ratings, and pricing from the application.",
            "action": "Presenter scrolls through vendor results. Highlights 2-3 vendors.",
            "voiceover": "Next, the agent searches for suitable vendors and compares the available options. This removes one of the repetitive tasks that hostel owners normally have to handle manually.",
            "overlay": "Search vendors (checkmark) | Compare options (checkmark)",
            "transition": "Vendor cards appear in sequence. Subtle data-loading effect.",
        },
        {
            "timestamp": "02:05 - 02:20",
            "duration": "15s",
            "visual": "Vendor comparison view. Show 2-3 vendors side by side: Name, Specialty, Rating, Estimated Cost, Availability. Agent highlights the recommended vendor with a reason.",
            "action": "Presenter points to the recommended vendor. Shows comparison data.",
            "voiceover": "The agent compares pricing, ratings, and availability -- then recommends the best option for this specific job.",
            "overlay": "Recommend best option (checkmark)",
            "transition": "Comparison cards animate in. Recommendation card glows or highlights.",
        },
        {
            "timestamp": "02:20 - 02:35",
            "duration": "15s",
            "visual": "AI Recommendation card prominently displayed. Shows: Recommended Vendor Name, Estimated Cost, Reason, Complaint Reference.",
            "action": "Presenter pauses on the recommendation card.",
            "voiceover": "Based on the available information, the agent recommends an appropriate option. But automation does not mean removing the owner from important decisions.",
            "overlay": "AI Recommendation (top) | Human control remains in the loop. (bottom)",
            "transition": "Recommendation card centered. Brief dramatic pause in narration. Music softens.",
        },
        {
            "timestamp": "02:35 - 02:48",
            "duration": "13s",
            "visual": "Approval screen appears. Clean, prominent modal/card: MAINTENANCE APPROVAL -- Room: 12, Issue: Leaking Tap, Vendor: [actual vendor name], Estimated Cost: [actual amount]. Two buttons: [APPROVE] [REJECT].",
            "action": "Presenter hovers over the APPROVE button. Pause for 2 seconds to let the judge read the approval card.",
            "voiceover": "Before creating the maintenance commitment, HostelOps asks the owner for approval.",
            "overlay": "APPROVAL REQUIRED",
            "transition": "Approval modal fades in. Subtle tension sound or silence for impact.",
        },
        {
            "timestamp": "02:48 - 03:00",
            "duration": "12s",
            "visual": "Presenter clicks the APPROVE button. Button changes to 'Approved' with a checkmark. Agent acknowledges approval and begins execution.",
            "action": "Presenter clicks APPROVE. Visual confirmation appears.",
            "voiceover": "Once approved, the agent continues the workflow automatically.",
            "overlay": "Approved (checkmark) | Agent continuing...",
            "transition": "Click SFX. Satisfying confirmation animation. Music resumes gently.",
        },
        {
            "timestamp": "03:00 - 03:12",
            "duration": "12s",
            "visual": "Agent executes actions. Status cards appear sequentially: Maintenance job created (Job ID shown), Vendor assigned (Vendor name shown), Complaint status updated to 'In Progress'.",
            "action": "Presenter highlights each status update as it appears.",
            "voiceover": "After approval, the agent creates the maintenance job, assigns the vendor, and updates the complaint.",
            "overlay": "Maintenance job created (checkmark) | Vendor assigned (checkmark) | Complaint updated (checkmark)",
            "transition": "Status cards cascade in. Each gets a soft checkmark sound.",
        },
        {
            "timestamp": "03:12 - 03:25",
            "duration": "13s",
            "visual": "Final action: Tenant notification sent. Notification card shows: Sent to Rahul, Room 12, Message content preview, Timestamp. Activity log updates.",
            "action": "Presenter shows the notification card and scrolls to activity log.",
            "voiceover": "And finally, it sends a notification to the tenant -- Rahul -- letting him know help is on the way.",
            "overlay": "Tenant notified (checkmark) | Workflow complete (checkmark)",
            "transition": "Notification card animates. Activity log populates. Gentle completion chime.",
        },
        {
            "timestamp": "03:25 - 03:40",
            "duration": "15s",
            "visual": "Navigate to AI Activity / Activity Log section. Show the full sequence of actions logged: timestamps, actions taken, tools used, outcomes.",
            "action": "Presenter scrolls through the activity log, highlighting key entries.",
            "voiceover": "Every important step is recorded in the activity history, giving the owner full visibility into what the agent did and when.",
            "overlay": "Transparent AI actions | Operational history",
            "transition": "Smooth scroll through log entries. Each entry highlights as mentioned.",
        },
        {
            "timestamp": "03:40 - 03:55",
            "duration": "15s",
            "visual": "Architecture diagram shown cleanly. Layers highlighted sequentially: React Frontend > FastAPI Backend > Strands Agent > Amazon Bedrock > Agent Tools > MySQL",
            "action": "Diagram animates layer by layer.",
            "voiceover": "Under the hood, the React dashboard communicates with a FastAPI backend. The Strands agent orchestrates the workflow, Amazon Bedrock provides the foundation model, and modular tools connect the agent to hostel operations and MySQL data.",
            "overlay": "React > FastAPI > Strands Agent > Bedrock > Tools > MySQL",
            "transition": "Architecture layers illuminate with subtle tech SFX per layer.",
        },
        {
            "timestamp": "03:55 - 04:10",
            "duration": "15s",
            "visual": "Quick montage (2-3s each): AI request typed > Complaint created > Vendors compared > Approval clicked > Maintenance job > Notification sent > Activity log.",
            "action": "Fast cuts between key moments of the demo.",
            "voiceover": "HostelOps is more than a chatbot. It transforms natural-language requests into real operational workflows, uses tools to perform actions, and keeps humans in control when decisions matter.",
            "overlay": "Not just chat. | Real work.",
            "transition": "Quick cuts. Each transition has a subtle whoosh. Music builds slightly.",
        },
        {
            "timestamp": "04:10 - 04:25",
            "duration": "15s",
            "visual": "Return to polished HostelOps dashboard. Show completed maintenance workflow status. Dashboard looks clean, professional, finalized.",
            "action": "Presenter shows the final state of the dashboard with the completed workflow.",
            "voiceover": "Our vision is simple: give small hostel and PG owners an AI operations team that reduces repetitive work and helps them run better operations.",
            "overlay": "(None yet)",
            "transition": "Smooth transition back to dashboard. Music at calm, confident level.",
        },
        {
            "timestamp": "04:25 - 04:35",
            "duration": "10s",
            "visual": "Dashboard fades slightly. Final branding appears: HostelOps logo, tagline, and AWS/Strands/Bedrock logos.",
            "action": "No action. Clean final frame.",
            "voiceover": "(Silence -- let the final frame speak)",
            "overlay": "HostelOps | Smarter operations. Less manual work. | Built with Strands Agents SDK + Amazon Bedrock",
            "transition": "Gentle fade to final branding frame. Music fades out softly.",
        },
        {
            "timestamp": "04:35 - 04:50",
            "duration": "15s",
            "visual": "Final frame holds. QR code or GitHub link if applicable. Hackathon branding.",
            "action": "No action. Hold final frame.",
            "voiceover": "(Silence or very soft ambient)",
            "overlay": "AWS 'Agents for Humans' Hackathon | github.com/[your-repo]",
            "transition": "Hold. Clean fade to black at 04:50.",
        },
        {
            "timestamp": "04:50 - 05:00",
            "duration": "10s",
            "visual": "Fade to black. Optional: HostelOps wordmark one final time.",
            "action": "(None)",
            "voiceover": "(None)",
            "overlay": "(None)",
            "transition": "Fade to black. Silence.",
        },
    ]

    for i, s in enumerate(master_sections):
        # Sanitize all text
        s = {k: sanitize(v) for k, v in s.items()}
        
        if pdf.get_y() > 220:
            pdf.add_page()

        # Section header
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_fill_color(30, 100, 200)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 8, f"  {s['timestamp']}  |  {s['duration']}", fill=True, new_x="LMARGIN", new_y="NEXT")

        pdf.set_text_color(30, 30, 30)

        fields = [
            ("SCREEN/VISUAL:", s["visual"]),
            ("PRESENTER ACTION:", s["action"]),
            ("VOICEOVER:", s["voiceover"]),
            ("TEXT OVERLAY:", s["overlay"]),
            ("TRANSITION/SFX:", s["transition"]),
        ]

        for label, value in fields:
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(0, 5.5, label, new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(30, 30, 30)
            pdf.multi_cell(0, 5.5, value)

        pdf.ln(3)

    # ============================================================
    # 4. FULL VOICEOVER SCRIPT
    # ============================================================
    pdf.add_page()
    pdf.section_title("4. Full Voiceover Script")
    pdf.body_text("Read at moderate pace. Total ~310 words, ~2 minutes 30 seconds.")
    pdf.body_text("Remaining time is visual breathing room, pauses, and transitions.")
    pdf.ln(3)

    voiceover_paragraphs = [
        "Managing a PG or hostel means dealing with dozens of small operational tasks every day. A tenant reports a problem. A vendor needs to be found. Approval is required. Work needs to be assigned. And the tenant needs an update.",
        "HostelOps is an AI-powered operations manager built for PG and hostel owners. Instead of simply answering questions, it can understand an operational request and coordinate the work required to complete it.",
        "HostelOps is powered by the Strands Agents SDK and Amazon Bedrock. The agent can reason about a request, select the tools it needs, interact with operational data, take actions, and involve the owner when human approval is required.",
        "Let's see this in action.",
        "A tenant reports a leaking tap in Room 12.",
        "The agent first understands the request and retrieves the relevant tenant and room information. It identifies Rahul and connects the request to Room 12. The agent now has the context it needs to proceed.",
        "It then creates a structured maintenance complaint and classifies the issue so the correct operational workflow can begin.",
        "Next, the agent searches for suitable vendors and compares the available options. This removes one of the repetitive tasks that hostel owners normally have to handle manually.",
        "The agent compares pricing, ratings, and availability -- then recommends the best option for this specific job.",
        "Based on the available information, the agent recommends an appropriate option. But automation does not mean removing the owner from important decisions.",
        "Before creating the maintenance commitment, HostelOps asks the owner for approval.",
        "Once approved, the agent continues the workflow automatically.",
        "After approval, the agent creates the maintenance job, assigns the vendor, and updates the complaint. And finally, it sends a notification to the tenant -- Rahul -- letting him know help is on the way.",
        "Every important step is recorded in the activity history, giving the owner full visibility into what the agent did and when.",
        "Under the hood, the React dashboard communicates with a FastAPI backend. The Strands agent orchestrates the workflow, Amazon Bedrock provides the foundation model, and modular tools connect the agent to hostel operations and MySQL data.",
        "HostelOps is more than a chatbot. It transforms natural-language requests into real operational workflows, uses tools to perform actions, and keeps humans in control when decisions matter.",
        "Our vision is simple: give small hostel and PG owners an AI operations team that reduces repetitive work and helps them run better operations.",
    ]

    for i, para in enumerate(voiceover_paragraphs):
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(30, 100, 200)
        pdf.cell(0, 6, f"[{i+1}]", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 5.5, f'"{para}"')
        pdf.ln(2)

    # ============================================================
    # 5. SCREEN-RECORDING CHECKLIST
    # ============================================================
    pdf.add_page()
    pdf.section_title("5. Screen-Recording Checklist")

    pdf.sub_title("Pre-Recording Setup")
    pre_items = [
        "HostelOps application fully running and seeded with data",
        "Room 12 exists and is occupied by Rahul (tenant)",
        "At least 2-3 vendors loaded in the vendor database with real names, ratings, pricing",
        "AI agent endpoint functional and responsive",
        "Browser zoom set to 100%, clean bookmarks bar, no notifications",
        "Screen resolution: 1920x1080 (Full HD)",
        "Browser window maximized, no desktop icons visible",
        "Disable all notifications (OS-level and browser-level)",
        "Close all unnecessary tabs and applications",
        "Disable popup blockers for the application",
        "Ensure cursor is visible and smooth (increase size if needed)",
    ]
    for item in pre_items:
        pdf.bullet(f"[ ] {item}")
    pdf.ln(3)

    pdf.sub_title("Recording Sequence")
    rec_items = [
        "01. Dashboard overview -- Full dashboard, static 5 seconds, then slow cursor pan",
        "02. Sidebar modules -- Hover over each: Rooms, Tenants, Complaints, Vendors, Maintenance, Approvals, AI Activity",
        "03. AI chat interface -- Navigate to AI agent input area",
        "04. Type request -- Type exactly: Room 12 ka tap leak ho raha hai. Rahul tenant hai.",
        "05. Submit -- Click Send/Submit, hold for 2 seconds",
        "06. Agent processing -- Capture spinner/thinking state",
        "07. Tenant identified -- Show Rahul's details as returned by agent",
        "08. Room identified -- Show Room 12 details as returned by agent",
        "09. Complaint created -- Show complaint card with ID, room, tenant, category, status",
        "10. Vendor search -- Show vendor list returned by agent (actual names, prices)",
        "11. Vendor comparison -- Show comparison view if available",
        "12. AI recommendation -- Show recommended vendor with reason and cost",
        "13. Approval screen -- Show approval modal/card prominently",
        "14. Click APPROVE -- Capture the click and confirmation",
        "15. Job created -- Show maintenance job with Job ID",
        "16. Vendor assigned -- Show vendor assignment confirmation",
        "17. Complaint updated -- Show updated complaint status",
        "18. Notification sent -- Show tenant notification details",
        "19. Activity log -- Navigate to AI Activity, scroll through full log",
        "20. Final dashboard -- Return to dashboard showing completed workflow",
    ]
    for item in rec_items:
        pdf.bullet(f"[ ] {item}")
    pdf.ln(3)

    pdf.sub_title("Post-Recording")
    post_items = [
        "Review recording for any UI glitches or loading delays",
        "Check cursor is visible throughout",
        "Verify all data shown is real (no placeholder/mock data)",
        "Ensure no personal/sensitive data is exposed",
        "Confirm text is readable at 1080p",
    ]
    for item in post_items:
        pdf.bullet(f"[ ] {item}")

    # ============================================================
    # 6. ASSETS REQUIRED
    # ============================================================
    pdf.add_page()
    pdf.section_title("6. Assets Required")

    pdf.sub_title("Application Assets")
    app_assets = [
        "HostelOps running instance with seed data",
        "Room 12 with tenant Rahul (with real tenant details)",
        "At least 3 vendors with names, specialties, ratings, pricing",
        "Functional AI agent endpoint",
        "Working approval workflow",
        "Working notification system",
        "Activity log populated with agent actions",
    ]
    for item in app_assets:
        pdf.bullet(f"[ ] {item}")
    pdf.ln(3)

    pdf.sub_title("Video Production Assets")
    prod_assets = [
        "Screen recording software (OBS Studio recommended -- free)",
        "Microphone (USB condenser or laptop built-in with quiet environment)",
        "Video editing software (DaVinci Resolve free, CapCut, or Premiere Pro)",
        "Background music (royalty-free tech ambient -- Artlist, Epidemic Sound, or YouTube Audio Library)",
        "Architecture diagram image (created for HostelOps)",
        "HostelOps logo/wordmark (PNG with transparency)",
        "Text overlay templates (consistent font, size, color)",
        "Sound effects: typing, click, confirmation chime, subtle whoosh",
    ]
    for item in prod_assets:
        pdf.bullet(f"[ ] {item}")
    pdf.ln(3)

    pdf.sub_title("Brand Assets")
    brand_assets = [
        "HostelOps logo (dark + light variants)",
        "AWS logo (for hackathon compliance)",
        "Strands Agents SDK logo",
        "Amazon Bedrock logo",
        "Consistent color palette: Primary blue (#1E64C8), Dark (#1E1E2E), Light (#F8FAFC)",
        "Font: Inter or system sans-serif for overlays",
    ]
    for item in brand_assets:
        pdf.bullet(f"[ ] {item}")

    # ============================================================
    # 7. EDITING CHECKLIST
    # ============================================================
    pdf.add_page()
    pdf.section_title("7. Editing Checklist")

    pdf.sub_title("Visual Editing")
    vis_items = [
        "Crop/zoom to highlight important UI elements during key moments",
        "Add smooth zoom transitions (1.2x-1.5x) on approval screen, recommendation card, and activity log",
        "Ensure all text overlays use consistent font, size, and position",
        "Text overlays: bottom-center for descriptions, top-left for section labels",
        "Remove any loading delays or slow API responses (speed up or cut)",
        "Ensure cursor is visible and smooth throughout",
        "Add subtle vignette or border to focus attention on center of screen",
        "Color grade for consistent, clean look (slightly cool tones for tech feel)",
    ]
    for item in vis_items:
        pdf.bullet(f"[ ] {item}")
    pdf.ln(3)

    pdf.sub_title("Audio Editing")
    aud_items = [
        "Record voiceover in quiet environment, consistent volume",
        "Normalize audio levels (-14 LUFS for YouTube)",
        "Background music at -20dB to -25dB relative to voice",
        "Reduce music volume during key explanations and approval moment",
        "Add subtle sound effects: typing (01:00), click (02:48), confirmation chime (03:12)",
        "Ensure no background noise or echo in voiceover",
        "Fade music in at 00:05, fade out at 04:35",
    ]
    for item in aud_items:
        pdf.bullet(f"[ ] {item}")
    pdf.ln(3)

    pdf.sub_title("Pacing & Transitions")
    pace_items = [
        "Hook section (00:00-00:20): Fast enough to grab attention, not rushed",
        "Demo section (01:00-03:55): Allow breathing room for judge to read screen",
        "Approval moment (02:35-03:00): Slightly slower, dramatic pause before click",
        "Architecture (04:15-04:35): Concise, don't linger",
        "Montage (03:55-04:10): Quick cuts, energetic",
        "Closing (04:50-05:00): Calm, confident, clean fade",
        "Use cross-dissolve for major section transitions",
        "Use hard cuts within demo sections for continuity",
    ]
    for item in pace_items:
        pdf.bullet(f"[ ] {item}")
    pdf.ln(3)

    pdf.sub_title("Final Review")
    final_items = [
        "Total duration is exactly 5:00 or under",
        "Voiceover is clear and professional throughout",
        "All screen text is readable at 1080p",
        "No placeholder/mock data visible",
        "Approval click is clearly visible",
        "Architecture diagram is legible",
        "Music doesn't overpower narration",
        "Video starts and ends cleanly",
        "No black frames or dead air (except intentional pauses)",
        "Export: H.264, 1080p, 30fps, YouTube optimized",
    ]
    for item in final_items:
        pdf.bullet(f"[ ] {item}")

    # ============================================================
    # 8. YOUTUBE TITLE & DESCRIPTION
    # ============================================================
    pdf.add_page()
    pdf.section_title("8. YouTube Title & Description")

    pdf.sub_title("YouTube Title (choose one)")
    titles = [
        "HostelOps: AI Operations Manager for PG & Hostel Owners | AWS Agents for Humans Hackathon",
        "HostelOps -- AI Agent That Manages Your Hostel Operations | Hackathon Demo",
        "From Complaint to Resolution: AI Agent Workflow for Hostel Management | HostelOps",
    ]
    for t in titles:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 6, f"  {t}")
        pdf.ln(2)

    pdf.ln(3)
    pdf.sub_title("YouTube Description")
    description = """HostelOps is an AI-powered operations manager for PG and hostel owners, built for the AWS "Agents for Humans" Hackathon.

THE PROBLEM:
PG and hostel owners spend hours every day handling tenant complaints, finding vendors, comparing quotes, getting approvals, and tracking operational work. A simple leaking tap can require 6-8 manual steps.

THE SOLUTION:
HostelOps uses an AI agent to turn natural-language requests into complete operational workflows. Just describe the problem, and the agent handles the rest -- while keeping you in control of important decisions.

KEY FEATURES:
- Natural language request processing
- Automated complaint creation and classification
- Vendor search, comparison, and recommendation
- Human-in-the-loop approval workflow
- Automated job creation and vendor assignment
- Tenant notification system
- Complete activity audit log

TECH STACK:
- Frontend: React + TypeScript + Tailwind CSS
- Backend: Python + FastAPI
- AI Agent: Strands Agents SDK
- LLM: Amazon Bedrock (Claude Sonnet)
- Database: MySQL
- Cloud: AWS

HOW IT WORKS:
1. Owner describes a problem in plain language (English or Hinglish)
2. Agent understands the request and identifies relevant entities
3. Agent creates a maintenance complaint and classifies the issue
4. Agent searches for suitable vendors and compares options
5. Agent recommends the best option with reasoning
6. Owner approves or rejects the recommendation
7. Agent executes: creates job, assigns vendor, notifies tenant
8. All actions are logged for transparency

BUILT FOR:
AWS "Agents for Humans" Hackathon

CONNECT:
GitHub: [your-repo-url]

#AWS #AIAgent #Hackathon #HostelOps #StrandsAgents #AmazonBedrock #PropertyManagement"""

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(0, 5, description)

    # ============================================================
    # SAVE
    # ============================================================
    output_path = os.path.join(os.path.dirname(__file__), "HostelOps_Demo_Video_Script.pdf")
    pdf.output(output_path)
    print(f"PDF generated successfully: {output_path}")
    return output_path


if __name__ == "__main__":
    build_pdf()
