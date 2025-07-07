# How to contribute to hackdb

thank you sooo much for considering. here are some ways you can help hackdb

## Report bugs in issues
You can even earn tokens with this :D

pls give a clear and obvious description of the bug/issue


## Submit PRs
Firstly clone the repo:
```
git clone https://github.com/meepstertron/HackDB.git
```

kubernetes recomended just apply all the .yaml files (make sure to change the image url)
docker works fine. just
```
docker compose up -d --build backend worker
cd frontend
npm run dev
```
change the url in api.ts though.