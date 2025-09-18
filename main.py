import argparse
from langgraph_dag import DebateDAG

def main(cli_topic=None):
    dag = DebateDAG()
    topic = cli_topic if cli_topic else dag.user_input.get_topic()
    dag.run(topic)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", type=str, help="Debate topic")
    args = parser.parse_args()
    main(args.topic)
