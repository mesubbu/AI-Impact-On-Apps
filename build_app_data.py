#!/usr/bin/env python3
"""
Merge CScore JSON files into a single flat data.json for the apps-visualizer.
Adds Play Store categories and Play Store URLs to each app entry.
"""
import json, re, urllib.parse

# ── Play Store category mappings ──────────────────────────────────────────────
# Manually curated from the 318 scored apps.
CATEGORY_MAP = {
    # ── Social & Communication ────────────────────────────────────────────
    "Facebook": "Social",
    "Instagram": "Social",
    "Snapchat": "Social",
    "TikTok": "Social",
    "Threads": "Social",
    "Reddit": "Social",
    "Discord": "Social",
    "Discord - Talk, Play, Hang Out": "Social",
    "GroupMe": "Social",
    "LINE: Calls & Messages": "Communication",
    "WhatsApp Messenger": "Communication",
    "WhatsApp Business": "Communication",
    "Telegram": "Communication",
    "Signal Private Messenger": "Communication",
    "Messenger": "Communication",
    "Messenger Kids – The Messaging": "Communication",
    "Messenger : Text Messages": "Communication",
    "Messenger SMS - Text Messages": "Communication",
    "Messages": "Communication",
    "Messages - SMS Texting App": "Communication",
    "Messages for Android": "Communication",
    "Messages: SMS Messaging App": "Communication",
    "SMS Messages App": "Communication",
    "SMS Messenger": "Communication",
    "Zangi Private Messenger": "Communication",
    "Telega － мессенджер и звонки": "Communication",
    "TextNow: Call + Text Unlimited": "Communication",
    "Google Voice": "Communication",
    "Google Chat": "Communication",
    "Burner: Second Phone Number": "Communication",

    # ── Productivity & Office ─────────────────────────────────────────────
    "Google Docs": "Productivity",
    "Google Sheets": "Productivity",
    "Google Slides": "Productivity",
    "Google Keep - Notes and lists": "Productivity",
    "Google Tasks": "Productivity",
    "Google Calendar": "Productivity",
    "Notion: Notes, Tasks, AI": "Productivity",
    "Obsidian": "Productivity",
    "Notepad - simple notes": "Productivity",
    "Notepad, Notes, Easy Notebook": "Productivity",
    "Slack": "Productivity",
    "Microsoft Teams": "Productivity",
    "Microsoft Outlook": "Productivity",
    "Microsoft OneNote: Save Notes": "Productivity",
    "Microsoft OneDrive": "Productivity",
    "Microsoft Copilot": "Productivity",
    "Zoom Workplace": "Productivity",
    "Webex": "Productivity",
    "GoTo": "Productivity",
    "Video Meeting": "Productivity",
    "Gmail": "Productivity",
    "Yahoo Mail: Email & Planner": "Productivity",
    "Proton Mail: Encrypted Email": "Productivity",
    "Docusign - Upload & Sign Docs": "Productivity",
    "Invoice Maker - Invoice Fly": "Productivity",
    "Tasker": "Productivity",
    "Calendar 2026": "Productivity",
    "Calendar For Android": "Productivity",
    "Toki - The AI Calendar": "Productivity",
    "Grammarly-AI Writing Assistant": "Productivity",
    "OtterAI Transcribe Voice Notes": "Productivity",
    "Summary - AI Note Taker": "Productivity",
    "Typeless: AI Voice Keyboard": "Productivity",
    "Wispr Flow: AI Voice-to-Text": "Productivity",
    "Speechify – Text to Speech": "Productivity",
    "Gboard - the Google Keyboard": "Productivity",
    "Connecteam Team Management App": "Productivity",
    "Shopify: Sell online/in person": "Productivity",
    "Square Point of Sale: Payment": "Productivity",
    "Meta Business Suite": "Productivity",

    # ── AI & Chat Assistants ──────────────────────────────────────────────
    "ChatGPT": "AI Assistant",
    "Google Gemini": "AI Assistant",
    "Google NotebookLM": "AI Assistant",
    "Claude by Anthropic": "AI Assistant",
    "DeepSeek - AI Assistant": "AI Assistant",
    "Perplexity - Ask Anything": "AI Assistant",
    "Grok": "AI Assistant",
    "Grok - Smartest AI Advisor": "AI Assistant",
    "AI Chat: All in One": "AI Assistant",
    "AI Chatbot - Nova": "AI Assistant",
    "AI Chat・Ask Chatbot Assistant": "AI Assistant",
    "AI! Chatbot Agent－Ask & Chat": "AI Assistant",
    "Chat AI: Ask Agent Anything": "AI Assistant",
    "Chat Smith: AI Chatbot & Agent": "AI Assistant",
    "ChatGO: AI Chatbot Assistant": "AI Assistant",
    "Chatbot AI - Search Assistant": "AI Assistant",
    "Open Chat - AI bot app": "AI Assistant",
    "Accio: Alibaba AI Agent": "AI Assistant",
    "Manus AI": "AI Assistant",
    "WolframAlpha Classic": "AI Assistant",
    "AI Hub: Photo, Video Generator": "AI Assistant",
    "Hype AI - AI Photo & Video": "AI Assistant",
    "Beatron - AI Music Maker": "AI Assistant",

    # ── Education & Learning ──────────────────────────────────────────────
    "Duolingo: Language Lessons": "Education",
    "Learn to Read - Duolingo ABC": "Education",
    "Babbel - Learn Languages": "Education",
    "Busuu: Learn & Speak Languages": "Education",
    "HelloTalk - Learn Languages": "Education",
    "Pimsleur | Language Learning": "Education",
    "Speak: Language Learning": "Education",
    "Speak English with Loora AI": "Education",
    "Praktika – AI Language Tutor": "Education",
    "Langify - AI Language Tutor": "Education",
    "BetterSpeak: AI Language Tutor": "Education",
    "Learn English, Spanish: Learna": "Education",
    "Lingvano: Sign Language - ASL": "Education",
    "Khan Academy": "Education",
    "Khan Academy Kids": "Education",
    "Coursera: Grow your career": "Education",
    "IXL": "Education",
    "Quizlet: More than Flashcards": "Education",
    "AnkiDroid Flashcards": "Education",
    "Kahoot! Play & Create Quizzes": "Education",
    "Gauth: AI Study Companion": "Education",
    "Knowunity: AI Study & Homework": "Education",
    "Solvely: AI Math & Homework": "Education",
    "ABCmouse: Kids Learning Games": "Education",
    "Buddy.ai: Kids Learning Games": "Education",
    "Kiddopia - Kids Learning Games": "Education",
    "SplashLearn: Kids Learning App": "Education",
    "Epic: Kids' Books & Reading": "Education",
    "Lingokids - Play and Learn": "Education",
    "Starfall": "Education",
    "Learn to Read: Reading.com": "Education",
    "ClassDojo": "Education",
    "Remind: School Communication": "Education",
    "Canvas By Instructure": "Education",
    "Campus Student": "Education",
    "Minecraft Education": "Education",
    "Minecraft Education Preview": "Education",
    "Clever: Brain Training Games": "Education",
    "Elevate - Brain Training Games": "Education",
    "IQ Booster: Brain Games & Test": "Education",
    "DMV Permit Practice Test 2026": "Education",
    "Driver Written Test: 2026 Test": "Education",
    "Zutobi: Permit & Driving Prep": "Education",
    "Vocabulary - Learn words daily": "Education",
    "PragerU": "Education",
    "Bible App for Kids": "Education",
    "Simple Bible Daily Verse Alarm": "Education",
    "Blinkist: Book Summaries Daily": "Education",
    "Headway - Daily Micro Learning": "Education",
    "Deepstash: Smarter Every Day!": "Education",
    "Nibble: Your Bite of Knowledge": "Education",
    "SmartyMe: Micro Learning App": "Education",
    "Learn Python Coding - Mimo": "Education",
    "Build Your First Game": "Education",
    "Easy Draw: Learn How to Draw": "Education",
    "Simply Draw: Learn to Draw": "Education",
    "Simply Guitar - Learn Guitar": "Education",
    "Simply Piano: Learn Piano Fast": "Education",
    "Yousician: Learn & Play Guitar": "Education",
    "Pok Pok | Montessori Preschool": "Education",
    "Potty with Pull-Ups ft. Disney": "Education",
    "Finelo: Master Trading": "Education",

    # ── Developer Tools ───────────────────────────────────────────────────
    "GitHub": "Developer Tools",
    "Replit": "Developer Tools",
    "Replit: Vibe code with AI Fast": "Developer Tools",
    "Emergent AI: Vibe Code Apps": "Developer Tools",
    "Base44: Build Apps with AI": "Developer Tools",
    "Builda - Create and Play": "Developer Tools",

    # ── Document & Scanner ────────────────────────────────────────────────
    "Adobe Acrobat Reader: Edit PDF": "Documents",
    "Adobe Scan AI PDF Scanner, OCR": "Documents",
    "CamScanner- scanner, PDF maker": "Documents",
    "ACE Scanner - PDF Scanner App": "Documents",
    "TapScanner": "Documents",
    "All PDF Reader": "Documents",
    "PDF Reader": "Documents",
    "PDF Reader - All PDF Scanner": "Documents",
    "PDF Reader - PDF Converter": "Documents",
    "PDF Reader - PDF Viewer": "Documents",
    "PDF Reader Zone": "Documents",
    "PDF Reader – PDF Viewer": "Documents",
    "PDF Reader, Editor & Scanner": "Documents",
    "PDF Toolkit - Reader": "Documents",
    "Keep PDF - PDF Reader": "Documents",
    "Image to PDF - PDF Converter": "Documents",
    "All Document Combo": "Documents",
    "All Document Reader:PDF Viewer": "Documents",
    "Document Reader & PDF Editor": "Documents",
    "Word Document: DOCX, PDF, XLSX": "Documents",
    "Word Office: Docs Reader": "Documents",
    "PDF & Launcher for Android": "Documents",

    # ── Web Browsers ──────────────────────────────────────────────────────
    "Google Chrome": "Browser",
    "Brave Private Web Browser, VPN": "Browser",
    "Firefox Fast & Private Browser": "Browser",
    "DuckDuckGo, Duck.ai, & VPN": "Browser",
    "Microsoft Edge: AI browser": "Browser",
    "Opera: Private Web Browser": "Browser",
    "UC Browser": "Browser",
    "Tor Browser": "Browser",
    "Ai Browser - Safe Web": "Browser",
    "Neuro Browser – Fast Video": "Browser",
    "Scano Browser": "Browser",

    # ── Translation ───────────────────────────────────────────────────────
    "Deep Translate - All Language": "Translation",
    "Translate - Translator": "Translation",
    "All Translate: Photo, PDF, DOC": "Translation",

    # ── Phone & Call Management ───────────────────────────────────────────
    "Truecaller: Spam Call Blocker": "Phone",
    "CallApp: Caller ID & Block": "Phone",
    "Eyecon Caller ID & Spam Block": "Phone",
    "Call Block: Filter and Blocker": "Phone",
    "Call Blocker - Block Numbers": "Phone",
    "Clap To Find Phone:Alarm&Find": "Phone",
    "Find My Phone by Clap Launcher": "Phone",
    "Alarm Clock": "Phone",
    "Alarm Clock - Wake Up Gently": "Phone",
    "Alarmy - Alarm Clock & Sleep": "Phone",
    "Contacts (Google)": "Phone",

    # ── Security & Privacy ────────────────────────────────────────────────
    "App Lock - Applock Fingerprint": "Security",
    "App Lock - Fingerprint Lock": "Security",
    "AppLock Pro - App Lock & Guard": "Security",
    "Authenticator App": "Security",
    "Microsoft Authenticator": "Security",
    "Duo Mobile": "Security",
    "ID.me Authenticator": "Security",
    "Permission Guard": "Security",
    "Yoti - your digital identity": "Security",

    # ── Utilities & Tools ─────────────────────────────────────────────────
    "Calculator": "Utilities",
    "QR & Barcode Scanner": "Utilities",
    "QR scanner launcher": "Utilities",
    "File Manager": "Utilities",
    "File Master - Clean & Manager": "Utilities",
    "Gallery": "Utilities",
    "Smart Transfer: Copy My Data": "Utilities",
    "Link to Windows": "Utilities",
    "Clean Utility Toolkit": "Utilities",
    "AVG Cleaner – Storage Cleaner": "Utilities",
    "Cleanfox: Spam & Email Cleaner": "Utilities",
    "EasyClean - File Cleaner": "Utilities",
    "MiraClean - File Manager": "Utilities",
    "ScanNow Home": "Utilities",
    "Analyze WiFi Launcher": "Utilities",
    "Duck Blast Launcher": "Utilities",
    "Portable WiFi - Mobile Hotspot": "Utilities",
    "inskam": "Utilities",
    "Photo Recover Plus - Restore": "Utilities",
    "WakeBox": "Utilities",

    # ── Nature & Identification ───────────────────────────────────────────
    "PictureThis - Plant Identifier": "Nature",
    "PlantIn Plant Identifier, Care": "Nature",
    "PlantNet Plant Identification": "Nature",
    "Plant App - Plant Identifier": "Nature",
    "Picture Insect: Bug Identifier": "Nature",
    "Seek by iNaturalist": "Nature",
    "iNaturalist": "Nature",
    "Star Walk 2 Plus: Sky Map View": "Nature",
    "Stellarium Mobile - Star Map": "Nature",
    "Watch Duty": "Nature",
    "Woofz - Puppy and Dog Training": "Nature",

    # ── Finance & Payments ────────────────────────────────────────────────
    "Cash App": "Finance",
    "PayPal": "Finance",
    "OnePay": "Finance",
    "Wallet - Digital Wallet Card": "Finance",
    "Gocrypto: Crypto Trading": "Finance",
    "SimplyWise Cost Estimator": "Finance",
    "Capital One Travel": "Finance",

    # ── Work & HR ─────────────────────────────────────────────────────────
    "ADP Mobile Solutions": "Work",
    "Dayforce": "Work",
    "Homebase: Scheduling & Payroll": "Work",
    "Paychex Flex": "Work",
    "Paylocity": "Work",
    "QuickBooks Workforce": "Work",
    "UKG Pro": "Work",
    "UKG Ready": "Work",
    "Workday": "Work",
    "MyWalmart": "Work",
    "brightwheel: Childcare App": "Work",
    "ParentSquare": "Work",

    # ── Jobs & Gig Economy ────────────────────────────────────────────────
    "Indeed Job Search": "Jobs",
    "LinkedIn": "Jobs",
    "Glassdoor": "Jobs",
    "Job Search by ZipRecruiter": "Jobs",
    "Fiverr - Freelance Service": "Jobs",
    "randstad: jobs for workers": "Jobs",
    "Instawork": "Jobs",
    "Shiftsmart - Find Work": "Jobs",
    "Amazon Flex": "Jobs",
    "DoorDash - Dasher": "Jobs",
    "Grubhub for Drivers": "Jobs",
    "Lyft Driver": "Jobs",
    "Spark Driver": "Jobs",
    "Uber - Driver": "Jobs",
    "Uber - Driver: Drive & Deliver": "Jobs",
    "DoorDash: Food, Grocery, More": "Jobs",
    "Shipt: Shopper and Driver": "Jobs",

    # ── Entertainment & Media ─────────────────────────────────────────────
    "Netflix": "Entertainment",
    "PBS KIDS Video": "Entertainment",
    "CandyJarTV": "Entertainment",
    "Reelway": "Entertainment",
    "NCAA March Madness Live": "Entertainment",
    "Baby Shark Hospital Play: Game": "Entertainment",
    "Baby Shark World for Kids": "Entertainment",
    "LEGO® DUPLO® Marvel": "Entertainment",
    "Pinkfong Baby Shark Phone Game": "Entertainment",
    "Talking Tom & Friends: World": "Entertainment",
    "Rbx Clothes Maker: Skin Editor": "Entertainment",
    "Kitcha": "Entertainment",
    "Hopenity": "Entertainment",

    # ── Shipping & Logistics ──────────────────────────────────────────────
    "FedEx Mobile": "Logistics",
    "UPS": "Logistics",
    "Package Tracker - pkge Mobile": "Logistics",
    "Public Storage": "Logistics",

    # ── Telecom ───────────────────────────────────────────────────────────
    "AT&T": "Telecom",
    "Boost Mobile": "Telecom",
    "My Straight Talk": "Telecom",
    "My Tracfone: Account Manager": "Telecom",
    "Visible": "Telecom",
    "Smart Home Manager": "Telecom",
    "HP": "Telecom",

    # ── Cloud Storage ─────────────────────────────────────────────────────
    "Dropbox: Secure Cloud Storage": "Cloud Storage",
    "Google One": "Cloud Storage",
    "MEGA": "Cloud Storage",

    # ── Shopping ──────────────────────────────────────────────────────────
    "Temu": "Shopping",
    "Walmart": "Shopping",
    "Spaces: Follow Businesses": "Shopping",

    # ── VPN & Network ─────────────────────────────────────────────────────
    "Planet Free VPN ™ Super Proxy": "VPN",
    "GTL | GettingOut": "VPN",
    "Securrus Mobile": "VPN",

    # Corrections for exact matching
    "Securus Mobile": "Communication",
    "4K Video Downloader & Player": "Utilities",
}

def make_play_store_url(app_name):
    """Generate a Play Store search URL for the app."""
    q = urllib.parse.quote(app_name)
    return f"https://play.google.com/store/search?q={q}&c=apps"

def make_slug(name):
    """Create a URL-safe slug from app name."""
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

def main():
    all_apps = []
    for fname in ['CScore1To5.json', 'CScore6789.json', 'CScore10To13.json']:
        with open(fname) as f:
            data = json.load(f)
            all_apps.extend(data['results'])

    # Deduplicate by name (keep first occurrence)
    seen = set()
    unique = []
    for a in all_apps:
        if a['name'] not in seen:
            seen.add(a['name'])
            unique.append(a)
    all_apps = unique

    # Identify any uncategorized apps
    uncategorized = [a['name'] for a in all_apps if a['name'] not in CATEGORY_MAP]
    if uncategorized:
        print(f"⚠️  {len(uncategorized)} uncategorized apps (assigned 'Other'):")
        for name in sorted(uncategorized):
            print(f"   - {name}")

    output = []
    for app in all_apps:
        category = CATEGORY_MAP.get(app['name'], 'Other')
        entry = {
            "name": app['name'],
            "slug": make_slug(app['name']),
            "category": category,
            "score": app['ai_impact_score'],
            "confidence": app['confidence'],
            "disruption_type": app['disruption_type'],
            "reasoning": app['reasoning'],
            "key_drivers": app['key_drivers'],
            "play_store_url": make_play_store_url(app['name']),
        }
        output.append(entry)

    # Sort by category then name
    output.sort(key=lambda x: (x['category'], x['name']))

    with open('apps-visualizer/data.json', 'w') as f:
        json.dump(output, f, indent=2)

    # Print summary
    from collections import Counter
    cats = Counter(e['category'] for e in output)
    print(f"\n✅ Built apps-visualizer/data.json with {len(output)} apps in {len(cats)} categories:")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"   {cat:25s} {count:3d} apps")

if __name__ == '__main__':
    main()
