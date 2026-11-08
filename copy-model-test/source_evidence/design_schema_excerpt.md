# 확인한 디자인 시스템 필드

원본: https://github.com/EunseongOH/tea_ad/blob/main/src/app.js

```javascript
const LAYOUTS = [
 {id:'hero',name:'단일 메인 비주얼',cat:'메인·비주얼',slots:0,fixed:true,desc:'이미지와 헤드라인 중심'},
 {id:'grid2',name:'2열 상품 그리드',cat:'상품 큐레이션',slots:2,fixed:false,desc:'카드 개수 자유 조절'},
 {id:'grid3',name:'3열 상품 그리드',cat:'상품 큐레이션',slots:3,fixed:false,desc:'작은 상품 카드 반복'},
 {id:'split',name:'강조형 비대칭 배치',cat:'상품 큐레이션',slots:2,fixed:true,desc:'고정 슬롯 2개 유지'},
 {id:'benefit',name:'혜택 안내',cat:'혜택·프로모션',slots:0,fixed:true,desc:'텍스트·혜택 강조'},
 {id:'editorial',name:'텍스트 + CTA',cat:'스토리',slots:0,fixed:true,desc:'설명과 행동 유도'}
];
```

실제 편집 문구: `section.title`, `section.subtitle`, `section.cta`.
구좌 배치와 기존 데이터는 수정하지 않고 별도의 추천 초안으로 반환합니다.

`design/UX_WRITING.md`의 해요체 규칙은 시스템 안내 UI에 대한 규칙이며, 기존 소비자 프로모션 카피를 자동 교정하지 않는 범위입니다.
