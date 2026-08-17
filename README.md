# Abhimanyu Saklani — Portfolio

> A modern personal portfolio showcasing my work in **AI/ML and Data Science**

The portfolio is built with a heavily customized Streamlit frontend, a lightweight FastAPI backend, and an AI-powered **Ask About Myself** experience powered by Groq.

## 🔗 Links

- 🌐 **Live Demo:** `https://abhimanyusaklani.in`
- 💼 **LinkedIn:** `https://linkedin.com/in/abhimanyu-saklani`



---

## 📸 Screenshots

### Home 

![Portfolio Home](assets/screenshots/screenshot-1.png)



```markdown
![About Section](assets/screenshots/screenshot-2.png)
![Projects Section](assets/screenshots/screenshot-3.png)
```

---

## ✨ What the Portfolio Includes

- Modern responsive portfolio interface
- Custom Streamlit UI styled to feel like a real web portfolio
- Custom typography and design system
- Subtle animations and micro-interactions
- Responsive navigation and sidebar
- Hero section with availability status
- About section
- Education and experience timeline
- Technical skills
- Featured projects
- Academic projects
- Certifications and achievements
- Project detail and case-study pages
- Resume viewing and download
- Certificate viewing and downloads
- GitHub / LinkedIn / LeetCode / Kaggle links
- AI-powered **Ask About Myself** chatbot
- JSON-based content management
- Optional FastAPI REST API
- Docker support
- Railway deployment support

---

# 🛠️ Tech Stack

### Frontend
- Python
- Streamlit
- HTML
- CSS

### Backend
- FastAPI
- Uvicorn

### AI
- Groq API
- OpenAI GPT OSS 120B

### Deployment
- Docker
- Railway
- Streamlit Community Cloud

---

# 🧠 Architecture

The project keeps portfolio content separate from the application logic.

```text
                    ┌─────────────────────┐
                    │     data/*.json     │
                    │ Profile / Projects  │
                    │ Skills / Experience │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    data_loader.py   │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
        ┌──────────────────┐        ┌──────────────────┐
        │ Streamlit        │        │ FastAPI          │
        │ Frontend         │        │ REST Backend     │
        └────────┬─────────┘        └──────────────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Portfolio UI     │
        │ + AI Q&A         │
        └──────────────────┘
```

The Streamlit frontend reads the JSON data directly, so the FastAPI backend is optional.

---

# 📁 Project Structure

```text
portfolio/
├── frontend/                  # Streamlit application
│   ├── app.py                 # Main entry point
│   ├── components/            # Individual portfolio sections
│   │   ├── hero.py
│   │   ├── about.py
│   │   ├── experience.py
│   │   ├── education.py
│   │   ├── skills.py
│   │   ├── projects.py
│   │   ├── academic_projects.py
│   │   ├── achievements.py
│   │   ├── sidebar.py
│   │   └── ai_chat.py
│   ├── views/                 # Project detail / case-study views
│   ├── static/                # Generated PDF/static assets
│   ├── styles/
│   │   └── main.css           # Global styling
│   ├── data_loader.py         # Portfolio data loader
│   └── utils.py               # Shared helpers
│
├── backend/                   # Optional FastAPI backend
│   ├── main.py
│   ├── routes/
│   └── services/
│
├── data/                      # Portfolio content
│   ├── profile.json
│   ├── experience.json
│   ├── education.json
│   ├── projects.json
│   ├── academic_projects.json
│   ├── skills.json
│   └── achievements.json
│
├── assets/
│   ├── profile.jpg
│   ├── resume.pdf
│   ├── screenshots/
│   │   ├── screenshot-1.png
│   │   ├── screenshot-2.png
│   │   └── ...
│   ├── projects/
│   └── certificates/
│
├── .streamlit/
│   └── secrets.toml.example
│
├── Dockerfile
├── requirements.txt
├── Procfile
├── railway.json
├── .gitignore
└── README.md
```

---

# 🚀 Run Locally

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd portfolio
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure the AI chatbot

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

Keep this file local. It should never be committed to GitHub.

## 5. Start the portfolio

```bash
streamlit run frontend/app.py
```

Open:

```text
http://localhost:8501
```

After changing JSON content, refresh the browser to see the updates.

---

# 🤖 Ask About Myself

The homepage includes an AI-powered **Ask About Myself** chatbot.

Visitors can ask questions such as:

```text
What are your technical skills?
Tell me about your Spark optimization project.
What is your educational background?
What projects have you worked on?
What kind of roles are you looking for?
```

The chatbot is grounded in the portfolio data and is intended to answer questions about my professional background.

### Model

```text
openai/gpt-oss-120b
```

The chatbot uses low reasoning effort and hides model reasoning so visitors only see the final answer.

### API Key

Local development:

```text
.streamlit/secrets.toml
```

Production:

```text
GROQ_API_KEY
```

as an environment variable.

Never put the API key in source code, JSON files, Dockerfiles, or GitHub.

---

# 📝 Updating Content

Most portfolio content can be changed without touching Python.

| Content | File |
|---|---|
| Name, hero, bio, links, target roles | `data/profile.json` |
| Work experience | `data/experience.json` |
| Education | `data/education.json` |
| Skills | `data/skills.json` |
| Featured projects | `data/projects.json` |
| Academic projects | `data/academic_projects.json` |
| Certifications & achievements | `data/achievements.json` |

The Python components are mainly for changing layout, styling, and behavior.

---

# 📸 Profile Photo & Resume

Add your profile photo:

```text
assets/profile.jpg
```

Add your resume:

```text
assets/resume.pdf
```

Both are optional.

The application gracefully handles missing assets.

PDF assets may be mirrored into:

```text
frontend/static/
```

automatically. Generated files in that directory should not be edited manually.

---

# 📂 Adding Projects

Create a project folder:

```text
assets/projects/my-project/
├── hero.png
├── screenshot-1.png
├── screenshot-2.png
└── case-study.pdf
```

Then add the project to:

```text
data/projects.json
```

Example:

```json
{
  "id": "my-project",
  "number": "01",
  "title": "Project Name",
  "tagline": "One short description.",
  "description": "A concise project summary.",
  "technologies": ["Python", "PyTorch", "SQL"],
  "github": "",
  "demo": "",
  "hero_image": "assets/projects/my-project/hero.png",
  "screenshots": [
    "assets/projects/my-project/screenshot-1.png"
  ],
  "case_study": "assets/projects/my-project/case-study.pdf",
  "problem": "...",
  "solution": "...",
  "contribution": "...",
  "results": [
    "A measurable result"
  ]
}
```

Optional fields are hidden automatically when they are empty.

---

# 🏆 Certifications

Store local certificate PDFs in:

```text
assets/certificates/
```

Then reference them from:

```text
data/achievements.json
```

Certificates can also use external credential URLs.

For local files, make sure the filename matches exactly.

---

# ⚡ FastAPI Backend

The FastAPI backend is optional.

The frontend reads the JSON files directly, so FastAPI does not need to run for the portfolio itself.

Start it locally:

```bash
uvicorn backend.main:app --reload --port 8000
```

API:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

The backend can be deployed separately if REST API access is required.

---

# 🐳 Docker

Build:

```bash
docker build -t abhimanyu-portfolio .
```

Run:

```bash
docker run -p 8501:8501 abhimanyu-portfolio
```

Open:

```text
http://localhost:8501
```

For local Docker testing with the AI chatbot:

```bash
docker run -p 8501:8501 -e GROQ_API_KEY="your-groq-api-key" abhimanyu-portfolio
```

Never hard-code secrets into the Dockerfile or source code.

---

# 🚢 Deployment

## Railway

The project is prepared for Railway deployment.

```text
GitHub
   ↓
Railway
   ↓
Docker / Python build
   ↓
Streamlit
   ↓
Live Portfolio
```

### Steps

1. Push the repository to GitHub.
2. Create a new Railway project.
3. Select **Deploy from GitHub Repo**.
4. Choose the portfolio repository.
5. Add environment variables.
6. Generate a public domain.
7. Test the live application.

For the AI chatbot, add:

```text
GROQ_API_KEY
```

to Railway's environment variables.

Do not upload:

```text
.streamlit/secrets.toml
```

Once GitHub and Railway are connected, new pushes can trigger automatic deployments.

### Production Checklist

Before deploying:

- [ ] Portfolio works locally
- [ ] All screenshots load
- [ ] Resume loads
- [ ] Certificate links work
- [ ] Project links work
- [ ] AI chatbot returns answers
- [ ] `GROQ_API_KEY` is configured in Railway
- [ ] No API keys are committed
- [ ] `README.md` Live Demo URL is updated
- [ ] Mobile/responsive layout is checked

---

# ☁️ Streamlit Community Cloud

The application can also be deployed through Streamlit Community Cloud.

Use:

```text
frontend/app.py
```

as the entry point and configure the Groq API key through Streamlit secrets.

Before pushing:

```bash
git status
```

Then:

```bash
git add .
git commit -m "Update portfolio"
git push
```

If an API key was ever committed accidentally, revoke it and create a new one.

---


Streamlit provides the application framework while custom HTML/CSS controls most of the visual experience.

---

# 🧩 Architecture Philosophy

The project follows a simple separation:

```text
JSON data
    ↓
data_loader.py
    ↓
Frontend components
    ↓
Streamlit UI
```

The optional API layer follows:

```text
JSON data
    ↓
FastAPI
    ↓
REST API
```

This makes content updates simple while keeping layout and application logic separate.


---

## 📄 License

This is a personal portfolio project.

The code can be used as a learning/reference resource, but personal information, branding, resume content, certificates, screenshots, images, and other personal assets should not be reused without permission.
