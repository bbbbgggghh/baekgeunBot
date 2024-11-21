import yt_dlp
import asyncio
import random
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import unicodedata

exclude_keywords = ["영상 제목 크롤링 제외 키워드", "커버", "cover", "뮤직비디오", "라이브" "플레이리스트", "등등"]
cover = ["커버곡 탐색 키워드", "유튜버 이름", "제목", "등등"]

class autoplay:
    async def autoplay_recommended(self, ctx):
        if self.autoplay_try > 2:
            self.autoplay_try = 0
            await ctx.send("추천 곡 탐색 실패")
            return
        if hasattr(self, 'is_crawling') and self.is_crawling:
                self.is_crawling = False
                return
        self.is_crawling = True
        
        if self.current_url:
            song_url = self.current_url
            
            options = webdriver.ChromeOptions()
            #options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument('--incognito')
            options.add_argument('--disable-gpu')
            options.add_argument('--lang=ja')
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

            try:
                driver = await asyncio.get_running_loop().run_in_executor(
                None, lambda: webdriver.Chrome(options=options)
                )
                await asyncio.get_running_loop().run_in_executor(None, driver.get, song_url)
                await asyncio.sleep(2)
                response = await asyncio.get_running_loop().run_in_executor(None, lambda: driver.page_source)
                soup = BeautifulSoup(response, 'lxml')
                await asyncio.get_running_loop().run_in_executor(None, driver.quit)

                unfiltered = []
                for renderer in soup.find_all("ytd-compact-video-renderer", class_="style-scope ytd-watch-next-secondary-results-renderer"):
                    a_tag = renderer.find("a", {"class": "yt-simple-endpoint style-scope ytd-compact-video-renderer"})
                    if a_tag:
                        url = f'https://www.youtube.jp{a_tag.get("href")}'
                        if 'watch?v=' not in url:
                            continue

                        title_span = a_tag.find("span", {"id": "video-title"})
                        title = title_span.get("title") if title_span else None

                        dur_tag = renderer.find("div", {"class": "badge-shape-wiz__text"})
                        if dur_tag:
                            duration = dur_tag.text.strip()
                            if re.match(r'^[\d:]+$', duration):
                                time_parts = list(map(int, duration.split(':')))
                                if len(time_parts) == 3:
                                    hours, minutes, seconds = time_parts
                                elif len(time_parts) == 2:
                                    hours = 0
                                    minutes, seconds = time_parts
                                total_minutes = hours * 60 + minutes
                                if total_minutes >= 10:
                                    continue
                        else:
                            continue

                        view_tag = a_tag.find("span", {"class": "inline-metadata-item style-scope ytd-video-meta-block"})
                        view_text = view_tag.text.replace(" 回視聴", "").strip() if view_tag else "0"
                        if "視聴中" in view_text:
                            continue

                        if "億" in view_text:
                            view_count = int(float(view_text.replace("億", "")) * 1e8)
                        elif "万" in view_text:
                            view_count = int(float(view_text.replace("万", "")) * 1e4)
                        else:
                            view_count = int(re.sub(r'\D', '', view_text))

                        unfiltered.append((url, title, view_count))

                recommended_urls = []
                for url, title, view_count in unfiltered:
                    title_lower = unicodedata.normalize('NFKC', title).lower()
                    if self.is_cover:
                        if any(keyword in unicodedata.normalize('NFKC', self.prev_title[-1]).lower() for keyword in cover):
                            if (all(title != prev_title for prev_title in self.prev_title)
                                    and any(keyword in title_lower for keyword in cover)
                                    and not any(re.search(rf'(?<!\w){re.escape(keyword)}(?!\w)', title_lower) for keyword in exclude_keywords)):
                                recommended_urls.append((url, title, view_count))
                        else:
                            if (all(title != prev_title for prev_title in self.prev_title)
                                    and not any(re.search(rf'(?<!\w){re.escape(keyword)}(?!\w)', title_lower) for keyword in exclude_keywords) 
                                    and ('cover' in title_lower or '커버' in title_lower)):
                                recommended_urls.append((url, title, view_count))
                    else:
                        if (all(title != prev_title for prev_title in self.prev_title)
                                and not any(re.search(rf'(?<!\w){re.escape(keyword)}(?!\w)', title_lower) for keyword in exclude_keywords)):
                            recommended_urls.append((url, title, view_count))
                print("found", len(recommended_urls), "songs")
        
                if recommended_urls:
                    self.autoplay_try = 0
                    if self.is_cover:
                        if any(keyword in unicodedata.normalize('NFKC', self.prev_title[-1]).lower() for keyword in cover):
                            self.current_url = max(recommended_urls, key=lambda x: x[2])[0]
                            self.prev_title.append(max(recommended_urls, key=lambda x: x[2])[1])
                        else:
                            recommended_urls.sort(key=lambda x: x[2], reverse=True)
                            median = len(recommended_urls) // 2
                            self.current_url = recommended_urls[median][0]
                            self.prev_title.append(recommended_urls[median][1])
                        
                    else:
                        condition = bool(random.getrandbits(1))
                        if condition:
                            recommended_urls.sort(key=lambda x: x[2], reverse=True)
                            tmp = random.choice(recommended_urls[:5])
                            self.current_url = tmp[0]
                            self.prev_title.append(tmp[1])
                        else:
                            self.current_url = max(recommended_urls[:3], key=lambda x: x[2])[0]
                            self.prev_title.append(max(recommended_urls[:3], key=lambda x: x[2])[1])
                    
                    if len(self.prev_title) > 50:
                        self.prev_title.pop(0)

                    with yt_dlp.YoutubeDL({'format': 'bestaudio', 'buffer-size': '2M'}) as ydl:
                        info = ydl.extract_info(self.current_url, download=False)
                        url = info['url']
                        title = info['title']
                        print(title)
                        self.queue.append((url, title))
                        await ctx.send(f"음악 추가됨: **{title}**")
                else:
                    if driver:
                        await asyncio.get_running_loop().run_in_executor(None, driver.quit)
                    if self.autoplay:
                        self.autoplay_try += 1
                        self.is_crawling = False
                        await self.autoplay_recommended(ctx)

            except Exception as e:
                print(e)
                if driver:
                    await asyncio.get_running_loop().run_in_executor(None, driver.quit)
                if self.autoplay:
                    self.autoplay_try += 1
                    self.is_crawling = False
                    await self.autoplay_recommended(ctx)

            finally:
                self.is_crawling = False
                if driver:
                    await asyncio.get_running_loop().run_in_executor(None, driver.quit)

        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)
