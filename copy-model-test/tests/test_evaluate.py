import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evaluate import evaluate,parse_output
class CopyChecks(unittest.TestCase):
 def setUp(self):
  self.case={'theme_id':'christmas','references':[{'reference_id':'osulloc-003#s01','text':'차, 미식의 발견. 차는 미식을 완성합니다.'}]}
  self.output={'theme_id':'christmas','id':'hero','layout':'hero','title':'크리스마스에 전하는 차 한 잔','subtitle':'소중한 사람과 따뜻한 순간을 나눠보세요','cta':'차 선물 살펴보기','reference_ids':['osulloc-003#s01'],'evidence':'차를 경험과 연결하는 표현 구조를 참고했습니다.','details_needed':['상품명','행사 기간']}
 def test_valid_draft(self):self.assertTrue(evaluate(json.dumps(self.output,ensure_ascii=False),self.case)['passed'])
 def test_fence_is_normalized_but_not_strict(self):
  e=evaluate('```json\n'+json.dumps(self.output)+'\n```',self.case);self.assertTrue(e['passed']);self.assertFalse(e['strict_json'])
 def test_numeric_offer_is_rejected(self):
  self.output['subtitle']='전 상품 50% 할인';self.assertIn('unsupported_numeric_claim',evaluate(self.output,self.case)['issues'])
 def test_fabricated_source_is_rejected(self):
  self.output['reference_ids']=['osulloc-999#s01'];self.assertIn('invalid_reference_ids',evaluate(self.output,self.case)['issues'])
 def test_wrong_theme_is_rejected(self):
  self.output['theme_id']='autumn';self.assertIn('wrong_theme_id',evaluate(self.output,self.case)['issues'])
 def test_reference_season_is_not_invented(self):
  self.output['evidence']='과거 크리스마스 시즌 프로모션을 참고했습니다.';self.assertTrue(any('misattribution' in x for x in evaluate(self.output,self.case)['warnings']))
 def test_truncated_json_is_failure(self):self.assertFalse(evaluate('{"title":',self.case)['parseable'])
 def test_provider_error_text_is_not_copy(self):self.assertFalse(evaluate('Sorry, I encountered an error: quota',self.case)['parseable'])
if __name__=='__main__':unittest.main()
