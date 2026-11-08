"""Infer sections from promotion markup, headings and local context.

No pixel/OCR or live-click claims are made. Paths address the saved HTML fragment.
Brand-specific selectors identify authored modules; traversal partitions wrapper
siblings as well so introductions, navigation and notices are not dropped.
"""
import re
from bs4 import Tag, NavigableString, Comment

BOUNDARIES = {
    'kakao_gift': '.cont_builder > *, .aside_layout',
    'shinsegaev': '.event-detail__vi, .event-detail__head, .event-detail__gnb, '
        '.sivEvent-M > .promotion__nav, .sivEvent-M > .promotion--visual, '
        '.sivEvent-M > .intro, .sivEvent-M > .is-hide, .sivEvent-M > .is-active, '
        '.promotion__tab-group > .promotion__tab, .promotion, '
        '.siv-popup, .popup-mini, .event-detail__coupon, .event-detail__notice, '
        '.event-detail__html-banner:not(:has(.sivEvent-M)), .event-detail__product, '
        '.event-product-filter, #prmGdLst',
    'zigzag': '#__content_editor > div:not(:last-child), '
        '[class*="QuickArtwork"], [class*="QuickBenefit"], [class*="gift-section"], '
        '[class*="QuickStore"], [class*="QuickBanner"], [class*="css-1q202gc"], '
        '[class*="css-79elbk"]',
    'hankkitongsal': '#img_container, #page_nav, #tabs > div, #product_list_component',
    'dongwonmall': '.planshop_a_head, .planshop_banner_box > div, .planshop_section, #comments_area',
    'cjthemarket': '.time__wrap, .event-nav, .event-section, .event-visual--pc, .event-page__item',
    'wconcept': 'section.Anchor, .event-info, .location',
}

def text(node):
    return re.sub(r'\s+', ' ', node.get_text(' ', strip=True)).strip()

def meaningful(node):
    if node.name in ('style','script','noscript'): return False
    return bool(text(node) or node.name in ('img','video','button','area')
                or node.select('img,video,button,area') or 'url(' in node.get('style',''))

def partition(root, brand):
    selected = root.select(BOUNDARIES.get(brand, 'section'))
    if brand == 'kolonmall':
        # UUID-named authored blocks, plus the promotion's sticky section menu.
        selected += [n for n in root.find_all(id=True)
                     if re.fullmatch(r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}', n['id'])]
        selected += root.select('[class*="pos_sticky"], [class*="pos_fixed"]')
    marked = {id(n) for n in selected}
    ancestors = set()
    for n in selected:
        for p in n.parents:
            ancestors.add(id(p))
            if p is root: break
    parts=[]
    def visit(node):
        if not meaningful(node): return
        if id(node) in marked or id(node) not in ancestors:
            parts.append(node); return
        # Wrappers should not own prose when child modules are explicit. Fail
        # rather than silently dropping any direct text between module elements.
        if any(isinstance(c,NavigableString) and not isinstance(c,Comment) and str(c).strip() for c in node.children):
            raise ValueError(f'{brand}: text-bearing wrapper {node.name} {node.get("id")} needs an explicit section boundary')
        for child in node.children:
            if isinstance(child,Tag): visit(child)
    visit(root)
    return parts

def infer_role(node, order, brand=None):
    markup = node.name+' '+node.get('id','')+' '+' '.join(node.get('class',[]))
    start = text(node)[:180]
    # These editors wrap semantic modules in generated classes; inspect the
    # authored module class rather than assigning a role from the wrapper hash.
    for child in node.select('[class*="Quick"]')[:1]:
        markup += ' ' + ' '.join(child.get('class',[]))
    if brand == 'zigzag' and node.select('img[alt="지그재그"]'):
        return 'section_navigation','navigation_markup'
    if re.search(r'comments_area',markup):return 'participation_event','container_markup'
    if re.search(r'promotion__tab(?: |$)',markup):return 'section_navigation','navigation_markup'
    if brand == 'kolonmall':
        if start.startswith('전체 남성 여성 랭킹'):return 'section_navigation','navigation_markup'
        if start.startswith('큼 슈퍼아이템'):return 'hero','heading_or_container'
        if start.startswith('베스트 랭킹'):return 'product_list','heading_or_container'
        if start.startswith('빅세일'):return 'sale_offer','heading_or_container'
        if start.startswith('라이브'):return 'sale_offer','heading_or_container'
        if start.startswith(("'큼' 콘텐츠",'이런 기획전')):return 'related_promotions','heading_or_container'
    if brand == 'dongwonmall':
        if start.startswith('우리집 냉장고엔') or (not start and order==2):return 'hero','position_in_dom'
        if start.startswith('웰니스 식탁 WITH'):return 'section_navigation','heading_or_container'
        if start.startswith(('덴마크 와 함께','덴마크 PICK 레시피')):return 'brand_story','heading_or_container'
        if start.startswith('덴마크 레시피 속'):return 'sale_offer','heading_or_container'
        if start.startswith('10% 할인 쿠폰'):return 'coupon_offer','heading_or_container'
        if start.startswith('5만원 적립금 응모'):return 'participation_event','heading_or_container'
    if brand == 'cjthemarket':
        if start.startswith('더 담을수록'):return 'coupon_offer','heading_or_container'
        if start.startswith('꼭 확인하세요'):return 'terms','heading_or_container'
        if 'event-visual--pc' in markup:return 'hero','container_markup'
    if brand == 'kakao_gift':
        if 'app-view-button' in markup:return 'participation_event','container_markup'
        if 'aside_layout' in markup:return 'product_list','container_markup'
        if 'app-view-image-banner' in markup:
            previous=node.find_previous_sibling('app-view-image-banner')
            return ('hero','position_in_dom') if previous is None else ('content','container_markup')
    if brand == 'wconcept' and node.get('id')=='section1' and node.select('img'):
        return 'hero','position_in_dom'

    # Modal template text is not an observed successful participation action.
    if re.search(r'popup|modal',markup,re.I): return 'content','container_markup'
    if re.search(r'nav|floating-tab|shortcut|gnb|filter|location|page_nav',markup,re.I):
        return 'section_navigation','navigation_markup'
    if re.search(r'notice|precaution|terms|comments_area',markup,re.I) or re.match(r'꼭 읽어|유의사항|알려드립니다',start):
        return 'terms','heading_or_container'
    if re.search(r'coupon|QuickBenefit',markup,re.I) or re.match(r'COUPON|스페셜 쿠폰|10% 장바구니',start,re.I):
        return 'coupon_offer','heading_or_container'
    if re.search(r'winning-event|first-point|new-member|first-come|first-buy',markup,re.I) or re.match(r'데일리 랜덤|구매 리워드|12쌍|EVENT |.*스탬프 찍고',start):
        return 'participation_event','heading_or_container'
    if re.search(r'related|promotion-list|brand-promotion|group-benefit',markup,re.I):
        return 'related_promotions','container_markup'
    if re.search(r'main-banner|main-visual|promotion--visual|QuickArtwork|img_container',markup,re.I):
        return 'hero','container_markup'
    if re.search(r'product|prdList|planshop_section|promotion--best|ranking',markup,re.I):
        return 'product_list','product_links' if node.select('a[href]') else 'container_markup'
    if re.search(r'card-benefit|payment-benefit|promotion--benefit|payback',markup,re.I) or re.match(r'결제 혜택|쓱데이 혜택',start):
        return 'benefit_overview','heading_or_container'
    if re.search(r'brand-day|corner-brand',markup,re.I) or re.match(r'브랜드데이|카테고리데이|하루특가|슈퍼아이템',start):
        return 'sale_offer','heading_or_container'
    if re.search(r'QuickStore',markup,re.I):return 'related_promotions','container_markup'
    if re.search(r'QuickBanner',markup,re.I):return 'sale_offer','container_markup'
    if re.match(r'NEW ITEM|BEST ITEM|MORE カ|MORE 카테고리|그룹 1',start):return 'product_list','heading_or_container'
    if start in ('NEW','BEST','MORE'):return 'section_navigation','navigation_markup'
    if re.search(r'intro|corner-text',markup,re.I):return 'brand_story','container_markup'
    if re.match(r'공유|이벤트 공유',start):return 'share','heading_or_container'
    if order==1 and node.select('img,video'):return 'hero','position_in_dom'
    return 'content','container_markup'
