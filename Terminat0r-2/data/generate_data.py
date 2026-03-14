# -*- coding: utf-8 -*-
"""Generate effects.json, events.json, levels.json"""
import json
import random
from pathlib import Path

DATA_DIR = Path(__file__).parent

EVENT_TYPES_EFFECTS = [
    "quest_complete", "fact_show", "level_up", "gold_earn", "xp_earn",
    "water", "food", "exercise", "room", "desk", "book", "nature", "rare", "epic"
]

EMOJI_POOLS = {
    "fire": ["🔥", "💥", "⚡", "🌋", "🌟", "✨", "💫", "⭐"],
    "gems": ["💎", "✨", "💠", "🔮", "💍", "🏆", "🎖️", "💠"],
    "coins": ["💰", "🪙", "💵", "💴", "💶", "💷", "🪙", "✨"],
    "stars": ["⭐", "🌟", "✨", "💫", "🌟", "⭐", "🌈", "☀️"],
    "sparkles": ["✨", "💫", "⭐", "🌟", "🌈", "🎆", "🎇", "💠"],
    "nature": ["🌿", "🌸", "🌺", "🍀", "🌻", "🌴", "🦋", "🐝"],
    "food": ["🍎", "🥗", "🍕", "🥑", "🍇", "🥕", "🥦", "🍓"],
    "misc": ["🎉", "🎊", "🏆", "🎯", "💪", "🧘", "📚", "✏️", "🔮", "🌟", "💎", "🔥"]
}

ALL_EMOJIS = list(set(
    sum(EMOJI_POOLS.values(), [])
))

def gen_effects():
    effects = []
    labels = [
        "Blazing Success", "Crystal Shine", "Golden Rain", "Star Burst", "Sparkle Wave",
        "Fire Trail", "Gem Flash", "Coin Shower", "Star Fall", "Magic Sparkle",
        "Blaze Glory", "Diamond Glow", "Treasure Burst", "Celestial Light", "Shimmer",
        "Inferno", "Sapphire Beam", "Gold Rush", "Stellar", "Twinkle",
        "Flame", "Ruby Blaze", "Coins Galore", "Cosmic", "Glitter",
        "Emerald Glow", "Wealth Wave", "Galaxy", "Shine", "Heat Wave",
        "Topaz Flash", "Money Rain", "Nebula", "Glisten", "Blaze",
        "Amethyst", "Fortune", "Constellation", "Radiant", "Volcanic",
        "Crystal", "Rich", "Stardust", "Luminous", "Phoenix", "Jade",
        "Bounty", "Meteor", "Brilliant", "Scorching", "Pearl", "Treasure",
        "Comet", "Glowing", "Searing", "Onyx", "Loot", "Aurora", "Sparkling",
        "Burning", "Opal", "Reward", "Supernova", "Dazzling", "Garnet",
        "Bonus", "Shooting Star", "Ember", "Aquamarine", "Prize", "Moonbeam",
        "Bright", "Flame Burst", "Turquoise", "Jackpot", "Sunray", "Vivid",
        "Fireworks", "Peridot", "Windfall", "Starlight", "Vibrant", "Explosion",
        "Citrine", "Earnings", "Moonlight", "Pulsing", "Torch", "Jasper",
        "Gain", "Dawn", "Flickering", "Bonfire", "Agate", "Profit", "Dusk",
        "Gleaming", "Campfire", "Quartz", "Income", "Twilight", "Shimmering",
        "Wildfire", "Moonstone", "Payday", "Sunrise", "Flashing", "Sunstone",
        "Bucks", "Sunset", "Blinding", "Flare", "Lapis", "Cash", "Noon",
        "Glinting", "Ignite", "Malachite", "Funds", "Midnight", "Polished",
    ]
    pools = list(EMOJI_POOLS.values())
    for i in range(520):
        ev = EVENT_TYPES_EFFECTS[i % len(EVENT_TYPES_EFFECTS)]
        if i % 3 == 0:
            combo = pools[i % len(pools)]
            emoji = "".join(random.choices(combo, k=3))
        else:
            emoji = "".join(random.choices(ALL_EMOJIS, k=random.randint(1, 3)))
        label = random.choice(labels)
        if i % 7 == 0:
            label += f" {random.randint(1, 99)}"
        effects.append({
            "id": f"eff_{i:04d}",
            "event_type": ev,
            "emoji": emoji,
            "label": label.strip()
        })
    return effects

EVENT_TYPES = [
    "cleaning", "cooking", "studying", "work", "health", "fitness", "sleep",
    "social", "reading", "writing", "exercise", "meditation", "gardening",
    "shopping", "organization", "hygiene", "meal_prep", "learning",
    "creative", "repair", "pet_care", "childcare", "commute", "admin"
]

EVENT_TITLES = {
    "cleaning": ["Vacuum floor", "Wash dishes", "Mop kitchen", "Dust shelves", "Clean bathroom", "Laundry load", "Tidy room", "Wipe counters", "Take out trash", "Organize closet", "Sweep balcony", "Clean windows", "Scrub toilet", "Change sheets", "Declutter desk"],
    "cooking": ["Make breakfast", "Prep lunch", "Cook dinner", "Bake cookies", "Make salad", "Cook pasta", "Grill vegetables", "Prepare smoothie", "Make soup", "Cook rice", "Fry eggs", "Make sandwich", "Prepare oatmeal", "Cook curry", "Make stir fry"],
    "studying": ["Read chapter", "Take notes", "Practice problems", "Review flashcards", "Watch lecture", "Complete assignment", "Write essay", "Study vocabulary", "Solve equations", "Read article", "Summarize text", "Prepare presentation", "Practice language", "Learn new topic", "Quiz yourself"],
    "work": ["Send emails", "Attend meeting", "Complete report", "Update spreadsheet", "Call client", "Review document", "Create presentation", "Organize files", "Plan sprint", "Code feature", "Fix bug", "Write documentation", "Design mockup", "Analyze data", "Present findings"],
    "health": ["Take vitamins", "Drink water", "Eat vegetables", "Check blood pressure", "Stretch routine", "Eye rest", "Meditate", "Deep breathing", "Stay hydrated", "Eat protein", "Rest day", "Sleep early", "Limit screen time", "Cold shower", "Warm bath"],
    "fitness": ["Morning run", "Gym session", "Yoga practice", "Push ups", "Squats", "Cycling", "Swimming", "HIIT workout", "Pilates", "Dance cardio", "Strength training", "Stretching", "Jump rope", "Plank hold", "Lunges"],
    "sleep": ["Go to bed early", "Power nap", "Sleep routine", "No screens before bed", "Dark room sleep", "Quality sleep", "Rest well", "Wake early", "Consistent schedule", "Relax before bed", "Comfortable pillow", "Cool room", "White noise", "Sleep mask", "No caffeine late"],
    "social": ["Call friend", "Meet for coffee", "Family dinner", "Video call", "Visit relative", "Group chat", "Birthday wish", "Help neighbor", "Team lunch", "Network event", "Reunion", "Play date", "Support group", "Game night", "Outing"],
    "reading": ["Read book", "Audiobook listen", "Magazine article", "News digest", "Poetry", "Comic", "Research paper", "Blog post", "Short story", "Non-fiction", "Fiction novel", "Biography", "Technical doc", "Self-help", "Classic literature"],
    "writing": ["Journal entry", "Blog post", "Email draft", "Creative writing", "To-do list", "Gratitude note", "Letter", "Memo", "Outline", "Script", "Poem", "Review", "Summary", "Notes", "Draft"],
    "exercise": ["Walk 30 min", "Jog", "Stairs", "Treadmill", "Elliptical", "Rowing", "Kettlebells", "Dumbbells", "Bodyweight", "Cross trainer", "Stepper", "Boxing", "Martial arts", "Hiking", "Sports game"],
    "meditation": ["5 min meditation", "Mindfulness", "Breathing exercise", "Body scan", "Loving kindness", "Guided meditation", "Silent sitting", "Morning calm", "Stress relief", "Focus session", "Gratitude meditation", "Visualization", "Mantra", "Walking meditation", "Evening unwind"],
    "gardening": ["Water plants", "Prune bushes", "Plant seeds", "Weed garden", "Fertilize", "Harvest herbs", "Repot plant", "Mow lawn", "Trim hedges", "Compost", "Mulch", "Seedling care", "Garden design", "Outdoor tidy", "Flower bed"],
    "shopping": ["Grocery run", "Buy essentials", "Compare prices", "Online order", "Farmers market", "Bulk buy", "Meal ingredients", "Household items", "Clothing", "Electronics", "Gift shopping", "Pharmacy", "Hardware store", "Bookstore", "Thrift find"],
    "organization": ["Sort desk", "File documents", "Calendar plan", "Budget update", "Tidy drawers", "Label boxes", "Digital cleanup", "Email inbox", "Photo backup", "Subscription review", "Task prioritization", "Goal tracking", "Inventory check", "Shelf organize", "Digital files"],
    "hygiene": ["Morning shower", "Brush teeth", "Skincare routine", "Hair care", "Nail trim", "Shave", "Floss", "Hand wash", "Deodorant", "Lotion", "Face mask", "Foot care", "Oil treatment", "Scalp care", "Oral care"],
    "meal_prep": ["Prep vegetables", "Portion meals", "Cook batch", "Freeze leftovers", "Plan week meals", "Snack prep", "Lunch boxes", "Smoothie bags", "Grain cook", "Protein prep", "Sauce batch", "Cut fruits", "Salad jars", "Bento prep", "Soups batch"],
    "learning": ["Online course", "Tutorial follow", "New skill", "Language lesson", "Coding practice", "Instrument practice", "Drawing practice", "Photography", "Cooking class", "DIY project", "Certification study", "Workshop attend", "Podcast learn", "Documentary", "Expert shadow"],
    "creative": ["Draw sketch", "Paint", "Photography", "Music composition", "Craft project", "Sewing", "Scrapbooking", "Calligraphy", "Pottery", "Collage", "Digital art", "Knitting", "Woodwork", "Jewelry", "Design"],
    "repair": ["Fix leak", "Replace bulb", "Tighten screws", "Unclog drain", "Patch wall", "Fix furniture", "Bike repair", "Electronics fix", "Door hinge", "Window seal", "Appliance check", "Paint touch up", "Cable organize", "Tool maintenance", "Quick fix"],
    "pet_care": ["Feed pet", "Walk dog", "Clean litter", "Brush pet", "Play fetch", "Vet visit", "Groom pet", "Pet training", "Fresh water", "Toy play", "Outdoor time", "Nail trim", "Bath time", "Treat reward", "Checkup"],
    "childcare": ["Read to child", "Play together", "Homework help", "Meal for kids", "Bath time", "Bedtime routine", "Outdoor play", "Craft activity", "Teach something", "Park visit", "Story time", "Puzzle play", "Music time", "Sports with kids", "Quality time"],
    "commute": ["Cycle to work", "Walk commute", "Public transit", "Carpool", "Listen podcast", "Plan route", "Early departure", "Park smart", "Stretch after", "Audiobook commute", "Mindful travel", "Bike maintenance", "Share ride", "Walk part way", "Relax drive"],
    "admin": ["Pay bills", "Renew license", "Update address", "Insurance review", "Tax prep", "Bank transfer", "Subscription cancel", "Appointment book", "Reservation", "Document sign", "Form submit", "Refund request", "Warranty register", "Membership renew", "Record keep"],
}

def gen_events():
    events = []
    for i in range(2000):
        ev_type = random.choice(EVENT_TYPES)
        titles = EVENT_TITLES.get(ev_type, ["Complete task"])
        title = random.choice(titles)
        if random.random() < 0.3:
            title += f" #{random.randint(1, 50)}"
        xp = random.randint(5, 100)
        gold = random.randint(5, 150)
        events.append({
            "id": i + 1,
            "event_type": ev_type,
            "title": title,
            "xp": xp,
            "gold": gold
        })
    return events

THEMES = [
    "starter", "explorer", "warrior", "mage", "chef", "scholar", "athlete", "gardener",
    "artist", "merchant", "healer", "ranger", "blacksmith", "bard", "alchemist",
    "knight", "rogue", "druid", "monk", "paladin", "necromancer", "summoner",
    "smith", "weaver", "miner", "fisher", "hunter", "farmer", "baker",
    "scribe", "oracle", "herald", "champion", "veteran", "legend", "master",
    "novice", "apprentice", "adept", "expert", "virtuoso", "sage",
    "treasure_hunter", "dragon_slayer", "peacekeeper", "voyager", "settler",
    "craftsman", "inventor", "philosopher", "scientist", "architect",
    "musician", "painter", "sculptor", "poet", "storyteller",
    "trader", "diplomat", "spy", "guardian", "sentinel",
    "elementalist", "frost_mage", "fire_master", "storm_caller", "earth_shaker",
    "shadow_walker", "light_bearer", "dawn_seeker", "twilight_guard",
    "wilderness_survivor", "urban_explorer", "cosmic_traveler", "time_keeper",
    "dreamweaver", "reality_shaper", "soul_forger", "mind_sculptor",
    "blood_warrior", "iron_will", "golden_touch", "silver_tongue",
    "emerald_heart", "ruby_spirit", "sapphire_mind", "diamond_soul",
    "phoenix_rising", "tiger_eye", "wolf_spirit", "eagle_vision",
    "lotus_master", "bamboo_dancer", "cherry_blossom", "oak_guardian",
]

def gen_levels():
    levels = []
    for lvl in range(1, 101):
        xp_req = 100 * lvl * (lvl + 1) // 2
        theme = THEMES[(lvl - 1) % len(THEMES)]
        title = f"Level {lvl} {theme.replace('_', ' ').title()}"
        levels.append({
            "level": lvl,
            "theme": theme,
            "title": title,
            "xp_required": xp_req
        })
    return levels

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_DIR / "effects.json", "w", encoding="utf-8") as f:
        json.dump(gen_effects(), f, ensure_ascii=False, indent=2)
    with open(DATA_DIR / "events.json", "w", encoding="utf-8") as f:
        json.dump(gen_events(), f, ensure_ascii=False, indent=2)
    with open(DATA_DIR / "levels.json", "w", encoding="utf-8") as f:
        json.dump(gen_levels(), f, ensure_ascii=False, indent=2)
    print("Generated: effects.json, events.json, levels.json")

if __name__ == "__main__":
    main()
