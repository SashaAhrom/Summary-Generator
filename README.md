# Summary-Generator

 <summary>
Running a project with docker (preferred method)
 </summary>
<br />

1. Install docker and docker compose  suitable for your operating system. [official docker website](https://docs.docker.com/engine/install/)
```bash
docker compose version

~ Docker Compose version v2.2.3
```
2. Clone a project in /your_dir/
```bash
git clone git@github.com:SashaAhrom/Summary-Generator.git
```
3. Create a .env file 
```bash
cd /your_dir/Summary-Generator/  # go to main dir
touch .env  # create .env file
nano .env   # open the .env file and add variables below
```
4. Add variables
```bash
NUMBER_OF_REQUESTS=3
OPENAI_API_KEY=your_api_key
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/postgres_db
```

5. Start project.
```bash
docker compose up --build -d
```
