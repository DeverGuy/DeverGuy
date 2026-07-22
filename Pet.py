import urllib.request
import re
import os

# --- Configuration ---
USERNAME = "DeverGuy"
README_PATH = "README.md"
STREAK_URL = f"https://github-readme-streak-stats.herokuapp.com/?user={USERNAME}"

# Eeveelutions Pokemon IDs from PokeAPI
EEVEE = 133
JOLTEON = 135
UMBREON = 197
SYLVEON = 700

def get_current_streak():
    try:
        req = urllib.request.Request(STREAK_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            svg_data = response.read().decode('utf-8')
            
        # Extract the streak number using regex
        match = re.search(r"currstreak.*?>(.*?)<\/text>", svg_data, re.IGNORECASE | re.DOTALL)
        if match:
            streak = int(match.group(1).strip())
            return streak
    except Exception as e:
        print(f"Error fetching streak: {e}")
    return 0

def get_pet_id(streak):
    if streak < 3:
        return EEVEE, "Eevee"
    elif streak < 10:
        return JOLTEON, "Jolteon"
    elif streak < 20:
        return UMBREON, "Umbreon"
    else:
        return SYLVEON, "Sylveon"

def update_readme(pet_id, pet_name):
    if not os.path.exists(README_PATH):
        print(f"Error: {README_PATH} not found.")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # The new animated image tag
    pet_img = f'<img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/{pet_id}.gif" width="60" alt="{pet_name}">'
    
    # Replace everything between <!-- PET-START --> and <!-- PET-END -->
    pattern = r"(<!-- PET-START -->\n).*?(\n\s*<!-- PET-END -->)"
    new_content = re.sub(pattern, rf"\1  {pet_img}\2", content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"Updated README with {pet_name} (Streak: {streak})")

if __name__ == "__main__":
    streak = get_current_streak()
    pet_id, pet_name = get_pet_id(streak)
    update_readme(pet_id, pet_name)
