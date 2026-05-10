# BCCD Dataset - Image Selection Instructions

## Dataset Source
**BCCD (Blood Cell Count and Detection) Dataset**

This dataset contains microscopy images of blood cells with three classes:
- **RBC** (Red Blood Cells) - Most abundant, circular red-colored cells
- **WBC** (White Blood Cells) - Larger cells with visible nucleus (purple/blue stained)
- **Platelets** - Smallest elements, often appear as small purple dots

## Download Options

### Option 1: Roboflow (Recommended - Easiest)
1. Go to: https://public.roboflow.com/object-detection/bccd
2. Click "Download Dataset"
3. Select "Original" format or any image format
4. Download and extract
5. Select 10 images from the dataset

### Option 2: GitHub Repository
1. Go to: https://github.com/Shenggan/BCCD_Dataset
2. Clone or download the repository
3. Images are in `BCCD/JPEGImages/` folder
4. Select any 10 images (e.g., BloodImage_00001.jpg through BloodImage_00010.jpg)

### Option 3: Direct Download (Manual)
Clone the repository:
```bash
git clone https://github.com/Shenggan/BCCD_Dataset.git
```

## Selected Images for This Assignment

For this assignment, the following 10 images were selected:
1. BloodImage_00001.jpg
2. BloodImage_00002.jpg
3. BloodImage_00003.jpg
4. BloodImage_00004.jpg
5. BloodImage_00005.jpg
6. BloodImage_00006.jpg
7. BloodImage_00007.jpg
8. BloodImage_00008.jpg
9. BloodImage_00009.jpg
10. BloodImage_00010.jpg

These images were chosen because they:
- Contain a good mix of all three cell types
- Have varying cell densities
- Include both clear and challenging annotation scenarios

## Image Characteristics
- Format: JPEG
- Resolution: 640 x 480 pixels (typical)
- Color: RGB microscopy images with Giemsa staining
- Objects per image: Typically 50-100+ cells per image

## Notes
- Do NOT include the actual images in the GitHub repository to keep repo size small
- Reviewers can download the same images using these instructions
- The annotation export contains all bounding box coordinates and can be verified against the images
