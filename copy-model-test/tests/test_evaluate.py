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
class DecemberFacts(unittest.TestCase):
 def setUp(self):
  self.case={'theme_id':'christmas','product_facts':{'specific_sku':'랑드샤 베스트 티 4종 세트'},'references':[{'reference_id':'osulloc-004#s02','text':'일 년만에 돌아온 오설록 블랙 프라이데이'}]}
  self.output={'theme_id':'christmas','id':'hero','layout':'hero','title':'크리스마스의 티타임','subtitle':'랑드샤 베스트 티 4종 세트로 마음을 전해요','cta':'세트 살펴보기','period':'12월 한 달','reference_ids':['osulloc-004#s02'],'evidence':'행사명을 짧게 앞세우는 구조를 참고했습니다.','details_needed':['가격']}
 def test_known_product_and_period_allowed(self):self.assertTrue(evaluate(self.output,self.case)['passed'])
 def test_product_in_title_is_factually_present_but_warned(self):
  self.output['title']='랑드샤 베스트 티 4종 세트';self.output['subtitle']='크리스마스의 티타임'
  e=evaluate(self.output,self.case);self.assertTrue(e['passed']);self.assertIn('product_name_in_title_instead_of_subtitle',e['warnings'])
 def test_other_numbers_rejected(self):
  self.output['title']='2개 구매하면';self.assertIn('unsupported_numeric_claim',evaluate(self.output,self.case)['issues'])
 def test_invented_price_rejected(self):
  self.output['subtitle']+=' 4원';self.assertIn('unsupported_numeric_claim',evaluate(self.output,self.case)['issues'])
 def test_missing_product_rejected(self):
  self.output['subtitle']='따뜻한 티타임';self.assertIn('missing_exact_product_name',evaluate(self.output,self.case)['issues'])
 def test_changed_period_rejected(self):
  self.output['period']='1월 한 달';self.assertIn('wrong_event_period',evaluate(self.output,self.case)['issues'])
 def test_conflicting_copy_period_rejected(self):
  self.output['title']='1월의 티타임';self.assertIn('conflicting_schedule_claim',evaluate(self.output,self.case)['issues'])

if __name__=='__main__':unittest.main()
