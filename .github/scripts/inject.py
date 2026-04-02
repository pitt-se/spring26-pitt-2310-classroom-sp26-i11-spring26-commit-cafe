import random
import re
import sys
from pathlib import Path

PUNS = [
    "Commit your coffee, not your code before it compiles.",
    "Espresso yourself, then push to main.",
    "Mugs before bugs.",
    "Practicing Caffeine-Driven Development (CDD).",
    "Decaf is just a failed build.",
    "Keep calm and merge the mocha.",
    "Pull, brew, rebase, repeat.",
    "Hotfixes and hot brews keep production alive.",
    "Merge conflicts taste better with espresso.",
    "Feature freeze? Time for an iced brew.",
    "Never debug before your first cup.",
    "It's not a bug, it's a feature - until the coffee wears off.",
    "I like my IDE like my coffee: dark theme, no sugarcoating.",
    "Version control your caffeine intake."
]

COMMIT_MESSAGES = [
    "fix: update brew logic after coffee review",
    "feature: add caffeinated brew status message",
    "refactor: simplify brew implementation",
]
COMMIT_MESSAGES = [
    "fix: update starter implementation",
    "feature: add CoffeeBot change",
    "refactor: adjust starter code",
]

JAVA_FILE = Path(sys.argv[1])
TARGETS = sys.argv[2:]

if not JAVA_FILE.exists():
    raise SystemExit(f"Error: {JAVA_FILE} not found")
if not TARGETS:
    raise SystemExit("Error: missing target(s)")

text = JAVA_FILE.read_text(encoding="utf-8")
pun = random.choice(PUNS)
commit_msg = random.choice(COMMIT_MESSAGES)

replacements = {
    "TODO_1A": (
        r'"Nadine";\s*//\s*STUDENT_TODO_1A:\s*Change name',
        '"CoffeeBot"; // STUDENT_TODO_1A: Change name'
    ),
    "TODO_1B": (
        r'//\s*STUDENT_TODO_1B:\s*Add a nickname or title for the barista',
        'private static String title = "[Lead Barista]"; // STUDENT_TODO_1B: Add a nickname or title for the barista'
    ),
    "TODO_2A": (
        r'//\s*STUDENT_TODO_2A:\s*Implement\s*-\s*add 1 to cups\s*&\s*print a message',
        'cups++;\n        System.out.println("CoffeeBot brewed " + drink + ". ' + pun + '");'
    ),
    "TODO_2B": (
        r'//\s*STUDENT_TODO_2B:\s*Add a second brew-related improvement',
        'System.out.println("[BOT CHECK] drink length = " + drink.length()); // STUDENT_TODO_2B: Add a second brew-related improvement'
    ),
}

new_text = text
injected = []
for TARGET in TARGETS:
    if TARGET not in replacements:
        print(f"Unknown target: {TARGET}, skipping.")
        continue
    pattern, replacement = replacements[TARGET]
    new_text, count = re.subn(pattern, replacement, new_text, count=1)
    if count == 0:
        print(f"No injectable match found for {TARGET}.")
    else:
        injected.append(TARGET)
        print(f"Injected competing change for {TARGET}")

if not injected:
    raise SystemExit(0)

JAVA_FILE.write_text(new_text, encoding="utf-8")

commit_msg_path = Path(".github/scripts/.commit_msg")
commit_msg_path.parent.mkdir(parents=True, exist_ok=True)
commit_msg_path.write_text(commit_msg, encoding="utf-8")
