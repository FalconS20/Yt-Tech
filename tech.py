import feedparser
import os
from datetime import datetime, timedelta

# Base YouTube URL for channels
BASE_YOUTUBE_URL = "https://www.youtube.com/feeds/videos.xml?channel_id="

# Define YouTube channels by categories
youtube_channels = {
    "Cybersecurity, Privacy & Digital Safety": [
        "UCvFGf8HZGZWFzpcDCqb3Lhw",  # All Things Secured
        "UCOLESdnG2yIF71N0b6-fojg",  # Cloudwards
        "UCH8rELPlKb04Auy6VIoEMRA",  # Cyber Lab
        "UCCsREoj8rSRkEvxWqxr74rQ",  # CyberNews
        "UC9EX_PSbngZP8pkPWSUpPzw",  # Cyberspatial
        "UC5KDiSAFxrDWhmysBcNqtMA",  # Eric Murphy
        "UCSuHzQ3GrHSzoBbwrIq3LLA",  # Naomi Brockwell TV
        "UCs6KfncB4OV6Vug4o_bzijg",  # Techlore
        "UC0W_BIuwk8D0Bv4THbVZZOQ"   # Surveillance Report
    ],
    "AI, Automation & Tools": [
        "UCQ-qAkbIkqjLVcpKueHbtBQ",  # Adrian Ching
        "UCn2RJFAA1ndipnVJsYAwWOw",  # AI Andy
        "UCWZwfV3ICOt3uEPpW6hYK4g",  # AI Foundations
        "UCFqXmQ56-Gp1rIKa-GoAJvQ",  # Andy Stapleton
        "UCN--o6qIVGlCJmKFXpAPMIQ",  # Annika Helendi
        "UCTs3VX60I6EKrrwdkgrwCGQ",  # Aurelius Tjin
        "UCdNj_PP__5kKtjZabuEjbqA",  # Dan Kieft
        "UCjy5wrSZmcFefxex3ljOouA",  # Demetri Panici
        "UCvX_cb1bZ4xgm4OIO_DS9Cw",  # Fluxomate
        "UCIDJH27tBTlA7jjMI5wnibA",  # FromSergio
        "UCrB7UFnkosBjAhOg3a9NdWw",  # Grace Leung
        "UCpM_g95uzZ_OyhgukvrbbiQ",  # Helena Liu
        "UCxVxcTULO9cFU6SB9qVaisQ",  # Jack Roberts
        "UCMfRfVxPrb0mMRzzfi6r2Cg",  # Lea David
        "UC7geKfz2-IH0rsgRBtHTm0g",  # Learn With Shopify
        "UC2ojq-nuP8ceeHqiroeKhBA",  # Nate Herk | AI Automation
        "UCYyaQsm2HyneP9CsIOdihBw",  # Tool Finder
        "UCwvXnrOCRlhokHlJwohf2OA",  # The AI Automators
        "UCNQbF87QPV685oFnHxb0zPg",  # Tasia Custode
        "UCmNAkARqTFvNoyxmFhKTS9Q",  # Rick Mulready
        "UCGk1LitxAZVnqQn0_nt5qxw",   # Pat Flynn
        "UCerWGX7_E2fR2spWSxAPwog",  # Efficient App (Alex & Andra)
    ],
    "Programming & Development": [
        "UCNQ6FEtztATuaVhZKCY28Yw",  # Chai aur Code
        "UC5DNytAJ6_FISueUfzZCVsw",  # Code with Ania Kubów
        "UCU-aPpP8BxAd4mDoP0OL4jQ",  # Agatha
        "UCtslD4DGH6PKyG_1gFAX7sg",  # Alexander Amini
        "UCVhQ2NnY5Rskt6UjCUkJ_DA",  # ArjanCodes
        "UCX88HOvHLtFKgAglSw6B3bQ",  # Aryan Singh
        "UCBGxe5vTiVWv7e2gP6QB1Mw",  # Boris Meinardus
        "UChPxqdfDbulLE9PyUqhijWw",  # Dipesh Malvia
        "UCtmn-DsF4BhPug-ff9LiDAA",  # Feel Free to Learn
        "UCKWaEZ-_VweaEx1j62do_vQ",  # IBM Technology
        "UCcJQ96WlEhJ0Ve0SLmU310Q",  # Internet Made Coder
        "UCKMjvg6fB6WS5WrPtbV4F5g",  # Kylie Ying
        "UCLLw7jmFsvfIVaUFsLs8mlQ",  # Luke Barousse
        "UCevUmOfLTUX9MNGJQKsPdIA",  # NeetCodeIO
        "UCSQnHL-F4wnMbg4BT-9pVSQ",  # NitMan Talks
        "UC5fs7PookxGfDPTo-RU0ReQ",  # Pavan Lalwani
        "UCHYVOFd3E5WfP5infRbuVtw",  # Pavan Sathiraju
        "UC5kuxbeWEsyFlS_6p_ncDog",  # Priya Bhatia
        "UC1mxuk7tuQT2D0qTMgKji3w",  # Very Academy
        "UCGPGirOab9EGy7VH4IwmWVQ",  # Travis Media
        "UCJQJAI7IjbLcpsjWdSzYz0Q",  # Thu Vu data analytics
        "UC4MZ7zUHb5eAxU75Dc_nqdQ",  # Tiff In Tech
        "UCHIbErciyS3Hs0kjAz-at5Q",  # Technical Suneja
        "UCNFmBuclxQPe57orKiQbyfA",  # Tanay Pratap
        "UCvEKHATlVq84hm1jduTYm8g",  # Striver
        "UCteRPiisgIoHtMgqHegpWAQ",  # Sundas Khalid
        "UCB6dvaWu0N8uVq2yKsZ5s5g",  # SuperSimpleDev
        "UCsh8qhZ4Wm2IJDRsNr_5Z0A",  # Smitha Kolan - Machine Learning Engineer
    ]
}

# Function to get videos from an RSS feed
def get_videos_from_rss(rss_url):
    try:
        feed = feedparser.parse(rss_url)
        if feed.bozo:
            raise ValueError(f"Failed to parse feed from {rss_url}. Error: {feed.bozo_exception}")

        today = datetime.now()

        # Calculate the start of the Monday two weeks ago and the end of the last Sunday
        # Monday is weekday 0, Sunday is weekday 6
        last_monday = today - timedelta(days=today.weekday() + 14)  # Start of Monday two weeks ago
        last_sunday = last_monday + timedelta(days=13, hours=23, minutes=59, seconds=59)  # End of Sunday of the second week

        videos = []

        for entry in feed.entries:
            try:
                published = datetime(*entry.published_parsed[:6])
                thumbnail_url = entry.media_thumbnail[0]['url'] if 'media_thumbnail' in entry else None

                # Check if the video was published between last Monday and last Sunday
                if last_monday <= published <= last_sunday:
                    videos.append({
                        'title': entry.title,
                        'link': entry.link,
                        'published': published,
                        'channel': feed.feed.title,
                        'thumbnail': thumbnail_url
                    })
            except Exception as e:
                print(f"Error processing entry: {e}")

        return videos
    except Exception as e:
        print(f"Error retrieving videos from {rss_url}: {e}")
        return []

# Aggregate videos by categories
all_videos_by_category = {}
for category, channels in youtube_channels.items():
    category_videos = []
    for channel_id in channels:
        rss_url = BASE_YOUTUBE_URL + channel_id
        category_videos.extend(get_videos_from_rss(rss_url))
    all_videos_by_category[category] = sorted(category_videos, key=lambda x: x['published'], reverse=True)

# Create HTML content with navbar and video cards
html_content = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Videos by Category</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&family=Kalam:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
        }

        h2 {
            text-align: center;
            font-family: 'Kalam', cursive;
            color: #333;
            margin-bottom: 20px;
        }

        .navbar {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }

        .navbar a {
            margin: 0 15px;
            text-decoration: none;
            font-weight: 600;
            color: #333;
        }

        .navbar a:hover {
            color: #007bff;
        }

        .video-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
        }

        .card {
            border: 1px solid #ddd;
            border-radius: 8px;  /* Reduced border-radius for a sharper look */
            width: 250px;
            background-color: #fff;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
            text-decoration: none;
            color: black;
            transition: transform 0.2s, box-shadow 0.2s;
            display: flex;
            flex-direction: column;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }

        .thumbnail {
            width: 100%;
            height: 150px;
            object-fit: cover;
        }

        .video-title {
            font-weight: 600;
            font-size: 1em;  /* Slightly reduced font size for titles */
            margin: 10px 0;
            padding: 0 10px;
        }

        .channel, .published {
            font-size: 0.9em;
            color: gray;
            margin-bottom: 8px;
        }

        .published {
            margin-bottom: 12px;
        }

        .category {
            margin-top: 30px;
        }

        h4{
            text-align: center;
            padding:10px;
            background-color: grey;
            color:white;
        }
    </style>
</head>
<body>

<h2>YouTube Videos by Category</h2>

<div class="navbar">
    <a href="#Cybersecurity_Privacy_and_Digital_Safety">Cybersecurity, Privacy & Digital Safety</a>
    <a href="#AI_Automation_and_Tools">AI, Automation & Tools</a>
    <a href="#Programming_and_Development">Programming & Development</a>
</div>
"""

# Loop through each category and its videos
for category, videos in all_videos_by_category.items():
    category_id = category.replace(" ", "_").replace("&", "and").replace(",", "")
    html_content += f'<div class="category" id="{category_id}"><h2>{category}</h2><div class="video-container">'

    for video in videos:
        html_content += f"""
        <a href="{video['link']}" target="_blank" class="card">
            <img src="{video['thumbnail']}" alt="{video['title']}" class="thumbnail">
            <div class="video-title">{video['title']}</div>
            <div class="channel">{video['channel']}</div>
            <div class="published">{video['published'].strftime('%d %b %Y')}</div>
        </a>
        """

    html_content += "</div></div>"

# Close HTML content
html_content += """

<h4>All content on this webpage, including YouTube videos and other media, belongs to their respective owners and is solely used to showcase user creativity.</h4>
</body>
</html>
"""

script_directory = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(script_directory, "index.html")

with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML file saved to {html_file_path}")
