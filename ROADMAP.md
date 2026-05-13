# 🛣️ Project Roadmap

> Visión de evolución del proyecto · RAM Pricing Prediction
> Última actualización: Mayo 2026

---

## 📊 Current Status (Mayo 2026)

```
✅ COMPLETED · Academic Phase 1.0
   • Web scraping pipeline (350 products from Newegg)
   • SQL database with B-Tree complexity analysis
   • Statistical inference (ANOVA, t-tests, Tukey HSD)
   • 5 predictive models trained and compared
   • Empirical ML complexity analysis (n up to 100,000)
   • Academic poster and final defense

🎯 CURRENT VERSION: v1.0 (Academic Release)
```

---

## 🚀 Roadmap

### Phase 1 · Foundation (COMPLETED ✅)
**Goal:** Build a complete data science pipeline from scratch

- [x] Web scraping infrastructure with multi-strategy regex parsers
- [x] Data cleaning and feature engineering
- [x] SQLite database with empirical complexity benchmarks
- [x] Statistical inference toolkit
- [x] 5 predictive models (OLS, Ridge, K-Means, Random Forest, Gradient Boosting)
- [x] Empirical ML complexity analysis
- [x] Professional academic poster
- [x] Final oral defense materials

---

### Phase 2 · Web Application (Planned · Q3 2026)
**Goal:** Transform academic project into interactive web product

#### 2.1 Frontend Dashboard
- [ ] React + Vite + TailwindCSS setup
- [ ] Interactive price predictor (user inputs specs → predicts price)
- [ ] Live model comparison visualizations (Recharts/Chart.js)
- [ ] Animated pipeline showcase (Framer Motion)
- [ ] Responsive design (mobile-first)
- [ ] Dark/light theme toggle

#### 2.2 Backend API
- [ ] FastAPI server with prediction endpoints
- [ ] Model serialization (joblib/pickle)
- [ ] Rate limiting and error handling
- [ ] OpenAPI documentation (Swagger)
- [ ] Input validation (Pydantic)

#### 2.3 Deployment
- [ ] Docker containerization
- [ ] GitHub Actions CI/CD
- [ ] Deploy to Vercel/Railway
- [ ] Custom domain configuration

**Estimated effort:** 40-60 hours

---

### Phase 3 · Data Expansion (Planned · Q4 2026)
**Goal:** Scale the dataset and improve model quality

#### 3.1 More Data Sources
- [ ] Amazon scraping (additional ~500 products)
- [ ] Best Buy integration
- [ ] eBay historical data
- [ ] Centralized data lake (PostgreSQL)

#### 3.2 Time Series Analysis
- [ ] Historical price tracking (weekly/monthly snapshots)
- [ ] Trend analysis with seasonal decomposition
- [ ] Inflation-adjusted comparisons
- [ ] Price prediction over time (not just current)

#### 3.3 Advanced Modeling
- [ ] XGBoost/LightGBM benchmarking
- [ ] Deep learning baseline (TensorFlow/PyTorch)
- [ ] AutoML comparison (auto-sklearn, H2O)
- [ ] Ensemble of ensembles

**Estimated effort:** 80-120 hours

---

### Phase 4 · Production Features (Future)
**Goal:** Make it a real-world useful tool

- [ ] User accounts and saved predictions
- [ ] Price alert system (email when target reached)
- [ ] Comparison wizard ("which RAM offers best $/GB?")
- [ ] Recommendation engine
- [ ] API marketplace integration
- [ ] Mobile app (React Native)

---

### Phase 5 · Research & Publication (Aspiration)
**Goal:** Submit findings to academic venue

- [ ] Refine methodology section
- [ ] Expand dataset to 5,000+ products
- [ ] Comparative analysis across categories (RAM, SSD, GPU)
- [ ] Submit to undergraduate research conference
- [ ] LinkedIn article series

---

## 📈 Success Metrics

### Phase 2 Success Criteria
- Working web app with < 200ms prediction latency
- 95+ Lighthouse score
- 1,000+ unique visitors in first month
- Deployed publicly with custom domain

### Phase 3 Success Criteria
- Dataset: 350 → 2,000+ products
- Best model MAPE: 8.32% → < 6%
- Time series predictions with 30-day forecast

### Long-term Vision
> Become the go-to open-source project for hardware price prediction,
> demonstrating end-to-end data science skills for software engineering portfolios.

---

## 🤝 Contributing

This project started as academic coursework but welcomes contributions:

- 🐛 Bug reports → GitHub Issues
- ✨ Feature requests → GitHub Discussions
- 📖 Documentation → Pull requests welcome
- 💡 Architectural feedback → Reach out via LinkedIn

---

## 📚 References & Inspirations

This roadmap is inspired by:
- Industry-standard data science projects (Kaggle, Hugging Face)
- Modern web app patterns (Vercel templates, awesome-fastapi)
- Academic research project life cycles
- Open source documentation best practices (Read the Docs)

---

## 📝 Changelog

| Version | Date | Highlights |
|---------|------|------------|
| v1.0 | May 2026 | Initial academic release · 5 models · poster |
| v0.x | May 2026 | Sprint of 12 days · daily commits · github |

See [CHANGELOG.md](CHANGELOG.md) for detailed history.

---

*Made with curiosity at Universidad de Guadalajara · 2026*
