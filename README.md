# 🎮 Zork LLM Player - Make an AI Master the Classic Text Adventure!

Welcome to an exciting experiment where we combine classic text adventure gaming with modern AI! This project lets you turn any Large Language Model (LLM) into a Zork player and watch as it tries to navigate through one of gaming's most iconic text adventures.

## 🎯 What Makes This Fun?

- **Experiment with Different Prompts**: The real magic lies in crafting the perfect system prompt. Can you create an AI that becomes a Zork speedrunning champion? Or maybe one that role-plays as a cautious explorer? The possibilities are endless!
- **Watch AI Learning**: See how different LLMs handle the complex world of Zork, learning from their mistakes and (hopefully) improving their strategies.
- **Compare Different LLMs**: Try various language models and see which ones perform better. While we default to Groq (because it's free and fast), you can easily plug in other LLMs.
- **Analyze AI Thinking**: Get detailed insights into how AI plans each move, with comprehensive logs of its decision-making process.

## 🚀 Getting Started

### Prerequisites

You'll need:
- Python 3.8+
- An LLM API key (we recommend starting with Groq as it's free)
- All other required files (DOS Frotz, Zork game files) are included in this repository!

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/zork-llm-player.git
cd zork-llm-player
```

2. Install required dependencies:
```bash
pip install langchain-groq  # For using Groq
# or install your preferred LLM library
```

3. Set up your API key:
   - Get a free API key from [Groq](https://console.groq.com)
   - Replace the API key in `zorkv2_main.py` or set it as an environment variable

4. Run the game:
```bash
python zorkv2_main.py
```

## 🧠 Customizing the AI Player

The real fun begins when you start experimenting with different system prompts! The default prompt (found in `zorkv2_main.py`) creates a strategic player focused on optimal scoring, but you could modify it to:

- Create a role-playing AI that acts like a specific character
- Design a careful explorer that prioritizes survival
- Build a speedrunner focused on completing the game as fast as possible
- Make an AI that tries to discover all possible game responses

### Using Different LLMs

While we default to Groq (free and fast), you can easily modify `zorkv2_main.py` to use other LLMs:
- OpenAI's GPT models
- Anthropic's Claude
- Local LLMs
- Any other LLM with a Python API

## 📊 Understanding the Output

The system generates several interesting files during gameplay:

1. `game_history_{game_id}.json`
   - Watch the complete story of your AI's adventure
   - See every action and its consequences
   - Track score progression

2. `zork_performance_{game_id}_{timestamp}.csv`
   - Analyze move-by-move performance
   - Perfect for comparing different prompts or LLMs

3. `zork_planning_log_{game_id}.json`
   - Peek into the AI's "mind"
   - See how it plans each move
   - Understand its decision-making process

## 🔧 System Components

### ZorkGame Class (`zorkv2_system.py`)

The main game controller handling:
- Game process management
- State tracking and logging
- Strategic planning
- Action execution

### Main Script (`zorkv2_main.py`)

Configures:
- LLM setup
- System prompt
- Game initialization

## 📝 Contributing

Have an idea for an amazing system prompt? Found a way to make the AI player smarter? We'd love to see it! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

Share your best system prompts and their results in the Issues section!

## ⚠️ Limitations

- Performance varies by LLM
- Response time depends on API speed
- Memory constraints based on LLM context window

## 📜 License

[MIT License](LICENSE)

## 🙏 Acknowledgments

- Infocom for creating the timeless classic Zork
- Frotz project for the game interpreter
- The LangChain community
- All contributors who experiment with and improve this project

---

Ready to create your own AI Zork master? Clone the repo and start experimenting with different prompts and LLMs! Share your results and let's see who can create the most effective (or entertaining) AI player! 🚀
