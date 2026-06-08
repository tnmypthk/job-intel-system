import yaml

with open("config.yaml") as f:
    _config = yaml.safe_load(f)

MODEL = _config["llm"]["model"]
MAX_ITER = _config["agents"]["max_iter"]
DEV_JOB_URL = _config["dev"]["job_url"]
DEV_RESUME_FILE = _config["dev"]["resume_file"]