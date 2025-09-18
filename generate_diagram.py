from graphviz import Digraph

def generate_diagram():
    dot = Digraph("DebateDAG", format="png")
    dot.attr(rankdir="LR", size="12,8", dpi="200")  # bigger, higher resolution
    dot.attr("node", fontsize="18", fontname="Helvetica-Bold")  # bold font for nodes
    dot.attr("edge", fontsize="16", fontname="Helvetica-Bold")  # bold font for edges

    # Nodes with bold labels
    dot.node("UserInput", "<<B>UserInput</B><BR/>(Topic)>", shape="parallelogram",
             style="filled", fillcolor="orange", width="2.5", height="1.2")
    dot.node("Scientist", "<<B>Agent A</B><BR/>(Scientist)>", shape="box",
             style="filled", fillcolor="lightblue", width="3", height="1.2")
    dot.node("Philosopher", "<<B>Agent B</B><BR/>(Philosopher)>", shape="box",
             style="filled", fillcolor="lightgreen", width="3", height="1.2")
    dot.node("Memory", "<<B>MemoryNode</B><BR/>(Transcript + Relevant Slice)>", shape="folder",
             style="filled", fillcolor="lightgrey", width="3.5", height="1.2")
    dot.node("Judge", "<<B>JudgeNode</B><BR/>(Summary + Winner)>", shape="ellipse",
             style="filled", fillcolor="yellow", width="3.5", height="1.2")
    dot.node("END", "<<B>END</B>>", shape="doublecircle",
             style="filled", fillcolor="red", width="1.5", height="1.2")

    # Bold edge labels
    dot.edge("UserInput", "Scientist", label="<<B>start debate</B>>")
    dot.edge("Scientist", "Memory", label="<<B>store + update</B>>")
    dot.edge("Philosopher", "Memory", label="<<B>store + update</B>>")

    dot.edge("Memory", "Philosopher", label="<<B>next turn (even rounds)</B>>")
    dot.edge("Memory", "Scientist", label="<<B>next turn (odd rounds)</B>>")

    dot.edge("Memory", "Judge", label="<<B>after round 8 → evaluate</B>>")
    dot.edge("Judge", "END", label="<<B>final verdict</B>>")

    # Render
    dot.render("dag_diagram", cleanup=True)
    print("DAG diagram saved as dag_diagram.png (bold text, larger size)")

if __name__ == "__main__":
    generate_diagram()
