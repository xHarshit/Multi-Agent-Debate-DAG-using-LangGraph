import os
from typing import TypedDict
from nodes import UserInputNode, AgentNode, MemoryNode, JudgeNode
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from colorama import Fore, Style

load_dotenv()
LOG_FILE = os.getenv("LOG_FILE", "logs/debate_log.txt")


class DebateState(TypedDict):
    topic: str
    round_no: int
    last_text: str
    speaker: str
    transcript: str


class DebateDAG:
    def __init__(self):
        self.user_input = UserInputNode()
        self.scientist = AgentNode("Scientist")
        self.philosopher = AgentNode("Philosopher")
        self.memory = MemoryNode()
        self.judge = JudgeNode()

    def log(self, text):
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(text + "\n")

    # ---- LangGraph Nodes ----

    def user_input_node(self, state: DebateState):
        topic = state["topic"]
        print(f"\nEnter topic for debate: {topic}\n")
        print("Starting debate between Scientist and Philosopher...\n")
        self.log(f"\n--- Debate on: {topic} ---")
        return {"topic": topic, "round_no": 1, "speaker": "Scientist"}

    def agent_node(self, state: DebateState):
        round_no = state["round_no"]
        speaker = state["speaker"]
        agent = self.scientist if speaker == "Scientist" else self.philosopher

        # Validation: enforce correct turn
        if (round_no % 2 == 1 and speaker != "Scientist") or (
            round_no % 2 == 0 and speaker != "Philosopher"
        ):
            raise ValueError(f"Invalid turn: {speaker} tried to speak in round {round_no}")

        memory_slice = self.memory.get_relevant_memory(speaker)
        text = agent.generate_argument(state["topic"], round_no, memory_slice)

        print(f"{Fore.BLUE if speaker=='Scientist' else Fore.GREEN}"
              f"[Round {round_no}] {speaker}: {text}{Style.RESET_ALL}")

        self.memory.update(speaker, text, round_no)
        self.log(f"Transition: {speaker} spoke in Round {round_no}")
        self.log(f"Memory after Round {round_no}:\n{self.memory.get_transcript()}\n")

        next_speaker = "Philosopher" if speaker == "Scientist" else "Scientist"
        return {
            "last_text": text,
            "round_no": round_no + 1,
            "speaker": next_speaker,
            "topic": state["topic"],
        }

    def judge_node(self, state: DebateState):
        transcript = self.memory.get_transcript()
        verdict = self.judge.evaluate(state["topic"], transcript)
        print(Fore.YELLOW + "\n" + verdict + Style.RESET_ALL)
        self.log("Transition: Debate finished → Judge node")
        self.log("\n[Judge Verdict]\n" + verdict)
        self.log("-" * 50)

        # Return transcript so LangGraph state stays valid
        return {"transcript": transcript}

    # ---- Run Debate ----
    def run(self, topic: str):
        graph = StateGraph(DebateState)
        graph.add_node("UserInput", self.user_input_node)
        graph.add_node("Agent", self.agent_node)
        graph.add_node("Judge", self.judge_node)

        # Set entry point
        graph.set_entry_point("UserInput")

        graph.add_edge("UserInput", "Agent")

        # Conditional edges: continue debate until 8 rounds, then go to Judge
        def continue_or_end(state: DebateState):
            if state["round_no"] <= 8:
                return "Agent"
            return "Judge"

        graph.add_conditional_edges("Agent", continue_or_end, {
            "Agent": "Agent",
            "Judge": "Judge"
        })

        graph.add_edge("Judge", END)

        compiled = graph.compile()
        compiled.invoke({"topic": topic, "round_no": 1, "speaker": "Scientist"})
