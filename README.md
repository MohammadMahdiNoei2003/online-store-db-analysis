# 🛍️ Online Store Database and Data Analysis Project

> A fully structured data-driven project focusing on database modeling, SQL development, analytical insights, and visualizations — powered by PostgreSQL and Python.

---

## 📌 Project Goals

- Build and normalize a relational database for an online store (up to 4NF)
- Perform data analysis to extract KPIs and behavioral insights
- Visualize results using Python (Pandas, Seaborn, Plotly)
- Optional graph modeling with Neo4j for relationship analysis
- Ensure clean development practices with GitHub Actions and semantic commit standards

---

## ⚙️ Tech Stack

| Area            | Tools & Technologies                              |
|-----------------|---------------------------------------------------|
| Database        | PostgreSQL, pgAdmin, DBeaver, DataGrip            |
| Data Analysis   | SQL, Pandas, Jupyter Notebook                     |
| Visualization   | Matplotlib, Seaborn, Plotly                       |
| DevOps & CI     | GitHub Actions, Docker, Semantic Commits          |
| Documentation   | Markdown, dbdiagram.io                            |
| Versioning      | Semantic Versioning (SemVer)                      |

---

## 📁 Project Structure

```bash
.
├── .github/
│   ├── ISSUE_TEMPLATE/           # Templates for bug reports & feature requests
│   ├── workflows/                # GitHub Actions for CI/linting
│   └── PULL_REQUEST_TEMPLATE.md
├── data/                         # Cleaned datasets (for analysis)
├── diagrams/                     # ERD diagrams
├── notebooks/                    # Jupyter notebooks for data analysis
├── scripts/
│   ├── create_database.sql       # SQL schema creation
│   ├── insert_mock_data.sql      # Mock data script
│   └── queries/                  # CRUD & analytical SQL
├── execution-plan.md            # Project execution roadmap
├── CONTRIBUTING.md              # Collaboration guidelines
├── LICENSE                      # Project license
└── README.md                    # You're here
```

---

## 🚀 Getting Started

1. Clone the repository

```bash
git clone https://github.com/MohammadMahdiNoei2003/online-store-db-analysis.git
cd online-store-db-analysis
```

2. Set up the PostgreSQL database

```bash
docker-compose up -d
```

Or manually execute:

```bash
psql -U postgres -f scripts/create_database.sql
```

3. Add mock data (optional)

```bash
psql -U postgres -f scripts/insert_mock_data.sql
```

4. Run analysis

Use Jupyter notebooks from the `/notebooks/` folder to explore, transform, and visualize data.

---

## 📊 Features

- ✅ ERD and logical modeling (up to 4NF)
- ✅ CRUD queries + stored procedures
- ✅ Analytical SQL (AOV, customer activity, revenue trends)
- ✅ Dynamic reporting via SQL views
- ✅ Visualizations in Python
- ✅ Optional Neo4j modeling and Cypher queries
- ✅ CI/CD integration with GitHub Actions
- ✅ Semantic commits & conventional versioning

---

## 🧰 Contributing

This project follows conventional commits and branch protection policies.

Please read `CONTRIBUTING.md` before starting.

---

## 📄 License

This project is licensed under the MIT License.  
See `LICENSE` for more information.

---

## 👨‍💻 Author

**Mohammad Mahdi Noei**  
LinkedIn / GitHub / Portfolio → *(links to be added)*

---

## ⭐ If you find this project useful...
Give it a ⭐ on GitHub and share it with your network!
