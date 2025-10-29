SymmetryVision
<img width="1836" height="1255" alt="SymmetryVision" src="https://github.com/user-attachments/assets/caa90776-1591-4bfc-ac1a-5615019d5744" />
---

AI-powered symmetry detection for images. Built for research. Designed for everyone.

Analyze vertical, horizontal, diagonal, and radial symmetry with quantitative precision. No manual inspection. No expensive software. Just upload, analyze, and understand.

---

Why I Built This

During my Master's research in Computer Vision, I spent countless hours manually analyzing architectural images for symmetry patterns. The process was frustrating: mark the center line, visually compare both sides, try to quantify what I saw, repeat for hundreds of images. Existing solutions either cost thousands of dollars for licenses or required complex MATLAB scripts that took longer to debug than to use.

One late night, after analyzing my 50th image of the day, I thought: **"There has to be a better way."

That's when I decided to build SymmetryVision. Not just for myself, but for every researcher, designer, and student who needs to understand symmetry objectively and efficiently.

The goal was simple: Create a tool that's fast, accurate, free, and actually enjoyable to use. Something that gives you real numbers, not just "looks symmetric to me." After weeks of coding, testing edge cases, and refining algorithms, SymmetryVision became what I wished existed when I started my research.

Now, what took me hours takes seconds. What was subjective is now quantifiable. What was expensive is now open-source.

---

What Problem Does This Solve?

The Challenge: Analyzing image symmetry manually is time-consuming and subjective. Professional tools cost thousands. Research needs reproducible, quantitative results.

The Solution: SymmetryVision automates symmetry detection using computer vision, providing objective scores and visual analysis in seconds.

Who Benefits: Researchers analyzing patterns, designers checking composition, students learning computer vision, manufacturers verifying product quality.

---

See It In Action

Main Interface
<img width="1836" height="1255" alt="SymmetryVision" src="https://github.com/user-attachments/assets/cda3e1c4-67ee-435a-be4b-ce3887138179" />


Upload & Analysis
<img width="2213" height="1257" alt="A" src="https://github.com/user-attachments/assets/3e112ca9-cbac-40b5-87f2-231dbab57160" />


Results Dashboard
<img width="2042" height="1268" alt="res" src="https://github.com/user-attachments/assets/40aa7256-c0c7-4d16-bcc1-6b999bb8d96f" />


Gallery Management
<img width="2023" height="1252" alt="gal" src="https://github.com/user-attachments/assets/07c0db94-dd91-4911-9622-46f2effa4854" />


---

Core Capabilities

Detection System
- Identifies 4 symmetry types: vertical, horizontal, diagonal (2 axes), radial
- Generates confidence scores (0-100%) for each detected axis
- Creates visual overlays highlighting symmetry lines
- Processes standard image formats (JPG, PNG, BMP, up to 10MB)

Analysis Output
- Overall symmetry score with weighted calculation
- Individual confidence metrics per axis type
- Processing time measurement
- Downloadable annotated images

Interface Design
- Single-page upload with immediate feedback
- Historical gallery with thumbnail previews
- Responsive layout adapting to screen size
- Interactive API documentation at `/api/docs`

---

Technical Foundation

Backend Architecture
```
FastAPI 0.109 + Python 3.9
├─ OpenCV 4.9 for image processing
├─ NumPy 1.26 for numerical operations
├─ Pydantic for data validation
└─ Uvicorn ASGI server
```

Frontend Stack
```
Next.js 14.1 + TypeScript 5.3
├─ React 18 component architecture
├─ Tailwind CSS 3.4 for styling
├─ Axios for API communication
└─ Lucide icons for UI elements
```

Why These Choices?
- FastAPI: Automatic OpenAPI docs, native async, type safety
- Next.js: Server-side rendering, optimal loading, file-based routing
- OpenCV: Industry-standard CV library, battle-tested algorithms
- TypeScript: Catches errors before runtime, better IDE support

---

Installation Guide

System Requirements
- Python 3.9 or newer
- Node.js 18 or newer
- 4GB available RAM
- Modern browser (Chrome, Firefox, Safari, Edge)

Start Backend Server
```bash
cd backend
python -m venv venv

# Activate environment
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux

# Install and run
pip install -r requirements.txt
python -m app.main
```
✅ Backend live at `http://localhost:8000`

Start Frontend Server
```bash
# New terminal window
cd frontend
npm install
npm run dev
```
✅ Frontend live at `http://localhost:3000`

Access the Application
Open `http://localhost:3000` in your browser. Upload an image to begin analysis.

---

Algorithm Mechanics

Processing Pipeline:
```
Input Image → Preprocessing → Detection → Scoring → Visualization
```

Step-by-Step:

1. Preprocessing
   - Convert to grayscale for uniform processing
   - Apply Gaussian blur to reduce noise
   - Detect edges using Canny algorithm

2. Symmetry Detection
   - Vertical: Split at center, flip right half, compute correlation
   - Horizontal: Split at center, flip bottom half, compute correlation
   - Diagonal: Rotate image, check for vertical symmetry
   - Radial: Test 8 rotational angles, measure consistency

3. **Confidence Calculation**
   - Normalized cross-correlation between halves
   - Convert correlation (-1 to +1) to confidence (0 to 1)
   - Apply threshold filtering (default: 0.75)

4. Overall Scoring
   - Weighted aggregation: vertical/horizontal (1.5×), radial (1.2×), diagonal (1.0×)
   - Normalize to 0-100 scale
   - Round to one decimal place

---

Project Structure

```
SymmetryVision/
│
├── backend/
│   ├── app/
│   │   ├── api/routes/        # REST endpoints
│   │   ├── core/              # Configuration
│   │   ├── ml/                # Detection algorithms
│   │   ├── models/            # Data schemas
│   │   ├── services/          # Business logic
│   │   └── main.py            # Application entry
│   ├── uploads/               # Temporary storage
│   ├── results/               # Processed images
│   ├── requirements.txt       # Dependencies
│   └── .env                   # Environment config
│
└── frontend/
    ├── src/
    │   ├── app/               # Page routes
    │   ├── components/        # React components
    │   ├── lib/               # Utilities & API client
    │   ├── styles/            # CSS modules
    │   └── types/             # TypeScript definitions
    ├── public/                # Static assets
    ├── package.json           # Node dependencies
    └── .env.local             # Frontend config
```

---

Research Applications

Computer Vision Studies
- Benchmark dataset for symmetry detection algorithms
- Comparative analysis across different image categories
- Algorithm performance evaluation

Architecture & Design
- Historical building symmetry analysis
- Urban planning pattern recognition
- Aesthetic composition scoring

Biology & Medicine
- Facial symmetry measurement in medical studies
- Organism morphology analysis
- Microscopy image evaluation

---

API Reference

Base URL: https://symmetry-vision.vercel.app/

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/analyze` | POST | Upload image, receive full analysis |
| `/analyze/{id}` | GET | Retrieve specific analysis result |
| `/gallery` | GET | List all analyzed images |
| `/gallery/{id}` | DELETE | Remove analysis from history |
| `/upload` | POST | Upload only (no analysis) |

Interactive Docs: Visit https://symmetry-vision.vercel.app/ for Swagger UI testing interface.

---

Development Roadmap

Version 1.0 (Current)
- ✅ Four-axis symmetry detection
- ✅ Web interface with gallery
- ✅ RESTful API with documentation
- ✅ Real-time processing feedback

Version 1.1 (Planned)
- [ ] Batch image processing
- [ ] PostgreSQL database integration
- [ ] User authentication system
- [ ] Analysis export to PDF

Version 2.0 (Future)
- [ ] Custom ML model training
- [ ] 3D object symmetry detection
- [ ] Video frame analysis
- [ ] Mobile application

---

Contributing

Ways to Contribute:
- Report bugs via GitHub Issues
- Suggest features or improvements
- Submit pull requests with enhancements
- Improve documentation clarity
- Share use cases from your field

Code Standards:
- Follow existing Python/TypeScript conventions
- Include docstrings for new functions
- Add tests for new features
- Update README for user-facing changes

---

Contact & Support

Developer: Hudayyar Yusubov   
Email: khudayyar@outlook.com  
**GitHub:** [@khudaiyar]https://github.com/khudaiyar

Issues & Questions: Open a GitHub issue for bug reports or feature requests.

Academic Use:If you use SymmetryVision in published research, please cite this repository.

---

Acknowledgments

This project emerged from practical research needs during my Master's program in Computer Vision. Special thanks to:
- OpenCV contributors for robust image processing tools
- FastAPI team for excellent async framework
- Next.js developers for seamless React experience
- Research advisors for encouraging practical implementations
- Open-source community for inspiration and resources

---
