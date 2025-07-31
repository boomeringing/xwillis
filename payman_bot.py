import aiml
import psutil
import rt
import uuid
import datetime
import os
import hashlib
import json
import time
import subprocess
import secrets
import token



MEMORY_FILE = "aiml_memory.json"
AIML_DIR = "Achat"  # New directory for AIML files
LOG_DIR = "logs"



class AIMLBot:
    def __init__(self, name="Trose"):
        self.name = name
        self.uuid = str(uuid.uuid4())
        self.kernel = aiml.Kernel()
        self.log = []
        self.boot_time = datetime.datetime.now()

        # Patch deprecated time.clock if needed
        if not hasattr(time, 'clock'):
            time.clock = time.perf_counter

        self.purpose = "To make reports and apply well."
        self.load_aiml_files(AIML_DIR)
        self.memory = self.load_memory()
        self.memory["corrector"] = self.name
        self.memory["scores"] = []

        if RAM.runtime_on():
            print("[runtime] RUNTIME MODE: ON")
            ram_state = RAM.allocate_ram()
            self.memory["ram_allocation_trose"] = ram_state["trose"]
            self.memory["ram_allocation_local"] = ram_state["local"]
            RAM.write_runtime_bridge()
        else:
            print("[runtime] RUNTIME MODE: OFF")

    def load_aiml_files(self, directory):
        if not os.path.isdir(directory):
            print(f"[aiml] Directory '{directory}' not found.")
            return

        aiml_files = []
        for root, dirs, files in os.walk(directory):
            for file in sorted(files):
                if file.endswith(".aiml") or file.endswith(".xml"):
                    full_path = os.path.join(root, file)
                    aiml_files.append(full_path)

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
                with open(MEMORY_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("[aiml] Corrupted memory. Starting fresh.")
        return {"id": self.uuid, "log": [], "purpose": self.purpose, "corrector": self.name, "scores": []}

    def save_memory(self):
        with open(MEMORY_FILE, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def log_mechanize_entry(self, input_text, response_text, score=None):
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(LOG_DIR, f"entry_{ts}.log")
        with open(filename, 'w') as logf:
            hashed_input = hashlib.sha256(input_text.encode()).hexdigest()[:10]
            logf.write(f"# Mechanized AIML Log\n")
            logf.write(f"Input: {input_text}\n")
            logf.write(f"Hash (decipher in logs): {hashed_input}\n")
            logf.write(f"Output: {response_text}\n")
            if score is not None:
                logf.write(f"Score: {score}\n")

    def pre_process(self, text):
        # Simulate ns pre-filter/validation
        print(f"[rosie→ns] Pre-processing input: {text}")
        # Placeholder for advanced filter or srai cleanup
        return text

    def listen(self, text, score=None):
        ts = datetime.datetime.now().isoformat()
        log_entry = {"in": text, "time": ts}
        processed_text = self.pre_process(text)
        response = self.kernel.respond(processed_text)
        if not response.strip():
            print("[rosie] Empty AIML response. Returning keywords instead.")
            keywords = [word for word in processed_text.split() if word.isalpha()]
            response = " ".join(keywords[:10]) or "[No usable words]"
        log_entry["out"] = response
        if score is not None:
            log_entry["score"] = score
            self.memory["scores"].append(score)
        self.memory["log"].append(log_entry)
        self.log_mechanize_entry(text, response, score=score)
        self.save_memory()
        return response

    def shutdown(self):
        print(f"[aiml] Shutting down. Uptime: {datetime.datetime.now() - self.boot_time}")

if __name__ == '__main__':
    bot = AIMLBot()
    print("[trose] Ready to chat. Type 'exit' to quit.")
    try:
        while True:
            user_input = input("You> ")
            if user_input.lower() in ['exit', 'quit']:
                break
            if user_input.lower().startswith("chat "):
                input_text = user_input[5:].strip()
                reply = bot.listen(input_text)
                print(f"Rosie> {reply}")
            else:
                reply = bot.listen(user_input)
                print(f"Bot> {reply}")
    except KeyboardInterrupt:
        pass
    finally:
        bot.shutdown()
