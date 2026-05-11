# TE Connectivity AI Hub Intern Assignment

## BCCD Blood Cell Detection - Annotation Workflow using Docker + Label Studio

This repository demonstrates a complete object detection annotation workflow using Label Studio running in Docker. The project annotates blood cell images from the BCCD dataset with three classes: **RBC**, **WBC**, and **Platelets**.

---

## Table of Contents
- [Project Summary](#project-summary)
- [Dataset](#dataset)
- [Quick Start](#quick-start)
- [Docker Setup](#docker-setup)
- [Label Studio Project Setup](#label-studio-project-setup)
- [Label Configuration](#label-configuration)
- [Annotation Summary](#annotation-summary)
- [Export Location](#export-location)
- [Screenshots](#screenshots)
- [Demo Video](#demo-video)
- [Repository Structure](#repository-structure)
- [Bonus Features](#bonus-features)
- [Issues Faced and Solutions](#issues-faced-and-solutions)
- [AI Tools Used](#ai-tools-used)
- [Annotation Quality at Scale](#annotation-quality-at-scale)

---

## Project Summary

This project sets up a local annotation workflow for object detection using:
- **Docker Desktop** for containerization
- **Label Studio** for image annotation
- **BCCD Dataset** for blood cell images

The goal is to demonstrate the ability to:
1. Run Label Studio locally using Docker
2. Create an object-detection labeling project
3. Import and annotate images with bounding boxes
4. Export annotations in multiple formats
5. Document the workflow clearly

---

## Dataset

**Source**: BCCD (Blood Cell Count and Detection) Dataset

| Source | Link |
|--------|------|
| Roboflow | https://public.roboflow.com/object-detection/bccd |
| GitHub | https://github.com/Shenggan/BCCD_Dataset |

### Selected Images
10 images were selected from the BCCD dataset:
- BloodImage_00001.jpg through BloodImage_00010.jpg
- See [samples/download_instructions.md](samples/download_instructions.md) for download steps

### Classes
| Class | Description | Color |
|-------|-------------|-------|
| RBC | Red Blood Cells | Red (#FF0000) |
| WBC | White Blood Cells | Blue (#0000FF) |
| Platelets | Platelets | Green (#00FF00) |

---

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git (optional, for cloning)

### Steps

```bash
# 1. Clone this repository
git clone https://github.com/Arun-sahukar/te-aihub-intern-assignment-arun-kumar.git
cd te-aihub-intern-assignment-arun-kumar

# 2. Start Label Studio using Docker Compose
docker-compose up -d

# 3. Open Label Studio in your browser
# Go to: http://localhost:8080

# 4. Create account and set up project (see instructions below)
```

---

## Docker Setup

### Option 1: Using Docker Compose (Recommended)

```bash
# Start Label Studio
docker-compose up -d

# View logs
docker-compose logs -f

# Stop Label Studio
docker-compose down
```

### Option 2: Using Docker Run

```bash
# Pull the image
docker pull heartexlabs/label-studio:latest

# Run the container
docker run -d -p 8080:8080 \
  -v label-studio-data:/label-studio/data \
  --name label-studio \
  heartexlabs/label-studio:latest
```

### Verify Docker is Running

```bash
docker ps
```

You should see the `label-studio` container running.

---

## Label Studio Project Setup

### Step 1: Access Label Studio
1. Open http://localhost:8080 in your browser
2. Create a new account (local account, no email verification needed)

### Step 2: Create Project
1. Click **"Create Project"**
2. Name: `BCCD Annotation Assignment`
3. Description: `Blood cell detection annotation project for TE Connectivity AI Hub assignment`

### Step 3: Import Images
1. Go to project settings → **Data Import**
2. Upload the 10 selected BCCD images
3. Wait for upload to complete

### Step 4: Configure Labels
1. Go to **Settings** → **Labeling Interface**
2. Select **"Custom template"**
3. Paste the contents of [label_config.xml](label_config.xml):

```xml
<View>
  <Image name="image" value="$image"/>
  <RectangleLabels name="label" toName="image">
    <Label value="RBC" background="#FF0000"/>
    <Label value="WBC" background="#0000FF"/>
    <Label value="Platelets" background="#00FF00"/>
  </RectangleLabels>
</View>
```

4. Click **Save**

---

## Label Configuration

The label configuration file (`label_config.xml`) defines:
- **Image source**: `$image` variable
- **Three bounding box labels**:
  - RBC (Red)
  - WBC (Blue)  
  - Platelets (Green)

This configuration enables rectangle bounding box annotation for object detection tasks.

---

## Annotation Summary

| Metric | Value |
|--------|-------|
| Total images imported | 10 |
| Images annotated | 5+ |
| Labels used | RBC, WBC, Platelets |
| Annotation type | Bounding boxes (rectangles) |

### Annotation Guidelines Followed
- Draw **tight bounding boxes** around each visible cell
- Select the **correct class** for each cell type
- Handle **overlapping cells** by drawing separate boxes when distinguishable
- Skip **partial cells** at image borders if less than 50% visible
- See [docs/edge_cases.md](docs/edge_cases.md) for detailed guidelines

---

## Export Location

Annotations are exported in multiple formats:

| Format | Location |
|--------|----------|
| Label Studio JSON | `exports/label_studio_export.json` |
| COCO Format | `exports/coco_format/annotations.json` |
| YOLO Format | `exports/yolo_format/` |

### How to Export from Label Studio
1. Go to your project
2. Click **Export**
3. Select **JSON** format
4. Save the file as `exports/label_studio_export.json`

### Convert to COCO/YOLO (Bonus)
```bash
# Convert to COCO format
python scripts/convert_to_coco.py

# Convert to YOLO format
python scripts/convert_to_yolo.py
```

---

## Screenshots

Screenshots are located in the `screenshots/` folder:

| Screenshot | Description |
|------------|-------------|
| `docker_running.png` | Docker Desktop showing Label Studio container running |
| `label_studio_project.png` | Label Studio project page |
| `annotated_example.png` | Example of annotated image with bounding boxes |

---

## Demo Video

**Google Drive Link**:https://drive.google.com/file/d/1OigOKACqJ9xUoa707G70zwqJZG2jJ-MR/view?usp=drive_link

Also available in: [video_link.txt](video_link.txt)

### Video Contents (3 minutes max)
- Docker running Label Studio
- Label Studio project page
- Configured labels (RBC, WBC, Platelets)
- One annotated image with bounding boxes
- Export file location in repository
- README walkthrough

---

## Repository Structure

```
te-aihub-intern-assignment-arun-kumar/
├── README.md                          # This file
├── label_config.xml                   # Label Studio labeling configuration
├── docker_commands.md                 # Docker commands reference
├── docker-compose.yml                 # Docker Compose for easy startup
├── video_link.txt                     # Google Drive video link
├── screenshots/
│   ├── docker_running.png            # Docker container running
│   ├── label_studio_project.png      # Project overview
│   └── annotated_example.png         # Annotated image example
├── exports/
│   ├── label_studio_export.json      # Main Label Studio export
│   ├── coco_format/
│   │   └── annotations.json          # COCO format export
│   └── yolo_format/
│       ├── classes.txt               # YOLO class names
│       └── *.txt                     # YOLO annotation files
├── samples/
│   └── download_instructions.md      # How to get BCCD images
├── scripts/
│   ├── validate_export.py            # Validates export file
│   ├── convert_to_coco.py            # Converts to COCO format
│   └── convert_to_yolo.py            # Converts to YOLO format
└── docs/
    ├── annotation_quality_plan.md    # Quality plan for 2500 images
    └── edge_cases.md                 # Edge case handling guidelines
```

---

## Bonus Features

### 1. Validation Script
Validates that the export file exists and contains valid annotations:
```bash
python scripts/validate_export.py
```

### 2. Format Conversion
Converts Label Studio export to COCO and YOLO formats:
```bash
python scripts/convert_to_coco.py
python scripts/convert_to_yolo.py
```

### 3. Docker Compose
Simplified startup with `docker-compose up -d`

### 4. Quality Plan
See [docs/annotation_quality_plan.md](docs/annotation_quality_plan.md) for scaling to 2,500 images

### 5. Edge Cases Documentation
See [docs/edge_cases.md](docs/edge_cases.md) for handling:
- Overlapping cells
- Tiny platelets
- Unclear objects
- Partial objects at borders

---

## Issues Faced and Solutions

### Issue 1: Docker Desktop Not Starting
**Problem**: Docker Desktop failed to start on Windows
**Solution**: Enabled WSL 2 and Hyper-V in Windows Features, then restarted

### Issue 2: Port 8080 Already in Use
**Problem**: Label Studio couldn't start because port 8080 was occupied
**Solution**: Changed the port mapping in docker-compose.yml to 8081:8080

### Issue 3: Images Not Loading in Label Studio
**Problem**: Imported images showed as broken links
**Solution**: Used the direct upload feature instead of URL-based import

### Issue 4: Annotation Not Saving
**Problem**: Annotations disappeared after refreshing
**Solution**: Ensured clicking "Submit" after completing each image annotation

---

## AI Tools Used

| Tool | Purpose |
|------|---------|
| Claude (Anthropic) | Generated project structure, scripts, and documentation |
| GitHub Copilot | Assisted with Python script syntax |
| ChatGPT | Clarified Label Studio configuration options |

### How AI Tools Helped
- **Project scaffolding**: Generated the initial folder structure and file templates
- **Script development**: Created validation and conversion scripts
- **Documentation**: Helped write clear, comprehensive documentation
- **Troubleshooting**: Provided solutions for Docker and Label Studio issues

**Note**: All AI-generated content was reviewed, understood, and customized for this specific assignment.

---

## Annotation Quality at Scale

### How to Ensure Quality When Annotating 2,500 Images with Business Users

1. **Clear Guidelines**: Create visual guidelines with examples of correct vs. incorrect annotations

2. **Training Session**: Conduct a 30-minute training with practice images before actual annotation

3. **Batch System**: Divide images into batches of 50-100, assign to annotators, track progress

4. **Spot Checks**: Review 10% of each annotator's work randomly

5. **Inter-Annotator Agreement**: Have 5% of images annotated by two people, measure agreement

6. **Automated Validation**: Run scripts to check for:
   - Missing annotations
   - Unusually small/large bounding boxes
   - Incorrect label distribution

7. **Feedback Loop**: Weekly meetings to share common mistakes and update guidelines

8. **Expert Review**: Domain expert reviews 5% of final dataset

See [docs/annotation_quality_plan.md](docs/annotation_quality_plan.md) for the complete plan.

---

## How to Reproduce This Work

1. **Install Docker Desktop** on your machine
2. **Clone this repository**
3. **Run** `docker-compose up -d`
4. **Open** http://localhost:8080
5. **Create account** and project named "BCCD Annotation Assignment"
6. **Download** 10 BCCD images (see samples/download_instructions.md)
7. **Import images** into Label Studio
8. **Configure labels** using label_config.xml
9. **Annotate** at least 5 images
10. **Export** as JSON to exports/label_studio_export.json
11. **Run** validation script: `python scripts/validate_export.py`

---

## License

This project was created for the TE Connectivity AI Hub Intern Assignment. The BCCD dataset is publicly available for educational and research purposes.

---

## Contact

**Author**: Arun Kumar  
**Assignment**: TE Connectivity AI Hub Intern - Docker + Label Studio Object Detection Workflow  
**Date**: May 2026
