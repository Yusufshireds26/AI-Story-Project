import os
import random
from textblob import TextBlob
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from fpdf import FPDF 

# Step 1: Create project folders
os.makedirs("story_results/images", exist_ok=True)

# Step 2: User Inputs
print("Welcome to the AI Story & Art Generator!\n")
prompts = []
for i in range(3):
    prompt = input(f"Enter a scene description for your story (Scene {i+1}): ")
    prompts.append(prompt)

# Step 3: Sentiment Analysis
sentiments = []
for text in prompts:
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.2:
        sentiments.append("Positive")
    elif polarity < -0.2:
        sentiments.append("Negative")
    else:
        sentiments.append("Neutral")

# Step 4: Generate placeholder AI images
for i, prompt in enumerate(prompts):
    img = Image.new("RGB", (500, 300), color=(random.randint(50,255), random.randint(50,255), random.randint(50,255)))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((20,140), f"Scene {i+1}:\n{prompt}\n({sentiments[i]})", fill="black", font=font)
   
    img_path = f"story_results/images/scene_{i+1}.png"
    img.save(img_path)
    print(f"Generated image saved: {img_path}")

# Step 5: Create Storyboard PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

for i, prompt in enumerate(prompts):
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.multi_cell(0,10, f"Scene {i+1}:\n{prompt}\nSentiment: {sentiments[i]}")
    pdf.image(f"story_results/images/scene_{i+1}.png", x=15, w=180)

pdf_output = "story_results/storyboard.pdf"
pdf.output(pdf_output)
print(f"\nStoryboard PDF generated: {pdf_output}")

# Step 6: Summary Report
report_text = "AI Story & Art Generator Report\n"
report_text += "===================================\n\n"
for i, prompt in enumerate(prompts):
    report_text += f"Scene {i+1}:\nPrompt: {prompt}\nSentiment: {sentiments[i]}\nImage: images/scene_{i+1}.png\n\n"

report_file = "story_results/reports.txt"
with open(report_file, "w") as f:
    f.write(report_text)
print(f"Text report saved: {report_file}")

# Step 7: Visual Summary
fig, axes = plt.subplots(1, 3, figsize=(15,5))
for i in range(3):
    img = Image.open(f"story_results/images/scene_{i+1}.png")
    axes[i].imshow(img)
    axes[i].axis("off")
    axes[i].set_title(f"Scene {i+1} ({sentiments[i]})")

plt.suptitle("AI Story Scenes", fontsize=16, weight="bold")
plt.tight_layout()
plt.savefig("story_results/story_summary.png", dpi=300)
plt.show()

print("\nAll results saved in 'story_results/' folder. Enjoy your AI story!")
