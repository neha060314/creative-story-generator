import streamlit as st
from transformers import pipeline, set_seed

# 🔧 Must be the first Streamlit command
st.set_page_config(page_title="Creative Story Generator", layout="centered", page_icon="📝")

# 🔄 Load model
@st.cache_resource
def load_generator():
    return pipeline('text-generation', model='gpt2')

generator = load_generator()

# 🌟 Streamlit UI
st.title("📝 Creative Story Generator with Constraints")

# 📥 Inputs
genre = st.selectbox("Choose a Genre:", ["Fantasy", "Sci-Fi", "Mystery", "Adventure", "Romance"])
characters = st.text_input("Enter Main Characters (comma-separated):")
word_count = st.slider("Word Count", 50, 300, step=50)

# ✨ Few-shot examples
def create_few_shot_prompt(genre, characters):
    example_1 = (
        "Genre: Mystery\n"
        "Characters: Detective Miles, The Whispering Shadow\n"
        "Story:\n"
        "Detective Miles adjusted his fedora, the rain slicking the cobbled alley. He was hunting The Whispering Shadow, a phantom thief who left only riddles. A crumpled note fluttered from a fire escape: 'Where light meets dark, the truth will spark.' Miles squinted at the symbols etched on the brick wall beside it. A cryptic clock, frozen at midnight. The game was afoot.\n\n"
    )

    example_2 = (
        "Genre: Sci-Fi\n"
        "Characters: Zara, a starship mechanic, and Unit 7, a sentient wrench\n"
        "Story:\n"
        "Zara wiped grease from her brow, the engine core of the Stardust Drifter sputtering. 'Come on, Unit 7, we need that flux capacitor fixed before the asteroid field hits!' she muttered. Unit 7, a battered wrench with a built-in AI, clanked its protest. 'Calculating probability of successful recalibration... 47.3%,' it chirped. Suddenly, a new reading flashed on the console: a wormhole opening just off their port bow. An unexpected detour.\n\n"
    )

    example_3 = (
        "Genre: Fantasy\n"
        "Characters: Lyra, a wandering sorceress, and Flicker, a mischievous pixiewisp\n"
        "Story:\n"
        "Lyra adjusted the weight of her spellbook, the ancient forest canopy filtering dappled sunlight onto the mossy path. She was searching for the Sunstone, a relic said to hold immense power. Flicker, a tiny creature of pure light, zipped around her head, giggling. 'Left at the singing waterfall!' he chirped, his voice like tiny bells. They reached the waterfall, but instead of singing, it was silent. A chill wind blew through the trees, carrying a whisper: 'The stone is guarded by silence, not song.'\n\n"
    )

    user_prompt = (
        f"Genre: {genre}\n"
        f"Characters: {characters}\n"
        f"Story:\n"
    )

    return example_1 + example_2 + example_3 + user_prompt

# 🧠 Button to generate story
if st.button("Generate Story"):
    if genre and characters:
        set_seed(42)

        prompt = create_few_shot_prompt(genre, characters)

        # Convert word count to tokens (1 word ≈ 1.3 tokens)
        max_tokens = int(word_count * 1.5)
        min_tokens = int(word_count * 0.9)

        # Generate story
        output = generator(
        prompt,
        max_new_tokens=100,       
        min_length=min_tokens,    
        do_sample=True,
        temperature=0.9)[0]['generated_text']

        # ✂️ Keep only the generated story part
        story_text = output.split("Story:\n")[-1].strip()

        # Trim to exact word count
        trimmed_words = ' '.join(story_text.split()[:word_count])

        # 📤 Output
        st.subheader("✨ Your Generated Story")
        st.write(trimmed_words)

        # ⬇️ Download
        st.download_button("Download Story as .txt", trimmed_words, file_name="generated_story.txt")
    else:
        st.warning("Please enter both genre and characters.")
