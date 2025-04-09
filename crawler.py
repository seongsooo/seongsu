import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def main():
    # CSV 파일 경로 직접 지정
    csv_path = r"./file.csv"
    
    # CSV 파일 읽기
    df_apps = pd.read_csv(csv_path)
    apps = []
    for _, row in df_apps.iterrows():
        app_name = str(row['appname']).strip()
        url = str(row['link']).strip()
        apps.append({"app_name": app_name, "url": url})

    # 첫 번째 드롭다운: 리뷰 정렬 (Most recent)
    SORT_DROPDOWN_SELECTOR = (
        "#reviews > div > div.xeuugli.x2lwn1j.x78zum5.xdt5ytf.xozqiw3.xi32cqo > "
        "div.xeuugli.x2lwn1j.x78zum5.xdt5ytf.xozqiw3.xgpatz3 > "
        "div.xeuugli.x2lwn1j.x78zum5.x1q0g3np.xozqiw3.x40hh3e > "
        "label:nth-child(1) > div.x1n2onr6 > select"
    )
    # 두 번째 드롭다운: 별점 필터 (기본값 'All', 이후 옵션: 5점, 4점, 3점, 2점, 1점)
    RATING_DROPDOWN_SELECTOR = (
        "#reviews > div > div.xeuugli.x2lwn1j.x78zum5.xdt5ytf.xozqiw3.xi32cqo > "
        "div.xeuugli.x2lwn1j.x78zum5.xdt5ytf.xozqiw3.xgpatz3 > "
        "div.xeuugli.x2lwn1j.x78zum5.x1q0g3np.xozqiw3.x40hh3e > "
        "label:nth-child(2) > div.x1n2onr6 > select"
    )
    
    # 리뷰 영역 및 "더보기" 버튼 관련 셀렉터
    PARENT_CONTAINER_SELECTOR = (
        "#reviews > div > div.xeuugli.x2lwn1j.x78zum5.xdt5ytf.xozqiw3.xi32cqo > "
        "div.xeuugli.x2lwn1j.x78zum5.xdt5ytf.xozqiw3.xgpatz3"
    )
    LOAD_MORE_RELATIVE_SELECTOR = (
        "div.x1i10hfl.x1qjc9v5.xjbqb8w.x1ypdohk.xdl72j9.xdt5ytf.x2lah0s.xe8uvvx."
        "xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.x16tdsg8.xggy1nq."
        "x1ja2u2z.x1t137rt.x1hl2dhg.x1lku1pv.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi."
        "xamhcws.xol2nv.xlxy82.x19p7ews.xdxvlk3.x1fglp.x1rp6h8o.xg6i1s1.x9f619."
        "x2wh2y9.x1n2onr6.x87ps6o.x889kno.x1a8lsjc.x1g8yoln.xe53cfu.xwji4o3."
        "x1g2r6go.xmy21w2.xcmpseh.xveyzlu.xtu2ozf.x1xrw417.x1rg5ohu"
    )
    LOAD_MORE_SELECTOR = f"{PARENT_CONTAINER_SELECTOR} > {LOAD_MORE_RELATIVE_SELECTOR}"
    REVIEWS_SELECTOR = f"{PARENT_CONTAINER_SELECTOR} > div:not({LOAD_MORE_RELATIVE_SELECTOR})"
    
    # 개별 리뷰 내부 데이터 경로
    USERNAME_SELECTOR = ".xp1r0qw > .xeuugli > .x16g9bbj"
    RATING_SELECTOR = 'div[aria-label*="out of"]'
    TITLE_SELECTOR = ".xfex06f > .x16g9bbj"
    CONTENT_SELECTOR = "span:nth-of-type(1) > .x16g9bbj"
    UPVOTE_SELECTOR = ".x6s0dn4 > div:nth-of-type(1) > .xt0psk2 > .x6s0dn4 > .x1n2onr6 > .x1heor9g"
    
    # 별점 필터 옵션에 대한 매핑
    rating_filter_mapping = {1: "5", 2: "4", 3: "3", 4: "2", 5: "1"}
    
    all_reviews = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # 각 앱에 대해 처리
        for app in apps:
            app_name = app["app_name"]
            url = app["url"]
            print(f"앱: {app_name} / {url}")
            
            # 별점 옵션 별로 반복 (0번 'All'은 패스)
            for rating_index in range(1, 6):  # rating_index: 1~5 (즉, 5점부터 1점까지)
                print(f"  별점 필터: {rating_filter_mapping[rating_index]}점")
                # 각 별점 옵션마다 새 컨텍스트 생성 (페이지 새로 로드)
                context = browser.new_context(locale="en-US")
                page = context.new_page()
                page.goto(url)
                
                # 드롭다운에서 "Most recent" 선택 (첫 번째 드롭다운: 두 번째 옵션, index=1)
                try:
                    page.wait_for_selector(SORT_DROPDOWN_SELECTOR, timeout=10000)
                    page.select_option(SORT_DROPDOWN_SELECTOR, index=1)
                    page.wait_for_timeout(2000)
                except Exception as e:
                    print(f"    {app_name} 드롭다운 정렬 오류: {e}")
                
                # 별점 필터 선택 (두 번째 드롭다운; 0번은 'All'이므로, 원하는 rating_index 사용)
                try:
                    page.wait_for_selector(RATING_DROPDOWN_SELECTOR, timeout=10000)
                    page.select_option(RATING_DROPDOWN_SELECTOR, index=rating_index)
                    page.wait_for_timeout(2000)
                except Exception as e:
                    print(f"    {app_name} 별점 필터 선택 오류: {e}")
                
                # 리뷰 영역 로드 대기
                try:
                    page.wait_for_selector(PARENT_CONTAINER_SELECTOR, timeout=10000)
                except Exception as e:
                    print(f"    {app_name} 리뷰 영역 로드 실패: {e}")
                    context.close()
                    continue
                
                # "더보기" 버튼 반복 클릭하여 모든 리뷰 로드
                while True:
                    load_more_button = page.query_selector(LOAD_MORE_SELECTOR)
                    if not load_more_button:
                        break
                    try:
                        load_more_button.click()
                        page.wait_for_timeout(3000)
                    except Exception as e:
                        print(f"    {app_name} 더보기 클릭 오류: {e}")
                        break
                
                # 리뷰 수집
                review_elements = page.query_selector_all(REVIEWS_SELECTOR)
                print(f"    {app_name} - {rating_filter_mapping[rating_index]}점: {len(review_elements)}개 리뷰 발견")
                for review in review_elements:
                    try:
                        username_elem = review.query_selector(USERNAME_SELECTOR)
                        username = username_elem.inner_text().strip() if username_elem else None
                    except Exception:
                        username = None

                    try:
                        rating_elem = review.query_selector(RATING_SELECTOR)
                        rating = rating_elem.get_attribute("aria-label").strip() if rating_elem else None
                    except Exception:
                        rating = None

                    try:
                        title_elem = review.query_selector(TITLE_SELECTOR)
                        title = title_elem.inner_text().strip() if title_elem else None
                    except Exception:
                        title = None

                    try:
                        content_elem = review.query_selector(CONTENT_SELECTOR)
                        content = content_elem.inner_text().strip() if content_elem else None
                    except Exception:
                        content = None

                    try:
                        upvote_elem = review.query_selector(UPVOTE_SELECTOR)
                        upvote = upvote_elem.inner_text().strip() if upvote_elem else None
                    except Exception:
                        upvote = None

                    review_data = {
                        "app_name": app_name,
                        "url": url,
                        "rating_filter": rating_filter_mapping[rating_index],
                        "username": username,
                        "rating": rating,
                        "title": title,
                        "content": content,
                        "upvote": upvote,
                    }
                    all_reviews.append(review_data)
                
                context.close()
                print(f"    {app_name} - {rating_filter_mapping[rating_index]}점 리뷰 수집 완료.\n")
            print(f"{app_name} 전체 별점 필터 리뷰 수집 완료.\n")
        
        browser.close()

    # 빈 리뷰(리뷰 관련 필드 모두 비어있음) 제거
    filtered_reviews = [
        r for r in all_reviews
        if any([r["username"], r["rating"], r["title"], r["content"], r["upvote"]])
    ]
    
    df_result = pd.DataFrame(filtered_reviews)
    df_result.to_excel("vr_games_review.xlsx", index=False)
    print(f"총 {len(filtered_reviews)}개의 리뷰가 'vr_games_review.xlsx'에 저장되었습니다.")

if __name__ == "__main__":
    main()
