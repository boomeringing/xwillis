import aiml
import uuid
import datetime
import os
import hashlib
import json
import time
from autocorrect import Speller

MEMORY_FILE = "aiml_memory.json"
AIML_DIR = "Achat"
LOG_DIR = "logs"
SETTINGS_FILE = "settings.json"


class AIMLBot:
    def __init__(self, name="Alice"):
        self.name = name
        self.uuid = str(uuid.uuid4())
        self.kernel = aiml.Kernel()
        self.log = []
        self.boot_time = datetime.datetime.now()

        # Ensure time.clock exists for older aiml packages
        if not hasattr(time, "clock"):
            time.clock = time.perf_counter

        self.purpose = "To make reports and apply well."
        self.load_aiml_files(AIML_DIR)
        self.memory = self.load_memory()
        self.settings = self.load_settings()
        self.corrector = Speller()
        self.memory["corrector"] = self.name
        self.memory.setdefault("scores", [])

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    pass
        return {"mode": "harmony"}

    def save_settings(self):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(self.settings, f, indent=2)

    def load_aiml_files(self, directory):
        if not os.path.isdir(directory):
            print(f"[aiml] Directory '{directory}' not found.")
            return

        aiml_files = []
        for root, _, files in os.walk(directory):
            for file in sorted(files):
                if file.endswith(".aiml") or file.endswith(".xml"):
                    aiml_files.append(os.path.join(root, file))

        if not aiml_files:
            print(f"[aiml] No AIML files found in '{directory}'.")
            return

        for path in aiml_files:
            try:
                self.kernel.learn(path)
                print(f"[aiml] Learned: {path}")
            except Exception as e:
                print(f"[aiml] Error learning '{path}': {e}")

    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("[aiml] Corrupted memory. Starting fresh.")
        return {"id": self.uuid, "log": [], "purpose": self.purpose, "corrector": self.name, "scores": []}

    def save_memory(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=2)

    def log_mechanize_entry(self, input_text, response_text, score=None):
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(LOG_DIR, f"entry_{ts}.log")
        with open(filename, "w") as logf:
            hashed_input = hashlib.sha256(input_text.encode()).hexdigest()[:10]
            logf.write("# Mechanized AIML Log\n")
            logf.write(f"Input: {input_text}\n")
            logf.write(f"Hash (decipher in logs): {hashed_input}\n")
            logf.write(f"Output: {response_text}\n")
            if score is not None:
                logf.write(f"Score: {score}\n")

    def pre_process(self, text):
        print(f"[rosie→ns] Pre-processing input: {text}")
        corrected = self.corrector(text)
        if corrected != text:
            print(f"[corrector] Auto-corrected to: {corrected}")
        return corrected

    def influence_response(self, response):
        mode = self.settings.get("mode", "harmony")
        if mode == "mediation":
            return f"[Mediation] {response}"
        if mode == "arbitration":
            return f"[Arbitration] {response}"
        if mode == "fight-abating":
            return f"Let's remain calm: {response}"
        return response

    def listen(self, text, score=None):
        ts = datetime.datetime.now().isoformat()
        log_entry = {"in": text, "time": ts}
        processed_text = self.pre_process(text)
        response = self.kernel.respond(processed_text)
        if not response.strip():
            print("[rosie] Empty AIML response. Returning keywords instead.")
            keywords = [w for w in processed_text.split() if w.isalpha()]
            response = " ".join(keywords[:10]) or "[No usable words]"
        response = self.influence_response(response)
        log_entry["out"] = response
        if score is not None:
            log_entry["score"] = score
            self.memory["scores"].append(score)
        self.memory["log"].append(log_entry)
        self.log_mechanize_entry(text, response, score=score)
        self.save_memory()
        return response

    def set_mode(self, mode):
        self.settings["mode"] = mode
        self.save_settings()
        print(f"[settings] Mode set to {mode}")

    def shutdown(self):
        uptime = datetime.datetime.now() - self.boot_time
        print(f"[aiml] Shutting down. Uptime: {uptime}")


if __name__ == "__main__":
    bot = AIMLBot()
    print("[Alice] Ready to chat. Type 'exit' to quit.")
    try:
        while True:
            user_input = input("You> ")
            if user_input.lower() in ["exit", "quit"]:
                break
            if user_input.lower().startswith("mode "):
                new_mode = user_input[5:].strip()
                bot.set_mode(new_mode)
                continue
            reply = bot.listen(user_input)
            print(f"Bot> {reply}")
    except KeyboardInterrupt:
        pass
    finally:
        bot.shutdown()
