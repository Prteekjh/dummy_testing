# dummy_testing

## Terminal GPT-4o Chat Client

This repository now includes `chat_cli.py`, a small terminal chat interface for OpenAI's GPT-4o model.

### Prerequisites

1. Install dependencies:
   ```bash
   pip install openai
   ```
2. Export your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="sk-your-key"
   ```

### Usage

Run the chat client from the repository root:

```bash
python chat_cli.py --system "You are a helpful assistant." --temperature 0.6
```

Arguments:
- `--model`: Override the model name (defaults to `gpt-4o`).
- `--system`: Optional system prompt to prime the assistant.
- `--temperature`: Sampling temperature between 0 and 2 (default `0.7`).

Type messages at the `You:` prompt. Enter `exit`, `quit`, or press `Ctrl-D` to finish the session.
