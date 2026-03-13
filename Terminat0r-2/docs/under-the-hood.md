# under the hood

## backend

port 8000

endpoints:
- post /api/analyze (image_b64) → job_id, ai picks fact from data/interesting-facts.txt
- get /api/job/{job_id} (poll for result)
- post /api/quest/generate
- post /api/quest/verify
- get /api/user/{id}/stats

---

## ai flow

1. app captures frame from camera
2. post /api/analyze with base64 image
3. backend returns job_id, runs ai in background
4. ai (gemini/openai vision) describes scene: keywords
5. match keywords to categories in interesting-facts.txt
6. pick random fact from matched category
7. job result: { fact, category, keywords }

---

## app flow

1. home screen: camera view (can hide)
2. every 45 sec: capture → analyze → poll job
3. when result: show fact card overlay (8 sec, fade)
4. footer: links to quests, stats

---

## data file

data/interesting-facts.txt
format: category|fact
one fact per line, # for comments
