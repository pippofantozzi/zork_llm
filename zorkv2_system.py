# zork_system.py

import os
import threading
import subprocess
from queue import Queue, Empty
import json
import time
import uuid
import csv
from datetime import datetime

class ZorkGame:
    def __init__(self, llm, system_prompt):
        """Initialize the Zork game with the given LLM and system prompt."""
        self.llm = llm
        self.system_prompt = system_prompt

        self.game_states = []
        self.process = None
        self.queue = Queue()
        self.current_score = 0
        self.move_number = 0
        self.game_id = str(uuid.uuid4())[:8]
        self.planning_history = []

    def start_game(self):
        """Initialize and start the Zork game process."""
        frotz_path = os.path.join(os.getcwd(), 'dfrotz.exe')
        game_file = 'zork1.z5'

        if not all(os.path.isfile(f) for f in [frotz_path, game_file]):
            raise FileNotFoundError("Required game files not found")

        self.process = subprocess.Popen(
            [frotz_path, game_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        threading.Thread(target=self._read_output, daemon=True).start()

    def _read_output(self):
        """Read output from the game process."""
        for line in iter(self.process.stdout.readline, ''):
            self.queue.put(line)
        self.process.stdout.close()

    def _extract_score(self, text):
        """Extract score from game output."""
        if 'Score: ' in text:
            try:
                score_text = text.split('Score: ')[1].split()[0]
                return int(score_text)
            except (IndexError, ValueError):
                return self.current_score
        return self.current_score

    def get_game_state(self, timeout=1.0):
        """Get the current game state."""
        outputs = []
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                line = self.queue.get_nowait()
                print(line, end='')
                outputs.append(line.strip())
                # Update score if found in output
                self.current_score = self._extract_score(' '.join(outputs))
            except Empty:
                time.sleep(0.1)

        state = ' '.join(outputs)
        self.game_states.append({
            "move_number": self.move_number,
            "game_state": state,
            "score": self.current_score,
            "timestamp": datetime.now().isoformat()
        })
        self._update_json()
        return state

    def _update_json(self):
        """Update the game history JSON file."""
        with open(f'game_history_{self.game_id}.json', 'w') as f:
            json.dump(self.game_states, f, indent=2)

    def _save_planning_log(self):
        """Save the planning history to a separate log file."""
        filename = f'zork_planning_log_{self.game_id}.json'
        with open(filename, 'w') as f:
            json.dump(self.planning_history, f, indent=2)
        return filename

    def strategic_planning(self, game_state):
        """Generate a strategic plan before taking action."""
        planning_prompt = self.system_prompt

        history_context = "Previous moves and outcomes:\n"
        for state in self.game_states[-30:]:  # Last 30 moves for context
            if 'action' in state:
                history_context += f"Move {state['move_number']}: {state['action']} (Score: {state['score']})\n"

        user_prompt = f"""Current game state:
{game_state}

Score: {self.current_score}
Moves: {self.move_number}

{history_context}

Provide your strategic analysis and next action:"""

        # Get the strategic response from the LLM
        response = self.llm.invoke([
            {"role": "system", "content": planning_prompt},
            {"role": "user", "content": user_prompt}
        ])

        # Parse the response to separate planning from action
        planning_text = response.content.strip()

        # Store the planning history
        self.planning_history.append({
            "move_number": self.move_number,
            "timestamp": datetime.now().isoformat(),
            "game_state": game_state,
            "planning_text": planning_text,
            "score": self.current_score
        })

        # Extract just the action from the planning text
        try:
            action = planning_text.split("ACTION:")[-1].strip()
        except:
            action = planning_text.split("\n")[-1].strip()  # Fallback to last line

        return planning_text, action

    def take_action(self, action, planning_text=None):
        """Execute an action in the game."""
        self.move_number += 1
        state_entry = {
            "move_number": self.move_number,
            "action": action,
            "score": self.current_score,
            "timestamp": datetime.now().isoformat()
        }

        if planning_text:
            state_entry["planning"] = planning_text

        self.game_states.append(state_entry)
        self._update_json()

        self.process.stdin.write(f"{action}\n")
        self.process.stdin.flush()
        print(f"\nExecuting action: {action}")

    def _save_performance_csv(self):
        """Save game performance data to CSV."""
        filename = f'zork_performance_{self.game_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Move Number', 'Action', 'Score', 'Timestamp', 'Planning Notes'])

            for state in self.game_states:
                if 'action' in state:
                    writer.writerow([
                        state['move_number'],
                        state['action'],
                        state['score'],
                        state['timestamp'],
                        state.get('planning', '')[:1000]  # Truncate planning notes if too long
                    ])
        return filename

    def play(self, max_moves=100):
        """Main game loop with strategic planning."""
        try:
            self.start_game()
            time.sleep(1)  # Give the game process time to initialize

            while self.move_number < max_moves:
                game_state = self.get_game_state()

                # Get both planning and action
                planning_text, action = self.strategic_planning(game_state)

                # Print the planning process
                print("\n=== STRATEGIC PLANNING ===")
                print(planning_text)
                print("========================\n")

                if action.lower() in ['quit', 'exit']:
                    break

                self.take_action(action, planning_text)
                time.sleep(1)  # Give the game time to process the action

        finally:
            if self.process:
                self.process.terminate()

            # Save final performance data
            csv_file = self._save_performance_csv()
            planning_file = self._save_planning_log()
            print(f"\nGame performance saved to: {csv_file}")
            print(f"Planning log saved to: {planning_file}")
            print(f"Final score: {self.current_score}")
            print(f"Total moves: {self.move_number}")
