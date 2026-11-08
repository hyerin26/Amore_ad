import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from run_ollama_models import validate_identity

class ModelIdentity(unittest.TestCase):
 def test_default_alias_resolving_to_thinking_is_rejected(self):
  observed={'details':{'parent_model':'dhiltgen/qwen3-vl:4b-thinking-q4_K_M-llamacpp'},'capabilities':['completion','vision','thinking']}
  with self.assertRaisesRegex(ValueError,'Thinking'):validate_identity('qwen3vl_4b',observed)
 def test_requested_instruct_variant_is_accepted(self):
  validate_identity('qwen3vl_4b',{'details':{'parent_model':'qwen3-vl:4b-instruct-q4_K_M'},'capabilities':['completion','vision']})

if __name__=='__main__':unittest.main()
