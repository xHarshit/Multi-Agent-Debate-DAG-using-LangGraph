import os
import textwrap
import difflib
import google.generativeai as genai
from dotenv import load_dotenv

# Load env vars
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")


# --------- Node Definitions ---------

class UserInputNode:
    def get_topic(self, cli_topic=None):
        if cli_topic:
            return cli_topic
        return input("Enter topic for debate: ")


class AgentNode:
    def __init__(self, name):
        self.name = name
        self.memory = []

    def generate_argument(self, topic, round_no, memory_slice):
        """
        memory_slice = dict with:
            - own_last
            - opponent_last
        """
        prompt = f"""
        You are {self.name}.
        Debate the topic: '{topic}'.
        This is round {round_no}.
        Opponent said: {memory_slice.get('opponent_last', 'N/A')}.
        Your last point was: {memory_slice.get('own_last', 'N/A')}.

        Reply with exactly ONE unique sentence (15–18 words max).
        Use **very simple, clear English** (like explaining to a school student).
        Do NOT use difficult academic or complex words.
        Do NOT repeat earlier points from you or your opponent.
        """
        
        model = genai.GenerativeModel(MODEL)
        resp = model.generate_content(prompt)
        text = resp.text.strip()

        # Trim overly long responses
        words = text.split()
        if len(words) > 18:
            text = " ".join(words[:18]) + "."

        # Duplicate / similarity check
        for prev in self.memory:
            sim = difflib.SequenceMatcher(None, text, prev).ratio()
            if sim > 0.8:  # too similar
                text = "(Skipped: could not generate unique point)"
                break

        wrapped_text = textwrap.fill(text, width=80)
        self.memory.append(wrapped_text)
        return wrapped_text


class MemoryNode:
    def __init__(self):
        self.transcript = []  # list of dicts: {round, speaker, text}

    def update(self, speaker, text, round_no):
        entry = {"round": round_no, "speaker": speaker, "text": text}
        self.transcript.append(entry)

    def get_transcript(self):
        return "\n".join(
            f"[Round {e['round']}] {e['speaker']}: {e['text']}"
            for e in self.transcript
        )

    def get_relevant_memory(self, speaker):
        """Return only last self + last opponent messages"""
        own_last = None
        opponent_last = None
        for e in reversed(self.transcript):
            if e["speaker"] == speaker and own_last is None:
                own_last = e["text"]
            elif e["speaker"] != speaker and opponent_last is None:
                opponent_last = e["text"]
            if own_last and opponent_last:
                break
        return {"own_last": own_last, "opponent_last": opponent_last}


class JudgeNode:
    def evaluate(self, topic, transcript):
        prompt = f"""
Debate topic: {topic}
Transcript:
{transcript}

Provide output in this strict format:

[Judge] Summary of debate:
(2–3 sentences maximum summary here)

[Judge] Winner: (Scientist or Philosopher)

Reason: (one sentence why)
"""
        model = genai.GenerativeModel(MODEL)
        resp = model.generate_content(prompt)
        text = resp.text.strip()

        # Clean & enforce spacing
        cleaned = []
        for line in text.splitlines():
            if line.strip():
                cleaned.append(line.strip())
        formatted = "\n\n".join(cleaned)

        wrapped_text = "\n".join(
            textwrap.fill(line, width=80) if not line.startswith("[Judge]") else line
            for line in formatted.splitlines()
        )
        return wrapped_text
