from django.db import migrations

# Initial page copy, lifted verbatim from the templates so nothing changes
# visually. Edit any of these in the admin afterwards.
CONTENT = [
    # ---- Brand & footer ----
    ("Brand & Footer", "site_small_tagline", "Header / footer small tagline", "by MISCYL Ernakulam", False),
    ("Brand & Footer", "footer_tagline", "Footer description", "A community-driven initiative connecting blood donors with those in need.", False),
    ("Brand & Footer", "footer_copyright", "Footer copyright line", "MKB Blood Donation Forum by MISC Youth League Ernakulam. All rights reserved.", False),

    # ---- Home: hero ----
    ("Home", "home_hero_eyebrow", "Hero eyebrow", "GIVE BLOOD <span>•</span> GIVE HOPE <span>•</span> SAVE LIVES", True),
    ("Home", "home_hero_title", "Hero title", "A Community<br>That <span>Gives Life</span>", True),
    ("Home", "home_hero_description", "Hero description",
     "MKB Blood Donation Forum by MISCYL Ernakulam is a community-driven initiative to connect blood donors, support those in need, and promote a healthier, stronger society.",
     False),

    # ---- Home: hero action cards ----
    ("Home", "home_search_title", "Search card title", "Search Donor", False),
    ("Home", "home_search_text", "Search card text", "Find blood donors by blood group, location and more.", False),
    ("Home", "home_search_button", "Search card button", "Search Donor", False),
    ("Home", "home_register_title", "Register card title", "Register as Donor", False),
    ("Home", "home_register_text", "Register card text", "Join our donor network and help save lives.", False),
    ("Home", "home_register_button", "Register card button", "Register Now", False),

    # ---- Home: stats & steps ----
    ("Home", "home_stats_heading", "Stats heading", "Community at a Glance", False),
    ("Home", "home_steps_title", "How-it-works title", "How It Works", False),
    ("Home", "home_steps_subtitle", "How-it-works subtitle", "Three simple steps to give — or find — the gift of life.", False),
    ("Home", "home_step1_title", "Step 1 title", "Register", False),
    ("Home", "home_step1_text", "Step 1 text", "Share your blood group, location and contact number. It takes less than a minute.", False),
    ("Home", "home_step2_title", "Step 2 title", "Get Connected", False),
    ("Home", "home_step2_text", "Step 2 text", "When someone nearby needs your blood group, they can find and reach you directly.", False),
    ("Home", "home_step3_title", "Step 3 title", "Save a Life", False),
    ("Home", "home_step3_text", "Step 3 text", "One donation can help up to three people. Your gift becomes someone's tomorrow.", False),

    # ---- Home: initiatives ----
    ("Home", "home_initiatives_title", "Initiatives section title", "Other Youth-Led Initiatives", False),

    # ---- Home: mission & vision ----
    ("Home", "home_mission_title", "Mission title", "Our Mission", False),
    ("Home", "home_mission_text", "Mission text (blank line = new paragraph)",
     "To build a dedicated blood donor network within the Mar Koorilose Bava Church community, bringing together our members and families who are willing to donate blood and support fellow community members during medical emergencies.\n\nOur mission is to connect community donors with patients from our community who require blood, particularly those travelling from Kunnamkulam to Ernakulam for specialised medical treatment.\n\nThrough the Youth League, we aim to create a trusted and responsive support system where our community stands together in times of medical need, ensuring that no member of our community faces a blood shortage alone.",
     False),
    ("Home", "home_vision_title", "Vision title", "Our Vision", False),
    ("Home", "home_vision_text", "Vision text (blank line = new paragraph)",
     "To create a strong, united, and dependable blood donor community within Mar Koorilose Bava Church, where every eligible donor is ready to support a fellow community member in need.\n\nWe envision a community where the bond between our members extends beyond generations and geographical boundaries—from Kunnamkulam to Ernakulam—and where voluntary blood donation becomes a lasting expression of our faith, compassion, and responsibility towards one another.\n\nOur vision is to make our community a reliable lifeline for our own people, whenever and wherever they need us.",
     False),

    # ---- Home: verse band & CTA ----
    ("Home", "home_verse_quote", "Verse quote", "Freely you have received; freely give.", False),
    ("Home", "home_verse_cite", "Verse reference", "Matthew 10:8", False),
    ("Home", "home_verse_note", "Verse note", "Serving our community is how we live out our faith. Join the youth of MISC in giving hope to those who need it most.", False),
    ("Home", "home_cta_title", "Call-to-action title", "Ready to be someone's miracle?", False),
    ("Home", "home_cta_text", "Call-to-action text", "Join our growing family of donors, or find a donor when every minute counts.", False),
    ("Home", "home_cta_primary", "Call-to-action primary button", "Become a Donor", False),
    ("Home", "home_cta_secondary", "Call-to-action secondary button", "Find a Donor", False),

    # ---- About ----
    ("About", "about_hero_eyebrow", "About hero eyebrow", "ABOUT US", False),
    ("About", "about_hero_title", "About hero title", "MKB <span>Blood Donation Forum</span>", True),
    ("About", "about_hero_sub", "About hero subtitle", "by MISCYL Ernakulam", False),
    ("About", "about_hero_text", "About hero paragraph",
     "MKB Blood Donation Forum is a youth-led initiative by the Malabar Independent Syrian Church (MISC) Youth League, Ernakulam, connecting voluntary blood donors and helping patients in need. We believe in the power of community, compassion and the spirit of service.",
     False),
    ("About", "about_intro_eyebrow", "About intro eyebrow", "ABOUT", False),
    ("About", "about_intro_title", "About intro title", "MISC Youth League Ernakulam", False),
    ("About", "about_intro_text", "About intro text (blank line = new paragraph)",
     "MISC Youth League Ernakulam is the youth wing of the Malabar Independent Syrian Church (MISC). It is a vibrant and active community of more than 30 members, bringing together young people aged 18 to 45. Our Youth League aims to strengthen unity, encourage fellowship, and promote active participation among our members through various spiritual, social, charitable, and cultural activities.\n\nWe organize programs and initiatives that help members develop their talents, build strong relationships, serve the community, and uphold our Christian values and traditions. Through teamwork, dedication, and a shared sense of responsibility, MISC Youth League Ernakulam strives to make a positive impact on our church and the wider community.\n\nAnyone aged 18 to 65 can register as a donor. Our team may contact you when a matching blood group is needed in your area.",
     False),
    ("About", "about_bearers_title", "Office bearers eyebrow", "OUR OFFICE BEARERS", False),
    ("About", "about_cta_button", "About page button", "Become a Donor", False),
]


def seed(apps, schema_editor):
    SiteContent = apps.get_model("core", "SiteContent")
    for group, key, label, value, is_html in CONTENT:
        SiteContent.objects.update_or_create(
            key=key,
            defaults={
                "label": label,
                "value": value,
                "group": group,
                "is_html": is_html,
            },
        )


def unseed(apps, schema_editor):
    SiteContent = apps.get_model("core", "SiteContent")
    SiteContent.objects.filter(key__in=[row[1] for row in CONTENT]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_sitecontent"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
